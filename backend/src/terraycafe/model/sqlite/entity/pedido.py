from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import reconstructor
from terraycafe.patterns.state.estado_em_preparo import EmPreparoState
from terraycafe.patterns.state.recebido_state import RecebidoState
from terraycafe.model.sqlite.settings.connection import Base
from terraycafe.patterns.observer.cliente_observer import ClienteObserver
from terraycafe.patterns.observer.cozinha_observer import CozinhaObserver


class Pedidos(Base):
    __tablename__ = "pedidos"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(50), nullable=False)
    valor_total = Column(Float, nullable=False)
    forma_pagamento = Column(String(50), nullable=False)
    desconto = Column(Integer, nullable=False)
    data_hora = Column(DateTime, nullable=False)
    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Inicializa o estado como RecebidoState ou conforme o status
            self.estado = RecebidoState()
            
    @reconstructor
    def init_on_load(self):
        # Inicializa o estado conforme o status do pedido
        if self.status == "Recebido":
            self.estado = RecebidoState()
        # Adicione outros estados conforme necessário
        elif self.status == "Em Preparo":
            self.estado = EmPreparoState()
        else:
            self.estado = RecebidoState()
            
    def __repr__(self) -> str:
        return (
            f"<Pedidos(id={self.id}, status='{self.status}', valor_total={self.valor_total}, "
            f"forma_pagamento='{self.forma_pagamento}', desconto={self.desconto}, "
            f"data_hora={self.data_hora}, cliente_id={self.cliente_id})>"
        )
    
    # Métodos de comportamento 
    def adicionar_observador(self, obs):
        if not hasattr(self, "observadores"):
            self.observadores = []
        self.observadores.append(obs)

    async def notificar_observadores(self, pedido_id=None, status=None):
        if hasattr(self, "observadores"):
            for obs in self.observadores:
                await obs.atualizar(pedido_id or self.id, status or self.status)

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


