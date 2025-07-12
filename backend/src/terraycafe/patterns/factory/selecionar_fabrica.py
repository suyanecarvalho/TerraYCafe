from terraycafe.patterns.factory.fabricas import (
    CafeFactory, ChaPretoFactory, CappuccinoFactory, MochaFactory,
    LimonadaFactory, LatteFactory, AffogatoFactory, ChaMatteFactory,
    ChaHibiscoFactory, ExpressoFactory, CafeAmericanoFactory,
    MatchaLatteFactory, ChaHortelaFactory, ChaGeladoFactory,
    FrappucinoFactory, ChocolateQuenteFactory
)

def get_fabrica(nome: str):
    nome = nome.lower()

    match nome:
        case "cafe":
            return CafeFactory()
        case "cha preto":
            return ChaPretoFactory()
        case "cappuccino":
            return CappuccinoFactory()
        case "mocha":
            return MochaFactory()
        case "limonada":
            return LimonadaFactory()
        case "latte":
            return LatteFactory()
        case "affogato":
            return AffogatoFactory()
        case "cha matte":
            return ChaMatteFactory()
        case "cha hibisco":
            return ChaHibiscoFactory()
        case "expresso":
            return ExpressoFactory()
        case "cafe americano":
            return CafeAmericanoFactory()
        case "matcha latte":
            return MatchaLatteFactory()
        case "cha hortelã" | "cha hortela":
            return ChaHortelaFactory()
        case "cha gelado":
            return ChaGeladoFactory()
        case "frappucino":
            return FrappucinoFactory()
        case "chocolate quente":
            return ChocolateQuenteFactory()
        case _:
            raise ValueError(f"Bebida não reconhecida: {nome}")
