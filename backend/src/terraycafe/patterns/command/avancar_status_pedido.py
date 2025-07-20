from terraycafe.patterns.command.command_base import Command
from terraycafe.model.sqlite.BO.pedidoBO import PedidoBO

class AvancarStatusPedido(Command):
    def __init__(self, bo: PedidoBO, pedido_id: int):
        self.bo = bo
        self.pedido_id = pedido_id

    async def executar(self):
        await self.bo.avancar_status(self.pedido_id)
