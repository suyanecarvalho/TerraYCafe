from terraycafe.model.sqlite.entity.bebida import Bebida

class BebidaDecorator(Bebida):
    def __init__(self, bebida: Bebida):
        self._bebida = bebida
    def get_descricao(self) -> str:
        return self._bebida.get_descricao()
    def get_preco(self) -> float:
        return self._bebida.get_preco()
