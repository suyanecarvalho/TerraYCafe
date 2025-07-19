class PedidoTempService:
    def __init__(self):
        self.itens_temp_por_cliente = {}

    def adicionar_bebida_temp(self, cliente_id: int, bebida: dict):
        if cliente_id not in self.itens_temp_por_cliente:
            self.itens_temp_por_cliente[cliente_id] = []
        self.itens_temp_por_cliente[cliente_id].append(bebida)

    def get_bebidas_temp(self, cliente_id: int) -> list[dict]:
        return self.itens_temp_por_cliente.get(cliente_id, [])

    def limpar_bebidas_temp(self, cliente_id: int):
        if cliente_id in self.itens_temp_por_cliente:
            del self.itens_temp_por_cliente[cliente_id]
