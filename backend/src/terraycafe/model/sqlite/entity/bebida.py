from sqlalchemy import Column, Float,Integer
from sqlalchemy import String

from terraycafe.model.sqlite.settings.connection import Base

class Bebida(Base):
    __tablename__ = "bebida"

    id= Column(Integer, nullable= False, primary_key=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=False)
    categoria = Column(String(255), nullable=False)
    preco_base = Column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"<Bebida(id={self.id}, nome='{self.nome}', descricao='{self.descricao}', categoria='{self.categoria}', preco_base={self.preco_base})>"
