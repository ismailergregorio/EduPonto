from config.config import PORTA_SERIAL, BAUDRATE
from hardware.as608 import AS608, AS608Error
from biometria.cadastro import cadastrar_digital
from biometria.validacao import identificar_digital


def pausar():
    input("\nPressione ENTER para continuar...")


def conectar_sensor():
    sensor = AS608(PORTA_SERIAL, BAUDRATE)
    sensor.conectar()
    return sensor


def menu_principal():
    print("\n" + "=" * 40)
    print("              EDUPONTO")
    print("         FASE 1 - BIOMETRIA")
    print("=" * 40)
    print(f"Porta: {PORTA_SERIAL}")
    print(f"Baudrate: {BAUDRATE}")
    print()
    print("1 - Testar conexao com AS608")
    print("2 - Testar deteccao de dedo")
    print("3 - Cadastrar digital")
    print("4 - Buscar digital")
    print("5 - Verificar digital por ID")
    print("6 - Excluir digital")
    print("7 - Monitorar sensor")
    print("0 - Sair")
    return input("\nOpcao: ").strip()


def testar_conexao():
    sensor = None
    try:
        sensor = conectar_sensor()
        print("\nAS608 conectado com sucesso.")
        print(f"Status: {sensor.get_template_count()} digitais armazenadas.")
    except AS608Error as exc:
        print(f"\nErro ao conectar ao AS608: {exc}")
    finally:
        if sensor:
            sensor.fechar()
    pausar()


def testar_deteccao():
    sensor = None
    try:
        sensor = conectar_sensor()
        print("\nColoque o dedo no sensor.")
        while True:
            if sensor.detectar_dedo():
                print("Dedo detectado.")
                break
    except KeyboardInterrupt:
        print("\nTeste interrompido.")
    except AS608Error as exc:
        print(f"\nErro no AS608: {exc}")
    finally:
        if sensor:
            sensor.fechar()
    pausar()


def testar_cadastro():
    sensor = None
    try:
        sensor = conectar_sensor()
        texto = input("\nID biometrico para salvar: ").strip()
        id_biometrico = int(texto)

        resultado = cadastrar_digital(sensor, id_biometrico)

        if resultado["sucesso"]:
            print("\nDigital cadastrada com sucesso.")
            print(f"ID: {resultado['id']}")
        else:
            print(f"\nFalha: {resultado['erro']}")
    except ValueError:
        print("\nID invalido.")
    except AS608Error as exc:
        print(f"\nErro no AS608: {exc}")
    except KeyboardInterrupt:
        print("\nCadastro interrompido.")
    finally:
        if sensor:
            sensor.fechar()
    pausar()


def testar_busca():
    sensor = None
    try:
        sensor = conectar_sensor()
        print("\nColoque o dedo no sensor.")
        resultado = identificar_digital(sensor)

        if resultado["encontrado"]:
            print("\nDIGITAL ENCONTRADA")
            print(f"ID: {resultado['id_biometrico']}")
            print(f"Confianca: {resultado['confianca']}")
        else:
            print("\nDigital nao encontrada.")
    except AS608Error as exc:
        print(f"\nErro no AS608: {exc}")
    except KeyboardInterrupt:
        print("\nBusca interrompida.")
    finally:
        if sensor:
            sensor.fechar()
    pausar()


def testar_verificacao():
    sensor = None
    try:
        sensor = conectar_sensor()
        id_biometrico = int(input("\nID biometrico cadastrado: ").strip())

        print("\nColoque o dedo no sensor.")
        resultado = sensor.verificar_digital(id_biometrico)

        if resultado:
            print("\nDIGITAL CONFERE COM O ID INFORMADO.")
        else:
            print("\nDIGITAL NAO CONFERE.")
    except ValueError:
        print("\nID invalido.")
    except AS608Error as exc:
        print(f"\nErro no AS608: {exc}")
    except KeyboardInterrupt:
        print("\nVerificacao interrompida.")
    finally:
        if sensor:
            sensor.fechar()
    pausar()


def testar_exclusao():
    sensor = None
    try:
        sensor = conectar_sensor()
        id_biometrico = int(input("\nID biometrico para excluir: ").strip())

        if sensor.deletar_digital(id_biometrico):
            print("\nDigital excluida com sucesso.")
        else:
            print("\nNao foi possivel excluir a digital.")
    except ValueError:
        print("\nID invalido.")
    except AS608Error as exc:
        print(f"\nErro no AS608: {exc}")
    finally:
        if sensor:
            sensor.fechar()
    pausar()


def monitorar_sensor():
    sensor = None
    try:
        sensor = conectar_sensor()
        print("\nMonitorando o AS608.")
        print("Coloque e retire o dedo varias vezes.")
        print("Pressione Ctrl+C para sair.\n")

        ultimo_estado = False

        while True:
            estado = sensor.detectar_dedo()

            if estado and not ultimo_estado:
                print("Dedo detectado.")
            elif not estado and ultimo_estado:
                print("Dedo removido.")

            ultimo_estado = estado
    except KeyboardInterrupt:
        print("\nMonitoramento encerrado.")
    except AS608Error as exc:
        print(f"\nErro no AS608: {exc}")
    finally:
        if sensor:
            sensor.fechar()
    pausar()


def main():
    while True:
        try:
            opcao = menu_principal()

            if opcao == "1":
                testar_conexao()
            elif opcao == "2":
                testar_deteccao()
            elif opcao == "3":
                testar_cadastro()
            elif opcao == "4":
                testar_busca()
            elif opcao == "5":
                testar_verificacao()
            elif opcao == "6":
                testar_exclusao()
            elif opcao == "7":
                monitorar_sensor()
            elif opcao == "0":
                print("\nEncerrando EduPonto.")
                break
            else:
                print("\nOpcao invalida.")
        except EOFError:
            print("\nEncerrando EduPonto.")
            break


if __name__ == "__main__":
    main()
