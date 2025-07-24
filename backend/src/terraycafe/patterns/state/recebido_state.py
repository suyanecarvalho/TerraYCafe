from terraycafe.patterns.state.estado_base import EstadoPedido
from terraycafe.patterns.state.estado_em_preparo import EmPreparoState
from terraycafe.patterns. state.estado_cancelado import CanceladoState


class RecebidoState(EstadoPedido):
    async def proximo_estado(self, pedido):
        await pedido.set_estado(EmPreparoState())

    def get_nome(self):
        return "Recebido"