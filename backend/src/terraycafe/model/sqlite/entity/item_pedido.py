from sqlalchemy import Column,Float, ForeignKey,Integer
from terraycafe.model.sqlite.settings.connection import Base

class Item_pedido(Base):
    __tablename__ = "item_pedido"

    id= Column(Integer, primary_key=True, autoincrement=True)
    preco = Column(Float, nullable=False)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    bebida_id = Column(Integer, ForeignKey('bebida.id'))

    def __repr__(self) -> str:
        return f"<Item_pedido(id={self.id}, pedido_id={self.pedido_id}, preco={self.preco}, bebida_id={self.bebida_id})>"