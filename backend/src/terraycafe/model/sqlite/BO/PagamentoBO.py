from terraycafe.patterns.strategy import desconto_strategy
from terraycafe.patterns.strategy.desconto_strategy import DescontoFidelidade,DescontoPix,SemDesconto

#interface de interacao com o cliente
class PagamentoContext:
    def __init__(self,tipo_pagamento: str):
        self.strategy= self._definir_estrategia(tipo_pagamento)
        
    def _definir_estrategia(self, tipo_pag: str):
        tipo_pag = tipo_pag.lower()
        if tipo_pag == "fidelidade" or tipo_pag == "voucher":
            return DescontoFidelidade()
        elif tipo_pag == "pix":
            return DescontoPix()
        elif tipo_pag == "debito":
            return SemDesconto()
        elif tipo_pag == "credito":
            return SemDesconto()
        else:
            return SemDesconto()       
    
    def processar_pagamento(self, valor: float) :        
        desconto = self.strategy.calcular_desconto(valor)
        valor_final = valor - desconto
        return {"valor":valor,
                "tipo_pagamento": self.strategy.get_descricao(),
                "desconto": desconto, 
                "valor_final": valor_final}