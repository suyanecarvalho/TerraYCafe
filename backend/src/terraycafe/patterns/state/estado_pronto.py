from terraycafe.patterns.state.estado_base import EstadoPedido
from terraycafe.patterns.state.estado_entregue import EntregueState


class ProntoState(EstadoPedido):
    async def proximo_estado(self, pedido):
        await pedido.set_estado(EntregueState())

    def get_nome(self):
        return "Pronto"