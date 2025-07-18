
from terraycafe.patterns.command.command_base import Command
from terraycafe.model.sqlite.BO.pedidoBO import PedidoBO


class CancelarPedido(Command):
    def __init__(self, bo:PedidoBO, dados_pedido: dict):
        self.bo = bo
        self.dados_pedido = dados_pedido
        self.id_pedido = None
    
    def executar(self):
        return self.bo.cancelar_pedido(self.dados_pedido)
        
    