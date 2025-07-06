from abc import ABC, abstractmethod
from terraycafe.model.sqlite.entity.bebida import Bebida as BebidaDB
from terraycafe.model.sqlite.entity.ingredientes import Ingredientes as IngredienteDB

class BebidaComponent(ABC):
    @abstractmethod
    def get_descricao(self) -> str: ...
    @abstractmethod
    def get_preco(self) -> float: ...


## isso aqui é para fazer uma bebida simples virar decoravel 

class BebidaSimples(BebidaComponent):
    def __init__(self, bebida_db: BebidaDB):
        self._db = bebida_db

    def get_descricao(self) -> str:
        return self._db.nome

    def get_preco(self) -> float:
        return self._db.preco_base

class BebidaDecorator(BebidaComponent):
    def __init__(self, bebida: BebidaComponent):
        self._bebida = bebida

    def get_descricao(self) -> str:
        return self._bebida.get_descricao()

    def get_preco(self) -> float:
        return self._bebida.get_preco()

class IngredienteDecorator(BebidaDecorator):
    def __init__(self, bebida: BebidaComponent, ingrediente_db: IngredienteDB):
        super().__init__(bebida)
        self._ing = ingrediente_db

    def get_descricao(self) -> str:
        return f"{super().get_descricao()} + {self._ing.nome}"

    def get_preco(self) -> float:
        return super().get_preco() + self._ing.preco_adicional

def aplicar_personalizacoes(
    bebida_base: BebidaComponent,
    ingredientes_db: list[IngredienteDB],   
) -> BebidaComponent:
    bebida = bebida_base
    for ing in ingredientes_db:
        bebida = IngredienteDecorator(bebida, ing)
    return bebida
