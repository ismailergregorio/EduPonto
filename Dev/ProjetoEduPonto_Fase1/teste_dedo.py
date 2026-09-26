import time

from config.config import PORTA_SERIAL, BAUDRATE
from hardware.as608 import AS608, AS608Error


def main():
    sensor = AS608(PORTA_SERIAL, BAUDRATE)

    try:
        sensor.conectar()

        print("Teste de deteccao de dedo")
        print("Coloque o dedo e retire algumas vezes.")
        print("Pressione Ctrl+C para encerrar.\n")

        estado_anterior = False

        while True:
            estado_atual = sensor.detectar_dedo()

            if estado_atual and not estado_anterior:
                print("DEDO DETECTADO")
            elif not estado_atual and estado_anterior:
                print("DEDO REMOVIDO")

            estado_anterior = estado_atual
            time.sleep(0.15)

    except KeyboardInterrupt:
        print("\nTeste encerrado.")
    except AS608Error as exc:
        print(f"\nERRO: {exc}")
    finally:
        sensor.fechar()


if __name__ == "__main__":
    main()
