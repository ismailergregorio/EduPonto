from config.config import PORTA_SERIAL, BAUDRATE
from hardware.as608 import AS608
from biometria.validacao import identificar_digital


def main():
    sensor = AS608(PORTA_SERIAL, BAUDRATE)

    try:
        sensor.conectar()

        print("Coloque o dedo no sensor.")
        resultado = identificar_digital(sensor)

        if resultado["encontrado"]:
            print("\nDIGITAL ENCONTRADA")
            print(f"ID biometrico: {resultado['id_biometrico']}")
            print(f"Nivel de confianca: {resultado['confianca']}")
        else:
            print("\nDIGITAL NAO ENCONTRADA")

    finally:
        sensor.fechar()


if __name__ == "__main__":
    main()
