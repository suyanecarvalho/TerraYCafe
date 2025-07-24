from terraycafe.patterns.state.estado_base import EstadoPedido

class EntregueState(EstadoPedido):
    def proximo_estado(self, pedido):
        print("Pedido já foi entregue. Nenhuma transição possível.")

    def get_nome(self):
        return "Entregue"