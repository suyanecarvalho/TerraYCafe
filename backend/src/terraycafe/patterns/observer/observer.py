from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def atualizar(self, pedido_id: int, novo_status: str):
        pass
