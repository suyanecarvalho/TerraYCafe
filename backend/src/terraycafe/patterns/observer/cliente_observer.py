from terraycafe.patterns.observer.observer import Observer

class ClienteObserver(Observer):
    def atualizar(self, pedido_id: int, novo_status: str):
        print(f"[CLIENTE] Pedido {pedido_id} mudou para: {novo_status}")