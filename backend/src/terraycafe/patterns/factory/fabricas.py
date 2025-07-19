from terraycafe.patterns.factory.bebida_factory import BebidaFactory
from terraycafe.model.sqlite.entity.bebida import (
    Cafe, ChaPreto, Cappuccino, Mocha, Limonada, Latte, Affogato,
    ChaMatte, ChaHibisco, Expresso, CafeAmericano, MatchaLatte,
    ChaHortela, ChaGelado, Frappucino, ChocolateQuente
)

class CafeFactory(BebidaFactory):
    def criar_bebida(self) -> Cafe:
        return Cafe("Café", "Café tradicional", 5.0)
    
    def info_bebida(self):
        return {
            "nome": "Café",
            "descricao": "Café tradicional",
            "preco_base": 5.0
        }

class ChaPretoFactory(BebidaFactory):
    def criar_bebida(self) -> ChaPreto:
        return ChaPreto("Chá Preto", "Chá preto tradicional", 4.0)
    
    def info_bebida(self):
        return {
            "nome": "Chá Preto",
            "descricao": "Chá preto tradicional",
            "preco_base": 4.0
        }

class CappuccinoFactory(BebidaFactory):
    def criar_bebida(self) -> Cappuccino:
        return Cappuccino("Cappuccino", "Cappuccino cremoso", 6.0)
    
    def info_bebida(self):
        return {
            "nome": "Cappuccino",
            "descricao": "Cappuccino cremoso",
            "preco_base": 6.0
        }

class MochaFactory(BebidaFactory):
    def criar_bebida(self) -> Mocha:
        return Mocha("Mocha", "Café com chocolate", 6.5)

    def info_bebida(self):
        return {
            "nome": "Mocha",
            "descricao": "Café com chocolate",
            "preco_base": 6.5
        }

class LimonadaFactory(BebidaFactory):
    def criar_bebida(self) -> Limonada:
        return Limonada("Limonada", "Limonada refrescante que realmente merecia um grammy", 4.5)

    def info_bebida(self):
        return {
            "nome": "Limonada",
            "descricao": "Limonada refrescante que realmente merecia um grammy",
            "preco_base": 4.5
        }

class LatteFactory(BebidaFactory):
    def criar_bebida(self) -> Latte:
        return Latte("Latte", "Café com leite vaporizado", 6.0)

    def info_bebida(self):
        return {
            "nome": "Latte",
            "descricao": "Café com leite vaporizado",
            "preco_base": 6.0
        }

class AffogatoFactory(BebidaFactory):
    def criar_bebida(self) -> Affogato:
        return Affogato("Affogato", "Café com sorvete", 7.0)

    def info_bebida(self):
        return {
            "nome": "Affogato",
            "descricao": "Café com sorvete",
            "preco_base": 7.0
        }

class ChaMatteFactory(BebidaFactory):
    def criar_bebida(self) -> ChaMatte:
        return ChaMatte("Chá Matte", "Chá mate gelado", 4.5)

    def info_bebida(self):
        return {
            "nome": "Chá Matte",
            "descricao": "Chá mate gelado",
            "preco_base": 4.5
        }

class ChaHibiscoFactory(BebidaFactory):
    def criar_bebida(self) -> ChaHibisco:
        return ChaHibisco("Chá de Hibisco", "Chá de hibisco natural", 5.0)

    def info_bebida(self):
        return {
            "nome": "Chá de Hibisco",
            "descricao": "Chá de hibisco natural",
            "preco_base": 5.0
        }

class ExpressoFactory(BebidaFactory):
    def criar_bebida(self) -> Expresso:
        return Expresso("Expresso", "Say you can't sleep, baby, I know that's that me espresso. Café expresso curto", 4.0)

    def info_bebida(self):
        return {
            "nome": "Expresso",
            "descricao": "Say you can't sleep, baby, I know that's that me espresso. Café expresso curto",
            "preco_base": 4.0
        }

class CafeAmericanoFactory(BebidaFactory):
    def criar_bebida(self) -> CafeAmericano:
        return CafeAmericano("Café Americano", "there's nothing like this Miss Americana. Café expresso com água", 4.5)
    
    def info_bebida(self):
        return {
            "nome": "Café Americano",   
            "descricao": "there's nothing like this Miss Americana. Café expresso com água",
            "preco_base": 4.5
        }

class MatchaLatteFactory(BebidaFactory):
    def criar_bebida(self) -> MatchaLatte:
        return MatchaLatte("Matcha Latte", "Chá verde com leite", 7.0)
    
    def info_bebida(self):
        return {
            "nome": "Matcha Latte",
            "descricao": "Chá verde com leite",
            "preco_base": 7.0
        }

class ChaHortelaFactory(BebidaFactory):
    def criar_bebida(self) -> ChaHortela:
        return ChaHortela("Chá de Hortelã", "Chá de hortelã fresco", 4.5)
    
    def info_bebida(self):
        return {
            "nome": "Chá de Hortelã",
            "descricao": "Chá de hortelã fresco",
            "preco_base": 4.5
        }

class ChaGeladoFactory(BebidaFactory):
    def criar_bebida(self) -> ChaGelado:
        return ChaGelado("Chá Gelado", "Chá gelado com limão", 4.5)
    
    def info_bebida(self):
        return {
            "nome": "Chá Gelado",
            "descricao": "Chá gelado com limão",
            "preco_base": 4.5
        }

class FrappucinoFactory(BebidaFactory):
    def criar_bebida(self) -> Frappucino:
        return Frappucino("Frappucino", "Bebida gelada de café", 8.0)
    
    def info_bebida(self):
        return {
            "nome": "Frappucino",
            "descricao": "Bebida gelada de café",
            "preco_base": 8.0
        }

class ChocolateQuenteFactory(BebidaFactory):
    def criar_bebida(self) -> ChocolateQuente:
        return ChocolateQuente("Chocolate Quente", "Chocolate quente cremoso", 7.0)
    
    def info_bebida(self):
        return {
            "nome": "Chocolate Quente",
            "descricao": "Chocolate quente cremoso",
            "preco_base": 7.0
        }

_fabricas = {
    "Cafe": CafeFactory(),
    "ChaPreto": ChaPretoFactory(),
    "Cappuccino": CappuccinoFactory(),
    "Mocha": MochaFactory(),
    "Limonada": LimonadaFactory(),
    "Latte": LatteFactory(),
    "Affogato": AffogatoFactory(),
    "ChaMatte": ChaMatteFactory(),
    "ChaHibisco": ChaHibiscoFactory(),
    "Expresso": ExpressoFactory(),
    "CafeAmericano": CafeAmericanoFactory(),
    "MatchaLatte": MatchaLatteFactory(),
    "ChaHortela": ChaHortelaFactory(),
    "ChaGelado": ChaGeladoFactory(),
    "Frappucino": FrappucinoFactory(),
    "ChocolateQuente": ChocolateQuenteFactory(),
}

def get_fabrica(tipo: str) -> BebidaFactory | None:
    return _fabricas.get(tipo)

def listar_tipos_bebidas_disponiveis() -> list[str]:
    return list(_fabricas.keys())
