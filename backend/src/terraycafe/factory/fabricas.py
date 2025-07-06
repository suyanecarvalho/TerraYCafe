from src.terraycafe.factory.bebida_factory import BebidaFactory
from terraycafe.model.sqlite.entity.bebida import Cafe, ChaPreto, Cappuccino, Mocha, Limonada, Latte, Affogato, ChaMatte, ChaHibisco, Expresso, CafeAmericano, MatchaLatte, ChaHortela, ChaGelado, Frappucino, ChocolateQuente


class CafeFactory(BebidaFactory):
    def criar_bebida(self) -> Cafe:
        return Cafe()

class ChaPretoFactory(BebidaFactory):
    def criar_bebida(self) -> ChaPreto:
        return ChaPreto()
    
class CappuccinoFactory(BebidaFactory):
    def criar_bebida(self) -> Cappuccino:
        return Cappuccino()

class MochaFactory(BebidaFactory):
    def criar_bebida(self) -> Mocha:
        return Mocha()

class LimonadaFactory(BebidaFactory):
    def criar_bebida(self) -> Limonada:
        return Limonada()

class LatteFactory(BebidaFactory):
    def criar_bebida(self) -> Latte:
        return Latte()

class AffogatoFactory(BebidaFactory):
    def criar_bebida(self) -> Affogato:
        return Affogato()

class ChaMatteFactory(BebidaFactory):
    def criar_bebida(self) -> ChaMatte:
        return ChaMatte()

class ChaHibiscoFactory(BebidaFactory):
    def criar_bebida(self) -> ChaHibisco:
        return ChaHibisco()

class ExpressoFactory(BebidaFactory):
    def criar_bebida(self) -> Expresso:
        return Expresso()

class CafeAmericanoFactory(BebidaFactory):
    def criar_bebida(self) -> CafeAmericano:
        return CafeAmericano()
    
class MatchaLatteFactory(BebidaFactory):
    def criar_bebida(self) -> MatchaLatte:
        return MatchaLatte()
    
class ChaHortelaFactory(BebidaFactory):
    def criar_bebida(self) -> ChaHortela:
        return ChaHortela()
    
class ChaGeladoFactory(BebidaFactory):
    def criar_bebida(self) -> ChaGelado:
        return ChaGelado()

class FrappucinoFactory(BebidaFactory):
    def criar_bebida(self) -> Frappucino:
        return Frappucino()

class ChocolateQuenteFactory(BebidaFactory):
    def criar_bebida(self) -> ChocolateQuente:
        return ChocolateQuente()
    