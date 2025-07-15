from sqlalchemy import Column, Float,Integer
from sqlalchemy import String

from terraycafe.model.sqlite.settings.connection import Base

class Ingredientes(Base):
    __tablename__ = "ingredientes"

    id= Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    preco_adicional = Column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"<Ingredientes(id={self.id}, nome='{self.nome}', tipo='{self.tipo}', preco_adicional={self.preco_adicional})>"
