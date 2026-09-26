from hardware.as608 import AS608, AS608Error


def identificar_digital(
    sensor: AS608,
    timeout: float = 20.0,
):
    """
    Captura uma digital e procura no banco interno do AS608.
    """
    try:
        print("Aguardando dedo...")
        sensor._esperar_dedo(timeout)

        sensor.capturar_imagem()
        sensor.converter_imagem(buffer=1)

        id_biometrico, confianca = sensor.buscar_digital()

        return {
            "encontrado": True,
            "id_biometrico": id_biometrico,
            "confianca": confianca,
        }

    except AS608Error as exc:
        mensagem = str(exc).lower()

        if "nao encontrada" in mensagem or "nao conferem" in mensagem:
            return {
                "encontrado": False,
                "id_biometrico": None,
                "confianca": 0,
            }

        raise
