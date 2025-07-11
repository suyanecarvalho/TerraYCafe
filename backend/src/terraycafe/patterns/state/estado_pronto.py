from terraycafe.patterns.state.estado_base import EstadoPedido
from terraycafe.patterns.state.estado_entregue import EntregueState


class ProntoState(EstadoPedido):
    def proximo_estado(self, pedido):
        pedido.set_estado(EntregueState())

    def get_nome(self):
        return "Pronto"