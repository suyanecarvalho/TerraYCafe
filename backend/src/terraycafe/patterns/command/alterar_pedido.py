from backend.src.terraycafe.patterns.command.command_base import Command
from backend.src.terraycafe.model.sqlite.BO.pedidoBO import PedidoBO


class AlterarPedido(Command):
    def __init__(self, bo:PedidoBO, id_pedido: int, novos_dados: dict):
        self.bo = bo
        self.id_pedido = id_pedido
        self.novos_dados = novos_dados
        
    
    def executa(self):
        #Trazer logica de status do pedido
        pedido= self.bo.buscar_pedido(self.id_pedido)
        if pedido.estado != "RECEBIDO":
            raise ValueError("Pedido não pode ser alterado após o preparo começar.")

        self.backup_pedido = pedido.copy()  # Supondo que o BO tenha um método para backup ou cópia
        return self.pedido_bo.alterar_pedido(self.id_pedido, self.novos_dados)