from sqlalchemy import Column, String, Integer, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from base import Base


class Extrato(Base):
    __tablename__ = 'tb_extrato_bancario'
    id = Column(Integer, primary_key=True)
    conta = Column(String)
    data_importacao = Column(Date)
    data_inicial = Column(Date)
    data_final = Column(Date)
    
    def __init__(self, conta, data_importacao, data_inicial, data_final):
        self.conta = conta
        self.data_importacao = data_importacao
        self.data_inicial = data_inicial
        self.data_final = data_final
    

class Lancamento(Base):
    __tablename__ = 'tb_lancamento_bancario'
    id = Column(Integer, primary_key=True)
    data = Column(Date)
    historico = Column(String)
    tipo_lancamento = Column(String)
    valor = Column(Numeric)
    categoria_lancamento = Column(String)
    detalhes = Column(String)
    estabelecimento = Column(String)
    id_extrato = Column(Integer, ForeignKey('tb_extrato_bancario.id'))
    extrato = relationship("Extrato", backref="tb_lancamento_bancario")

    def __init__(self, data, historico, valor, extrato):
        self.data = datetime.strptime(data, "%d/%m/%Y")
        self.historico = historico
        self.tipo_lancamento = 'C' if valor >= 0 else 'D'
        self.valor = abs(valor)
        self.categoria_lancamento = self.__extract_categoria(historico)
        self.detalhes = self.__extract_detalhes(historico, self.categoria_lancamento)
        self.estabelecimento = self.__extract_estabelecimento(historico, self.categoria_lancamento)
        self.extrato = extrato

    def __extract_categoria(self, historico):
        return historico[:historico.find(' - ')]

    def __extract_detalhes(self, historico, categoria_lancamento):
        return (historico[historico.find(' - ') + 3:]).strip()

    def __extract_estabelecimento(self, historico, categoria_lancamento):
        if categoria_lancamento == 'COMPRA CARTAO':
            return (historico[historico.find('no estabelecimento ') + 18:-1]).strip()
        elif categoria_lancamento == 'PAGAMENTO DE TITULO' or categoria_lancamento == 'RECARGA CELULAR':
            return self.detalhes
        else:
            return None
