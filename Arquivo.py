import pandas as pd
import MovimentacaoBancaria as mb
from datetime import date, datetime

from base import Session, engine, Base

# Tratamento da string para retirada do "R$" e converção para tipo numérico
def __valor_str_to_float(str_valor):
    str_valor = str_valor.replace(' R$ ', '')
    str_valor = str_valor.replace('.', '')
    str_valor = str_valor.replace(',', '.')
    return float(str_valor)

# Busca pelos dados contidos no cabeçalho do CSV
def __tratar_cabecalho(nome_arquivo, encoding='ISO-8859-1'):
    with open(nome_arquivo, 'r', encoding=encoding) as arquivo:
        linhas = arquivo.read().splitlines(True)
        conta = linhas[1].replace('\n', '').split(sep=';')[1]
        datas = linhas[2].replace('\n', '').split(sep=';')
        data_ini, data_fim = datas[1], datas[2]
        return conta, data_ini, data_fim


def importar_arquivo(nome_arquivo, encoding='ISO-8859-1'):
    conta, data_inicial, data_final = __tratar_cabecalho(nome_arquivo, encoding)
    ext = mb.Extrato(conta, date.today(), datetime.strptime(data_inicial, "%d/%m/%Y"), datetime.strptime(data_final, "%d/%m/%Y"))

    Base.metadata.create_all(engine)
    session = Session()

    session.add(ext)

    extrato = pd.read_csv(nome_arquivo, sep=';', encoding=encoding, header=6)
    extrato.apply(lambda row: session.add(mb.Lancamento(row['DATA LANÇAMENTO'], row['HISTÓRICO'], __valor_str_to_float(row['VALOR']), ext)), axis=1)

    session.commit()
    session.close()

    return ext
