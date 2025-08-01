from terraycafe.patterns.command.command_base import Command
from terraycafe.model.sqlite.BO.pedidoBO import PedidoBO

class FazerPedido(Command):
    def __init__(self, bo:PedidoBO, dados_pedido: dict):
        self.bo = bo
        self.dados_pedido = dados_pedido
        self.id_pedido = None
    
    def executar(self):
        self.id_pedido = self.bo.finalizar_pedido(self.dados_pedido)
        return self.id_pedido
        
