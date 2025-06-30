from sqlalchemy import Column, DateTime, Float, ForeignKey,Integer
from sqlalchemy import String


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

    # observers 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.observadores = []
        self.itens = kwargs.get('itens', [])

    def calcular_total(self):
        self.valor_total = sum(item.calcular_preco() for item in self.itens)
        return self.valor_total

    def aplicar_desconto(self, estrategia):
        desconto = estrategia.calcular_desconto(self)
        self.valor_total -= desconto

    def mudar_status(self):
        self.status = self.status.atualizar()
        self.notificar_observadores()

    def adicionar_observador(self, obs):
        self.observadores.append(obs)

    def notificar_observadores(self):
        for obs in self.observadores:
            obs.atualizar(self)
       