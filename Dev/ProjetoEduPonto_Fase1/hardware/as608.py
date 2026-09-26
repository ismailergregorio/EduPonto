import time
from typing import Optional, Tuple

import serial

from config.config import (
    AS608_ENDERECO,
    AS608_HEADER,
    AS608_ID_MAX,
    AS608_ID_MIN,
    INTERVALO_POLLING,
    TIMEOUT_SERIAL,
)


class AS608Error(Exception):
    """Erro relacionado a comunicacao ou comandos do AS608."""


class AS608:
    PACKAGE_COMMAND = 0x01
    PACKAGE_DATA = 0x02
    PACKAGE_ACK = 0x07

    OK = 0x00
    NO_FINGER = 0x02
    ENROLL_FAIL = 0x03
    IMAGE_FAIL = 0x06
    MATCH_FAIL = 0x08
    NOT_FOUND = 0x09
    DELETE_FAIL = 0x10
    CLEAR_FAIL = 0x11
    INVALID_IMAGE = 0x15
    FLASH_ERROR = 0x18

    ERROR_MESSAGES = {
        0x01: "Erro ao receber pacote.",
        0x02: "Nenhum dedo detectado.",
        0x03: "Falha ao cadastrar a digital.",
        0x06: "Falha ao gerar imagem/template.",
        0x07: "Falha na combinacao das digitais.",
        0x08: "Digitais nao conferem.",
        0x09: "Digital nao encontrada.",
        0x0A: "Falha ao combinar templates.",
        0x0B: "Endereco fora do limite.",
        0x0C: "Erro ao ler template.",
        0x0D: "Erro ao transferir template.",
        0x0E: "Sensor nao conseguiu receber os dados.",
        0x0F: "Erro ao transferir imagem.",
        0x10: "Falha ao excluir digital.",
        0x11: "Falha ao limpar memoria.",
        0x13: "Senha do sensor incorreta.",
        0x15: "Imagem invalida.",
        0x18: "Erro de memoria Flash.",
    }

    def __init__(
        self,
        porta: str,
        baudrate: int = 57600,
        timeout: float = TIMEOUT_SERIAL,
        endereco: int = AS608_ENDERECO,
    ):
        self.porta = porta
        self.baudrate = baudrate
        self.timeout = timeout
        self.endereco = endereco
        self._serial: Optional[serial.Serial] = None

    @property
    def conectado(self) -> bool:
        return self._serial is not None and self._serial.is_open

    def conectar(self) -> None:
        if self.conectado:
            return

        try:
            self._serial = serial.Serial(
                port=self.porta,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=self.timeout,
                write_timeout=self.timeout,
            )
            self._serial.reset_input_buffer()
            self._serial.reset_output_buffer()
        except serial.SerialException as exc:
            self._serial = None
            raise AS608Error(
                f"Nao foi possivel abrir a porta {self.porta}: {exc}"
            ) from exc

    def fechar(self) -> None:
        if self._serial is not None:
            try:
                self._serial.close()
            finally:
                self._serial = None

    def _garantir_conexao(self) -> None:
        if not self.conectado:
            raise AS608Error("AS608 nao conectado.")

    def _limpar_buffer(self) -> None:
        self._serial.reset_input_buffer()

    def _montar_pacote(self, tipo: int, dados: bytes) -> bytes:
        endereco = self.endereco.to_bytes(4, "big")
        comprimento = len(dados) + 2
        comprimento_bytes = comprimento.to_bytes(2, "big")

        checksum_base = (
            bytes((tipo,))
            + comprimento_bytes
            + dados
        )
        checksum = sum(checksum_base) & 0xFFFF

        return (
            AS608_HEADER
            + endereco
            + checksum_base
            + checksum.to_bytes(2, "big")
        )

    def _ler_exatamente(self, quantidade: int) -> bytes:
        dados = bytearray()

        while len(dados) < quantidade:
            bloco = self._serial.read(quantidade - len(dados))
            if not bloco:
                raise AS608Error("Timeout aguardando resposta do AS608.")
            dados.extend(bloco)

        return bytes(dados)

    def _ler_pacote(self) -> Tuple[int, bytes]:
        self._garantir_conexao()

        estado = bytearray()

        while True:
            byte = self._serial.read(1)

            if not byte:
                raise AS608Error("Timeout aguardando resposta do AS608.")

            estado += byte

            if len(estado) > 2:
                estado = estado[-2:]

            if bytes(estado) == AS608_HEADER:
                break

        endereco = self._ler_exatamente(4)
        tipo = self._ler_exatamente(1)[0]
        comprimento_bytes = self._ler_exatamente(2)
        comprimento = int.from_bytes(comprimento_bytes, "big")

        if comprimento < 2:
            raise AS608Error("Tamanho de pacote invalido recebido do AS608.")

        dados_e_checksum = self._ler_exatamente(comprimento)
        dados = dados_e_checksum[:-2]
        checksum_recebido = int.from_bytes(dados_e_checksum[-2:], "big")

        checksum_calculado = (
            sum(bytes((tipo,)) + comprimento_bytes + dados) & 0xFFFF
        )

        if checksum_calculado != checksum_recebido:
            raise AS608Error(
                "Checksum invalido na resposta do AS608."
            )

        _ = endereco
        return tipo, dados

    def _enviar_comando(self, dados: bytes, timeout: Optional[float] = None) -> bytes:
        self._garantir_conexao()

        pacote = self._montar_pacote(self.PACKAGE_COMMAND, dados)

        try:
            if timeout is not None:
                timeout_anterior = self._serial.timeout
                self._serial.timeout = timeout
            else:
                timeout_anterior = None

            self._limpar_buffer()
            self._serial.write(pacote)
            self._serial.flush()

            tipo, resposta = self._ler_pacote()

            if tipo != self.PACKAGE_ACK:
                raise AS608Error(
                    f"Tipo de pacote inesperado: 0x{tipo:02X}"
                )

            if not resposta:
                raise AS608Error("Resposta vazia do AS608.")

            codigo = resposta[0]
            if codigo != self.OK:
                mensagem = self.ERROR_MESSAGES.get(
                    codigo,
                    f"Codigo de erro 0x{codigo:02X}.",
                )
                raise AS608Error(mensagem)

            return resposta
        except serial.SerialException as exc:
            raise AS608Error(f"Falha na comunicacao serial: {exc}") from exc
        finally:
            if timeout is not None and self._serial is not None:
                self._serial.timeout = timeout_anterior

    def _enviar_sem_erro(self, dados: bytes, timeout: Optional[float] = None):
        self._garantir_conexao()

        pacote = self._montar_pacote(self.PACKAGE_COMMAND, dados)

        try:
            if timeout is not None:
                timeout_anterior = self._serial.timeout
                self._serial.timeout = timeout
            else:
                timeout_anterior = None

            self._limpar_buffer()
            self._serial.write(pacote)
            self._serial.flush()

            tipo, resposta = self._ler_pacote()

            if tipo != self.PACKAGE_ACK:
                raise AS608Error(
                    f"Tipo de pacote inesperado: 0x{tipo:02X}"
                )

            if not resposta:
                raise AS608Error("Resposta vazia do AS608.")

            codigo = resposta[0]
            return codigo, resposta
        except serial.SerialException as exc:
            raise AS608Error(f"Falha na comunicacao serial: {exc}") from exc
        finally:
            if timeout is not None and self._serial is not None:
                self._serial.timeout = timeout_anterior

    def detectar_dedo(self) -> bool:
        codigo, _ = self._enviar_sem_erro(bytes((0x01,)))

        if codigo == self.OK:
            return True

        if codigo == self.NO_FINGER:
            return False

        mensagem = self.ERROR_MESSAGES.get(
            codigo,
            f"Codigo de erro 0x{codigo:02X}.",
        )
        raise AS608Error(mensagem)

    def capturar_imagem(self) -> bool:
        return self.detectar_dedo()

    def converter_imagem(self, buffer: int = 1) -> bool:
        if buffer not in (1, 2):
            raise AS608Error("Buffer deve ser 1 ou 2.")

        self._enviar_comando(bytes((0x02, buffer)))
        return True

    def gerar_modelo(self) -> bool:
        self._enviar_comando(bytes((0x05,)))
        return True

    def salvar_digital(self, id_biometrico: int, buffer: int = 1) -> bool:
        self._validar_id(id_biometrico)

        if buffer not in (1, 2):
            raise AS608Error("Buffer deve ser 1 ou 2.")

        dados = bytes((
            0x06,
            buffer,
            (id_biometrico >> 8) & 0xFF,
            id_biometrico & 0xFF,
        ))
        self._enviar_comando(dados)
        return True

    def buscar_digital(
        self,
        inicio: int = AS608_ID_MIN,
        quantidade: int = AS608_ID_MAX,
    ) -> Tuple[int, int]:
        if inicio < 0 or inicio > 0xFFFF:
            raise AS608Error("ID inicial invalido.")

        if quantidade <= 0 or quantidade > 0xFFFF:
            raise AS608Error("Quantidade de busca invalida.")

        dados = bytes((
            0x04,
            0x01,
            (inicio >> 8) & 0xFF,
            inicio & 0xFF,
            (quantidade >> 8) & 0xFF,
            quantidade & 0xFF,
        ))

        resposta = self._enviar_comando(dados)

        if len(resposta) < 5:
            raise AS608Error("Resposta de busca invalida.")

        id_biometrico = (resposta[1] << 8) | resposta[2]
        confianca = (resposta[3] << 8) | resposta[4]

        return id_biometrico, confianca

    def deletar_digital(
        self,
        id_biometrico: int,
        quantidade: int = 1,
    ) -> bool:
        self._validar_id(id_biometrico)

        if quantidade <= 0 or quantidade > 0xFFFF:
            raise AS608Error("Quantidade invalida para exclusao.")

        dados = bytes((
            0x0C,
            (id_biometrico >> 8) & 0xFF,
            id_biometrico & 0xFF,
            (quantidade >> 8) & 0xFF,
            quantidade & 0xFF,
        ))

        self._enviar_comando(dados)
        return True

    def verificar_digital(self, id_biometrico: int) -> bool:
        self._validar_id(id_biometrico)

        self._esperar_dedo(timeout=10.0)
        self.capturar_imagem()
        self.converter_imagem(buffer=1)

        dados_load = bytes((
            0x07,
            0x02,
            (id_biometrico >> 8) & 0xFF,
            id_biometrico & 0xFF,
        ))
        self._enviar_comando(dados_load)

        self._enviar_comando(bytes((0x03,)))
        return True

    def get_template_count(self) -> int:
        resposta = self._enviar_comando(bytes((0x1D,)))

        if len(resposta) < 3:
            raise AS608Error("Resposta invalida ao consultar quantidade.")

        return (resposta[1] << 8) | resposta[2]

    def _esperar_dedo(self, timeout: float) -> None:
        limite = time.monotonic() + timeout

        while time.monotonic() < limite:
            if self.detectar_dedo():
                return
            time.sleep(INTERVALO_POLLING)

        raise AS608Error("Tempo esgotado aguardando o dedo.")

    def esperar_remocao_dedo(self, timeout: float) -> None:
        limite = time.monotonic() + timeout

        while time.monotonic() < limite:
            if not self.detectar_dedo():
                return
            time.sleep(INTERVALO_POLLING)

        raise AS608Error("Tempo esgotado aguardando a remocao do dedo.")

    @staticmethod
    def _validar_id(id_biometrico: int) -> None:
        if not isinstance(id_biometrico, int):
            raise AS608Error("ID biometrico deve ser inteiro.")

        if id_biometrico < 0 or id_biometrico > 0xFFFF:
            raise AS608Error("ID biometrico fora do intervalo permitido.")

    def _teste_conexao(self) -> bool:
        self.get_template_count()
        return True
