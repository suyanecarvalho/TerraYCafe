from terraycafe.patterns.command.command_base import Command
from terraycafe.model.sqlite.BO.pedidoBO import PedidoBO

class AlterarPedido(Command):
    def __init__(self, bo: PedidoBO, id_pedido: int, novos_dados: dict):
        self.bo = bo
        self.id_pedido = id_pedido
        self.novos_dados = novos_dados
        self.backup_pedido = None
        
    def executar(self):
        """
        Executa a alteração do pedido
        """
        try:
            # Verificar se o pedido existe e pode ser alterado
            pedido = self.bo.buscar_pedido(self.id_pedido)
            if not pedido:
                raise ValueError("Pedido não encontrado.")
            
            if pedido.status != "Recebido":
                raise ValueError("Pedido não pode ser alterado após o preparo começar.")
            
            # Fazer backup dos dados atuais para possível desfazer
            self.backup_pedido = {
                "status": pedido.status,
                "valor_total": pedido.valor_total,
                "forma_pagamento": pedido.forma_pagamento,
                "desconto": pedido.desconto,
                "data_hora": pedido.data_hora,
                "Cliente_id": pedido.Cliente_id
            }
            
            # Executar a alteração
            pedido_alterado = self.bo.alterar_pedido(self.id_pedido, self.novos_dados)
            
            return {
                "success": True,
                "message": f"Pedido {self.id_pedido} alterado com sucesso",
                "pedido": {
                    "id": pedido_alterado.id,
                    "status": pedido_alterado.status,
                    "valor_total": pedido_alterado.valor_total,
                    "forma_pagamento": pedido_alterado.forma_pagamento,
                    "desconto": pedido_alterado.desconto,
                    "data_hora": pedido_alterado.data_hora
                }
            }
            
        except Exception as e:
            raise ValueError(f"Erro ao alterar pedido: {str(e)}")
    
    def desfazer(self):
        """
        Desfaz a alteração do pedido (se backup estiver disponível)
        """
        if self.backup_pedido is None:
            raise ValueError("Não há backup disponível para desfazer a operação.")
        
        try:
            # Restaurar dados do backup
            self.bo.alterar_pedido(self.id_pedido, self.backup_pedido)
            return {
                "success": True,
                "message": f"Alteração do pedido {self.id_pedido} foi desfeita"
            }
        except Exception as e:
            raise ValueError(f"Erro ao desfazer alteração: {str(e)}")