from terraycafe.patterns.observer.observer import Observer
from terraycafe.websocket.conexao import gerenciador_websocket

class WebSocketObserver(Observer):
    async def atualizar(self, pedido_id: int, novo_status: str):
        mensagem = {
            "tipo": "atualizacao_pedido",
            "id_pedido": pedido_id,
            "status": novo_status
        }
        # Envia para todos os clientes conectados
        await gerenciador_websocket.transmitir_para_todos(mensagem)