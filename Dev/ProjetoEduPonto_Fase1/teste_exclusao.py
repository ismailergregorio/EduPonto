from config.config import PORTA_SERIAL, BAUDRATE
from hardware.as608 import AS608, AS608Error


def main():
    try:
        id_biometrico = int(
            input("Informe o ID biometrico para excluir: ").strip()
        )
    except ValueError:
        print("ID invalido.")
        return

    sensor = AS608(PORTA_SERIAL, BAUDRATE)

    try:
        sensor.conectar()

        if sensor.deletar_digital(id_biometrico):
            print("Digital excluida com sucesso.")

    except AS608Error as exc:
        print(f"ERRO: {exc}")
    finally:
        sensor.fechar()


if __name__ == "__main__":
    main()
