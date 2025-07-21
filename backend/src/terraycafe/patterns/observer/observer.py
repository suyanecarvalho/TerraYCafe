from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    async def atualizar(self, pedido_id: int, novo_status: str):
        pass
