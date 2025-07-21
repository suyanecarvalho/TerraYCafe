from terraycafe.patterns.observer.observer import Observer

class CozinhaObserver(Observer):
    async def atualizar(self, pedido_id: int, novo_status: str):
        print(f"[COZINHA] Pedido {pedido_id} agora está em: {novo_status}")