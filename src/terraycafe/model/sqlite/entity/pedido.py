from sqlalchemy import Column, DateTime, Float, ForeignKey,Integer
from sqlalchemy import String

from terraycafe.model.sql.settings.connection import Base

class Pedidos(Base):
    __tablename__ = "pedidos"

    id= Column(Integer, nullable= False, primary_key=True)
    status = Column(String(50), nullable=False)
    valor_total = Column(Float, nullable=False)
    forma_pagamento = Column(String(50), nullable=False)
    desconto = Column(Integer, nullable=False)
    data_hora = Column(DateTime, nullable=False)
    
    cliente_id = Column(Integer, ForeignKey('cliente.id'))

    def __repr__(self) -> str:
        return f"<Pedidos(id={self.id}, status='{self.status}', valor_total={self.valor_total}, forma_pagamento='{self.forma_pagamento}', desconto={self.desconto}, data_hora={self.data_hora}, cliente_id={self.cliente_id})>"
