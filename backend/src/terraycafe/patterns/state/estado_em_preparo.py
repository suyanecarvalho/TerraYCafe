from terraycafe.patterns.state.estado_base import EstadoPedido
from terraycafe.patterns.state.estado_pronto import ProntoState
from terraycafe.patterns. state.estado_cancelado import CanceladoState


class EmPreparoState(EstadoPedido):
    def proximo_estado(self, pedido):
        pedido.set_estado(ProntoState())

    def get_nome(self):
        return "Em Preparo"