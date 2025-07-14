from sqlalchemy import Column, Float, Integer, String
from terraycafe.model.sqlite.settings.connection import Base

class Bebida(Base):
    __tablename__ = "bebida"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=False)
    categoria = Column(String(255), nullable=False)
    preco_base = Column(Float, nullable=False)

    def __init__(self, nome, descricao, categoria, preco_base):
        self.nome = nome
        self.descricao = descricao
        self.categoria = categoria
        self.preco_base = preco_base

    def __repr__(self) -> str:
        return f"<Bebida(id={self.id}, nome='{self.nome}', descricao='{self.descricao}', categoria='{self.categoria}', preco_base={self.preco_base})>"
    
    def get_nome(self):
        return self.nome

    def get_descricao(self):
        return self.descricao

    def get_categoria(self):
        return self.categoria

    def get_preco(self):
        return self.preco_base

class Cafe(Bebida):
    @classmethod
    def criar(cls):
        return cls(nome="Café", descricao="Café tradicional", categoria="Café", preco_base=5.0)

class ChaPreto(Bebida):
    @classmethod
    def criar(cls):
        return cls(nome="Chá Preto", descricao="Chá preto tradicional", categoria="Chá", preco_base=4.0)

class Cappuccino(Bebida):
    @classmethod
    def criar(cls):
        return cls(nome="Cappuccino", descricao="Cappuccino cremoso", categoria="Cappuccino", preco_base=6.0)

class Mocha(Bebida):
    @classmethod
    def criar(cls):
        return cls(nome="Mocha", descricao="Café com chocolate", categoria="Mocha", preco_base=6.5)

class Limonada(Bebida):
    @classmethod
    def criar(cls):
        return cls(nome="Limonada", descricao="Limonada refrescante que realmente merecia um grammy", categoria="Limonada", preco_base=4.5)

class Latte(Bebida):
    @classmethod
    def criar(cls):
        return cls(nome="Latte", descricao="Café com leite vaporizado", categoria="Latte", preco_base=6.0)

class Affogato(Bebida):
    @classmethod
    def criar(cls):
        return cls(nome="Affogato", descricao="Café com sorvete", categoria="Affogato", preco_base=7.0)

class ChaMatte(Bebida):
    @classmethod
    def criar(cls):
        return cls(nome="Chá Matte", descricao="Chá mate gelado", categoria="Chá", preco_base=4.5)

class ChaHibisco(Bebida):
    @classmethod
    def criar(cls):
        return cls(nome="Chá de Hibisco", descricao="Chá de hibisco natural", categoria="Chá", preco_base=5.0)

class Expresso(Bebida):
    @classmethod
    def criar(cls):
        return cls(nome="Expresso", descricao="Say you can't sleep, baby, I know that's that me espresso. Café expresso curto", categoria="Café", preco_base=4.0)

class CafeAmericano(Bebida):
    @classmethod
    def criar(cls):
        return cls(nome="Café Americano", descricao="there's nothing like this Miss Americana. Café expresso com água", categoria="Café", preco_base=4.5)

class MatchaLatte(Bebida):
    @classmethod
    def criar(cls):
        return cls(nome="Matcha Latte", descricao="Chá verde com leite", categoria="Chá", preco_base=7.0)

class ChaHortela(Bebida):
    @classmethod
    def criar(cls):
        return cls(nome="Chá de Hortelã", descricao="Chá de hortelã fresco", categoria="Chá", preco_base=4.5)

class ChaGelado(Bebida):
    @classmethod
    def criar(cls):
        return cls(nome="Chá Gelado", descricao="Chá gelado com limão", categoria="Chá", preco_base=4.5)

class Frappucino(Bebida):
    @classmethod
    def criar(cls):
        return cls(nome="Frappucino", descricao="Bebida gelada de café", categoria="Café", preco_base=8.0)

class ChocolateQuente(Bebida):
    @classmethod
    def criar(cls):
        return cls(nome="Chocolate Quente", descricao="Chocolate quente cremoso", categoria="Chocolate Quente", preco_base=7.0)
