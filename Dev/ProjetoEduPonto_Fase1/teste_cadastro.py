from config.config import PORTA_SERIAL, BAUDRATE
from hardware.as608 import AS608
from biometria.cadastro import cadastrar_digital


def main():
    try:
        id_biometrico = int(
            input("Informe o ID biometrico para cadastrar: ").strip()
        )
    except ValueError:
        print("ID invalido.")
        return

    sensor = AS608(PORTA_SERIAL, BAUDRATE)

    try:
        sensor.conectar()
        resultado = cadastrar_digital(sensor, id_biometrico)

        if resultado["sucesso"]:
            print("\nCADASTRO CONCLUIDO")
            print(f"ID salvo: {resultado['id']}")
        else:
            print("\nFALHA NO CADASTRO")
            print(resultado["erro"])

    finally:
        sensor.fechar()


if __name__ == "__main__":
    main()
