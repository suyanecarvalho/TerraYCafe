from abc import ABC, abstractmethod

class EstadoPedido(ABC):
    @abstractmethod
    def proximo_estado(self, pedido):
        pass

    @abstractmethod
    def get_nome(self):
        pass