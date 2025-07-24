from terraycafe.patterns.state.estado_base import EstadoPedido

class CanceladoState(EstadoPedido):
    def proximo_estado(self, pedido):
        print("Pedido cancelado. Nenhuma transição possível.")

    def get_nome(self):
        return "Cancelado"