from sqlalchemy import Column, DateTime, Float, ForeignKey,Integer
from sqlalchemy import String
from terraycafe.patterns.observer.ClienteObserver import ClienteObserver
from terraycafe.patterns.observer.CozinhaObserver import CozinhaObserver    

try:
    from terraycafe.model.sqlite.settings.connection import Base
except ImportError:
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()

class Pedidos(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, nullable=False, primary_key=True)
    status = Column(String(50), nullable=False)
    valor_total = Column(Float, nullable=False)
    forma_pagamento = Column(String(50), nullable=False)
    desconto = Column(Integer, nullable=False)
    data_hora = Column(DateTime, nullable=False)
    
    cliente_id = Column(Integer, ForeignKey('cliente.id'))

    def __repr__(self) -> str:
        return f"<Pedidos(id={self.id}, status='{self.status}', valor_total={self.valor_total}, forma_pagamento='{self.forma_pagamento}', desconto={self.desconto}, data_hora={self.data_hora}, cliente_id={self.cliente_id})>"

    def __init__(self, cliente_id, bebida):
        self.cliente_id = cliente_id
        self.bebida = bebida
        self.estado = RecebidoState()
        self.status = self.estado.get_nome()

    def set_estado(self, novo_estado):
        self.estado = novo_estado
        self.status = novo_estado.get_nome()

    def avancar_estado(self):
        self.estado.proximo_estado(self)

    def mudar_status(self, novo_status: str):
        self.status = novo_status
        self.notificar_observadores()

    def notificar_observadores(self):
        for obs in self.observadores:
            obs.atualizar(self.id, self.status)