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
class Cafe(Bebida):
    def __init__(self):
        super().__init__(nome="Café", descricao="Café tradicional", categoria="Café", preco_base=5.0)

class ChaPreto(Bebida):
    def __init__(self):
        super().__init__(nome="Chá Preto", descricao="Chá preto tradicional", categoria="Chá", preco_base=4.0)

class Cappuccino(Bebida):
    def __init__(self):
        super().__init__(nome="Cappuccino", descricao="Cappuccino cremoso", categoria="Cappuccino", preco_base=6.0)

class Mocha(Bebida):
    def __init__(self):
        super().__init__(nome="Mocha", descricao="Café com chocolate", categoria="Mocha", preco_base=6.5)

class Limonada(Bebida):
    def __init__(self):
        super().__init__(nome="Limonada", descricao="Limonada refrescante que realmente merecia um grammy", categoria="Limonada", preco_base=4.5)

class Latte(Bebida):
    def __init__(self):
        super().__init__(nome="Latte", descricao="Café com leite vaporizado", categoria="Latte", preco_base=6.0)

class Affogato(Bebida):
    def __init__(self):
        super().__init__(nome="Affogato", descricao="Café com sorvete", categoria="Affogato", preco_base=7.0)

class ChaMatte(Bebida):
    def __init__(self):
        super().__init__(nome="Chá Matte", descricao="Chá mate gelado", categoria="Chá", preco_base=4.5)

class ChaHibisco(Bebida):
    def __init__(self):
        super().__init__(nome="Chá de Hibisco", descricao="Chá de hibisco natural", categoria="Chá", preco_base=5.0)

class Expresso(Bebida):
    def __init__(self):
        super().__init__(nome="Expresso", descricao="Say you can't sleep, baby, I know that's that me espresso. Café expresso curto", categoria="Café", preco_base=4.0)

class CafeAmericano(Bebida):
    def __init__(self):
        super().__init__(nome="Café Americano", descricao="there's nothing like this Miss Americana. Café expresso com água", categoria="Café", preco_base=4.5)

class MatchaLatte(Bebida):
    def __init__(self):
        super().__init__(nome="Matcha Latte", descricao="Chá verde com leite", categoria="Chá", preco_base=7.0)

class ChaHortela(Bebida):
    def __init__(self):
        super().__init__(nome="Chá de Hortelã", descricao="Chá de hortelã fresco", categoria="Chá", preco_base=4.5)

class ChaGelado(Bebida):
    def __init__(self):
        super().__init__(nome="Chá Gelado", descricao="Chá gelado com limão", categoria="Chá", preco_base=4.5)

class Frappucino(Bebida):
    def __init__(self):
        super().__init__(nome="Frappucino", descricao="Bebida gelada de café", categoria="Café", preco_base=8.0)

class ChocolateQuente(Bebida):
    def __init__(self):
        super().__init__(nome="Chocolate Quente", descricao="Chocolate quente cremoso", categoria="Chocolate Quente", preco_base=7.0)