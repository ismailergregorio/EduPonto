from hardware.as608 import AS608, AS608Error


def cadastrar_digital(
    sensor: AS608,
    id_biometrico: int,
    timeout: float = 20.0,
):
    """
    Executa o cadastro completo da digital no AS608.

    Fluxo:
    1. Aguarda o primeiro dedo.
    2. Captura e converte no buffer 1.
    3. Aguarda a retirada.
    4. Aguarda o mesmo dedo novamente.
    5. Captura e converte no buffer 2.
    6. Gera o modelo.
    7. Salva no ID informado.
    """
    try:
        print("\n=== CADASTRO DA DIGITAL ===")
        print("Coloque o dedo no sensor...")
        sensor._esperar_dedo(timeout)
        sensor.capturar_imagem()
        sensor.converter_imagem(buffer=1)

        print("Primeira leitura concluida.")
        print("Retire o dedo...")
        sensor.esperar_remocao_dedo(timeout)

        print("Coloque o mesmo dedo novamente...")
        sensor._esperar_dedo(timeout)
        sensor.capturar_imagem()
        sensor.converter_imagem(buffer=2)

        print("Segunda leitura concluida.")
        print("Gerando modelo...")
        sensor.gerar_modelo()

        print(f"Salvando digital no ID {id_biometrico}...")
        sensor.salvar_digital(id_biometrico, buffer=1)

        return {
            "sucesso": True,
            "id": id_biometrico,
        }

    except AS608Error as exc:
        return {
            "sucesso": False,
            "erro": str(exc),
        }
