from sqlalchemy import Column,Integer
from sqlalchemy import String

from terraycafe.model.sqlite.settings.connection import Base

class Cliente(Base):
    __tablename__ = "cliente"

    id= Column(Integer, nullable= False, primary_key=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    pontos_fidelidade = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"<Cliente(id={self.id}, nome='{self.nome}', email='{self.email}', pontos={self.pontos_fidelidade})>"
