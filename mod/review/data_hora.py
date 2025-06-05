from datetime import datetime
from dateutil.parser import parserinfo, parse, ParserError


FORMATO_DATA_AMERICANO = '%Y-%m-%d'
FORMATO_DATA_BRASIL = '%d/%m/%Y'
FORMATO_DATA_HORA_BRASIL = ''
FORMATO_DATA_UTC = '%Y-%m-%dT%H:%M:%S%z'
VERIFICACAO_ORDEM_DIA_ANO = [(True, False), (False, True), (False, False), (True, True)]


def obter_data_atual(formato_saida: str=FORMATO_DATA_AMERICANO) -> str:
    data_hora_atual = datetime.now()
    return data_hora_atual.strftime(formato_saida)


def obter_data_hora_atual(formato_saida: str='%Y-%m-%d %H:%M:%S') -> str:
    data_hora_atual = datetime.now()
    return data_hora_atual.strftime(formato_saida)


class ConversorDataCustomizado(parserinfo):
    parserinfo.JUMP = [
        " ", ".", ",", ";", "-", "/", "'", "\\",
        "at", "on", "and", "ad", "m", "t", "of",
        "st", "nd", "rd", "th", "de"
    ]
    parserinfo.MONTHS = [
        ("Jan", "Janeiro", "Jan", "January"),
        ("Fev", "Fevereiro", "Feb", "February"),
        ("Mar", "Março", "Mar", "March"),
        ("Abr", "Abril", "Apr", "April"),
        ("Mai", "Maio", "May", "May"),
        ("Jun", "Junho", "Jun", "June"),
        ("Jul", "Julho", "Jul", "July"),
        ("Ago", "Agosto", "Aug", "August"),
        ("Set", "Setembro", "Sep", "Sept", "September"),
        ("Out", "Outubro", "Oct", "October"),
        ("Nov", "Novembro", "Nov", "November"),
        ("Dez", "Dezembro", "Dec", "December")
    ]


def converter_data(texto_data: str, dia_primeiro: bool, ano_primeiro: bool) -> datetime | None:
    """Função auxiliar para converter string de data em datetime com inferência de formato.

    Args:
        texto_data (str): Texto representando uma data para ser convertido.
        dia_primeiro (bool): Auxiliar para distinguir datas confusas como 01/02/10. Caso o ano_primeiro seja True, diferencia entre YMD e YDM.
        ano_primeiro (bool): Auxiliar para distinguir datas confusas inferindo que o ano venha primeiro.

    Returns:
        datetime | None: Retorna um objeto datetime caso seja reconhecido um formato válido de data. Caso contrário, retorna None.
    """
    try:
        return parse(texto_data, parserinfo=ConversorDataCustomizado(), default=datetime(1900, 1, 1, 0, 0),
                    dayfirst=dia_primeiro, yearfirst=ano_primeiro, fuzzy=True)
    except ParserError:
        return


def formatar_string_data(texto_data: str, formato_saida: str = FORMATO_DATA_AMERICANO) -> str | None:
    for dia_primeiro, ano_primeiro in VERIFICACAO_ORDEM_DIA_ANO:
        datetime_origem = converter_data(texto_data, dia_primeiro, ano_primeiro)
        if datetime_origem is not None: return datetime_origem.strftime(formato_saida)


def obter_objeto_data_hora(texto_data: str, formato_origem: str | None = FORMATO_DATA_AMERICANO) -> datetime | None:
    if formato_origem is not None: return datetime.strptime(texto_data, formato_origem)
    for dia_primeiro, ano_primeiro in VERIFICACAO_ORDEM_DIA_ANO:
        datetime_origem = converter_data(texto_data, dia_primeiro, ano_primeiro)
        if datetime_origem is not None: return datetime_origem
