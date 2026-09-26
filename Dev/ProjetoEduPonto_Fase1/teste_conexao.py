from config.config import PORTA_SERIAL, BAUDRATE
from hardware.as608 import AS608, AS608Error


def main():
    sensor = AS608(PORTA_SERIAL, BAUDRATE)

    try:
        print("Abrindo comunicacao com o AS608...")
        sensor.conectar()
        print("Conexao aberta com sucesso.")

        quantidade = sensor.get_template_count()
        print(f"Quantidade de digitais na memoria: {quantidade}")

    except AS608Error as exc:
        print(f"ERRO: {exc}")

    finally:
        sensor.fechar()
        print("Porta serial fechada.")


if __name__ == "__main__":
    main()
