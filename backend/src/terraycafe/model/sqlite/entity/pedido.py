from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base
from terraycafe.patterns.state.recebido_state import RecebidoState
from terraycafe.model.sqlite.settings.connection import Base
from terraycafe.patterns.observer.cliente_observer import ClienteObserver   
from terraycafe.patterns.observer.cozinha_observer import CozinhaObserver

Base = declarative_base()

class Pedidos(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, nullable=False)
    status = Column(String(50), nullable=False)
    valor_total = Column(Float, nullable=False)
    forma_pagamento = Column(String(50), nullable=False)
    desconto = Column(Integer, nullable=False)
    data_hora = Column(DateTime, nullable=False)
    cliente_id = Column(Integer, ForeignKey('cliente.id'))

    
    def __repr__(self) -> str:
        return (
            f"<Pedidos(id={self.id}, status='{self.status}', valor_total={self.valor_total}, "
            f"forma_pagamento='{self.forma_pagamento}', desconto={self.desconto}, "
            f"data_hora={self.data_hora}, cliente_id={self.cliente_id})>"
        )

    def __init__(self, cliente_id, bebida):
        self.cliente_id = cliente_id
        self.bebida = bebida  
        self.estado = RecebidoState()
        self.status = self.estado.get_nome()
        self.observadores = []
        self.registrar_observadores()
        self.notificar_observadores()

    # Métodos de comportamento 
    def adicionar_observador(self, obs):
        if not hasattr(self, "observadores"):
            self.observadores = []
        self.observadores.append(obs)

    def notificar_observadores(self):
        if hasattr(self, "observadores"):
            for obs in self.observadores:
                obs.atualizar(self.id, self.status)
    
    def registrar_observadores(self):
        self.adicionar_observador(ClienteObserver())
        self.adicionar_observador(CozinhaObserver())

    def set_estado(self, novo_estado):
        self.estado = novo_estado
        self.status = self.estado.get_nome()
        self.notificar_observadores()

    def avancar_estado(self):
        self.estado.proximo_estado(self)
        self.status = self.estado.get_nome()
        self.notificar_observadores()

