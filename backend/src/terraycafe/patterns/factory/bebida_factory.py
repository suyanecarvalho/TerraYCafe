from abc import ABC, abstractmethod
from terraycafe.model.sqlite.entity.bebida import Bebida

class BebidaFactory(ABC):
    @abstractmethod
    def criar_bebida(self) -> Bebida:
        pass
    
