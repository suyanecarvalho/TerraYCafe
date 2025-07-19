from sqlalchemy import Column, Float, Integer, String
from terraycafe.model.sqlite.settings.connection import Base

class Bebida(Base):
    __tablename__ = "bebida"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=False)
    preco_base = Column(Float, nullable=False)

    def __init__(self, nome, descricao, preco_base):
        self.nome = nome
        self.descricao = descricao
        self.preco_base = preco_base

    def __repr__(self) -> str:
        return f"<Bebida(id={self.id}, nome='{self.nome}', descricao='{self.descricao}', preco_base={self.preco_base})>"
    
    def get_nome(self):
        return self.nome

    def get_descricao(self):
        return self.descricao

    def get_preco(self):
        return self.preco_base

# Classes específicas de bebida para o padrão Factory
class Cafe(Bebida):
    def __init__(self, nome="Café tradicional", descricao="Café tradicional", preco_base=5.0):
        super().__init__(nome, descricao, preco_base)

class ChaPreto(Bebida):
    def __init__(self, nome="Chá Preto", descricao="Chá preto tradicional",  preco_base=4.0):
        super().__init__(nome, descricao,  preco_base)

class Cappuccino(Bebida):
    def __init__(self, nome="Cappuccino", descricao="Cappuccino cremoso",  preco_base=6.0):
        super().__init__(nome, descricao,  preco_base)

class Mocha(Bebida):
    def __init__(self, nome="Mocha", descricao="Café com chocolate",  preco_base=6.5):
        super().__init__(nome, descricao,  preco_base)

class Limonada(Bebida):
    def __init__(self, nome="Limonada", descricao="Limonada refrescante que realmente merecia um grammy",  preco_base=4.5):
        super().__init__(nome, descricao,  preco_base)

class Latte(Bebida):
    def __init__(self, nome="Latte", descricao="Café com leite vaporizado",  preco_base=6.0):
        super().__init__(nome, descricao,  preco_base)

class Affogato(Bebida):
    def __init__(self, nome="Affogato", descricao="Café com sorvete",  preco_base=7.0):
        super().__init__(nome, descricao,  preco_base)

class ChaMatte(Bebida):
    def __init__(self, nome="Chá Matte", descricao="Chá mate gelado",  preco_base=4.5):
        super().__init__(nome, descricao,  preco_base)

class ChaHibisco(Bebida):
    def __init__(self, nome="Chá de Hibisco", descricao="Chá de hibisco natural",  preco_base=5.0):
        super().__init__(nome, descricao,  preco_base)

class Expresso(Bebida):
    def __init__(self, nome="Expresso", descricao="Say you can't sleep, baby, I know that's that me espresso. Café expresso curto",  preco_base=4.0):
        super().__init__(nome, descricao,  preco_base)

class CafeAmericano(Bebida):
    def __init__(self, nome="Café Americano", descricao="there's nothing like this Miss Americana. Café expresso com água",  preco_base=4.5):
        super().__init__(nome, descricao,  preco_base)

class MatchaLatte(Bebida):
    def __init__(self, nome="Matcha Latte", descricao="Chá verde com leite",  preco_base=7.0):
        super().__init__(nome, descricao,  preco_base)

class ChaHortela(Bebida):
    def __init__(self, nome="Chá de Hortelã", descricao="Chá de hortelã fresco",  preco_base=4.5):
        super().__init__(nome, descricao,  preco_base)

class ChaGelado(Bebida):
    def __init__(self, nome="Chá Gelado", descricao="Chá gelado com limão",  preco_base=4.5):
        super().__init__(nome, descricao,  preco_base)

class Frappucino(Bebida):
    def __init__(self, nome="Frappucino", descricao="Bebida gelada de café",  preco_base=8.0):
        super().__init__(nome, descricao,  preco_base)

class ChocolateQuente(Bebida):
    def __init__(self, nome="Chocolate Quente", descricao="Chocolate quente cremoso",  preco_base=7.0):
        super().__init__(nome, descricao,  preco_base)
