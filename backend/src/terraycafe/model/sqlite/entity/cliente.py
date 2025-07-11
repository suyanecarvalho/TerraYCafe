from sqlalchemy import Column,Integer
from sqlalchemy import String

from terraycafe.model.sqlite.settings.connection import Base

class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    telefone = Column(String(255), nullable=True) 
    senha = Column(String(255), nullable=True)     
    pontos_fidelidade = Column(Integer, nullable=False, default=0)

    def __repr__(self) -> str:
        return f"<Cliente(id={self.id}, nome='{self.nome}', email='{self.email}', telefone='{self.telefone}',senha='{self.senha}', pontos={self.pontos_fidelidade})>"
