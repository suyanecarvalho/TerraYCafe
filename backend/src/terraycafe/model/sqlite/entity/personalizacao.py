from sqlalchemy import Column, ForeignKey,Integer

from terraycafe.model.sqlite.settings.connection import Base

class Personalizacao(Base):
    __tablename__ = "personalizacao"

    id= Column(Integer, nullable= False, primary_key=True)
    ingredientes_id = Column(Integer, ForeignKey('ingredientes.id'))
    item_pedido_id = Column(Integer, ForeignKey('item_pedido.id'))

    def __repr__(self) -> str:
        return f"<Personalizacao(id={self.id}, ingredientes_id={self.ingredientes_id}, item_pedido_id={self.item_pedido_id})>"