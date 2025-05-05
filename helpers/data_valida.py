import re


def data_valida(data_str):
    padrao = r"^\d{2}/\d{2}/\d{4}$"
    if not re.match(padrao, data_str):
        return False

    try:
        dia, mes, ano = map(int, data_str.split("/"))
        from datetime import datetime

        datetime(ano, mes, dia)
        return True
    except ValueError:
        return False
