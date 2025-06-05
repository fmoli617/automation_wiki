from datetime import datetime
import re
import pandas as pd


def dataframe_para_csv(data_frame: pd.DataFrame, caminho_arquivo: str, index: bool=False, sep: str=';', encoding: str='utf-8-sig'):
    """ """
    data_frame.to_csv(path_or_buf=caminho_arquivo, index=index, sep=sep, encoding=encoding)  

def csv_para_dataframe(caminho_arquivo: str, sep: str=';', encoding: str='utf-8-sig') -> pd.DataFrame:
    """ """
    return pd.read_csv(caminho_arquivo, sep=sep, encoding=encoding) 

def formatar_documento(texto: str):
    
    if texto == None or texto == '':
        return ''
    
    elif type(texto) == str:
        # se CNPJ
        if len(texto) > 11:
            documento = formatar_cnpj(texto)            
        # se CPF:
        else:
            documento = formatar_cpf(texto)

        return documento

def tratar_texto_com_documento(texto):
    """ """
    regex = r'\d+'
    numeros = re.findall(regex, texto)
    lista_strings = [re.sub(r'\D', '', numero) for numero in numeros]
    
    return  "".join(lista_strings) # Remover símbolos e manter apenas os dígitos
    
def extrair_valor_monetario(texto) -> float:
    
    # r'R\$\s*((\d{1,3}(?:\.\d{3})*|\d+),\d{2})'
    pattern = r'((\d{1,3}(?:\.\d{3})*|\d+),\d{2})'

    match = re.search(pattern, texto, flags= re.X)
    
    if match:
        
        valor = match.group(1).replace('.', '').replace(',', '.')
        return float(valor)
    
    else:
        return 0
    
def calcular_ano_vencimento(data_calculo_string, formato_data_calculo):
    datetime_calculo = datetime.strptime(data_calculo_string, formato_data_calculo)
    if datetime_calculo.year >= 2022:
        if datetime_calculo >= datetime(datetime_calculo.year,1,1,0,0,0) and datetime_calculo <= datetime(datetime_calculo.year,4,2,23,59,59):
            ano_vencimento = datetime_calculo.year + 1
        else:
            ano_vencimento = datetime_calculo.year + 2
    else:
        if datetime_calculo >= datetime(datetime_calculo.year,1,1,0,0,0) and datetime_calculo <= datetime(datetime_calculo.year,7,2,23,59,59):
            ano_vencimento = datetime_calculo.year + 1
        else:
            ano_vencimento = datetime_calculo.year + 2
    return str(ano_vencimento)

def manter_somente_numeros(texto):
    numeros = None
    if texto:
        numeros = re.sub(r'[^0-9]', '', texto)
    return numeros

def formatar_cpf(cpf):
    cpf = str(cpf)
    numeros_cpf = manter_somente_numeros(cpf)
    cpf_preenchido = numeros_cpf.zfill(11)
    return f'{cpf_preenchido[:3]}.{cpf_preenchido[3:6]}.{cpf_preenchido[6:9]}-{cpf_preenchido[9:11]}'

def formatar_cnpj(cnpj):
    cnpj = str(cnpj)
    numeros_cnpj = manter_somente_numeros(cnpj)
    cnpj_preenchido = numeros_cnpj.zfill(14)
    return f'{cnpj_preenchido[:2]}.{cnpj_preenchido[2:5]}.{cnpj_preenchido[5:8]}/{cnpj_preenchido[8:12]}-{cnpj_preenchido[12:14]}'