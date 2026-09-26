from config.config import PORTA_SERIAL, BAUDRATE
from hardware.as608 import AS608, AS608Error


def main():
    try:
        id_biometrico = int(
            input("Informe o ID biometrico a verificar: ").strip()
        )
    except ValueError:
        print("ID invalido.")
        return

    sensor = AS608(PORTA_SERIAL, BAUDRATE)

    try:
        sensor.conectar()
        print("Coloque o dedo no sensor.")

        try:
            sensor.verificar_digital(id_biometrico)
            print("\nDIGITAL CONFERE COM O ID INFORMADO.")
        except AS608Error as exc:
            if "nao conferem" in str(exc).lower():
                print("\nDIGITAL NAO CONFERE.")
            else:
                raise

    except AS608Error as exc:
        print(f"\nERRO: {exc}")
    finally:
        sensor.fechar()


if __name__ == "__main__":
    main()
