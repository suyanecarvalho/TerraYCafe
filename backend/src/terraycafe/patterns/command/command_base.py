from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def executa(self) :
        pass

