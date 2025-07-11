from abc import AbC, abstractmethod

#classe que define a interface de estrategias de desconto(que sao iguais p todos)
class DescontoStrategy(AbC):
    @abstractmethod
    def calcular_desconto(self, valor: float) -> float:
        pass
    def get_descricao(self,) -> str:
        pass

# classes concretas que implementam de fato cada estrategias de desconto
class DescontoFidelidade(DescontoStrategy):
    def calcular_desconto(self, valor: float) -> float:
        return valor * 0.10
    def get_descricao(self):
        return "Desconto de 10%"

class DescontoPix(DescontoStrategy):
    def calcular_desconto(self, valor: float) -> float:
        return valor * 0.05
    def get_descricao(self):
        return "Desconto de 5% para PIX"
    
class SemDesconto(DescontoStrategy):
    def calcular_desconto(self, valor: float) -> float:
        return 0.0
    def get_descricao(self):
        return "Sem desconto"

        