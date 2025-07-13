from datetime import datetime
from terraycafe.patterns.factory.selecionar_fabrica import get_fabrica
from terraycafe.patterns.decorator.decorator import BebidaDecorator, aplicar_personalizacoes
from terraycafe.model.sqlite.entity.pedido import Pedidos
from terraycafe.model.sqlite.BO.PagamentoBO import PagamentoContext
from terraycafe.model.sqlite.DAO.pedidoDAO import PedidoDAO
from terraycafe.patterns.state.estado_cancelado import CanceladoState
from terraycafe.model.sqlite.DAO.bebidaDAO import BebidaDAO
from terraycafe.model.sqlite.DAO.item_pedidoDAO import ItemPedidoDAO
from terraycafe.model.sqlite.DAO.personalizacaoDAO import PersonalizacaoDAO


class PedidoBO: 
    def __init__(self, db_connection):
        self.dao = PedidoDAO(db_connection)
        self.bebida_dao = BebidaDAO(db_connection)
        self.item_pedido_dao = ItemPedidoDAO(db_connection)
        self.personalizacao_dao = PersonalizacaoDAO(db_connection)

    def criar_pedido(self, cliente_id: int, itens: list[dict], forma_pagamento: str) -> Pedidos:
        try:
            pedido = Pedidos(
                status="Recebido",
                valor_total=0.0,
                forma_pagamento=forma_pagamento,
                desconto=0,
                data_hora=datetime.now(),
                Cliente_id=cliente_id
            )
            self.dao.salvar(pedido)

            itens_criados = []
            valor_bruto_total = 0.0

            # Criar e personalizar bebidas
            for item in itens:
                tipo = item["tipo_bebida"]
                ingrs = item.get("ingredientes", [])

                fabrica = get_fabrica(tipo)
                if not fabrica:
                    raise ValueError(f"Tipo de bebida inválido: {tipo}")

                bebida = fabrica.criar_bebida()
                bebida_personalizada = aplicar_personalizacoes(bebida, ingrs)

                preco_item = bebida_personalizada.get_preco()
                valor_bruto_total += preco_item

                itens_criados.append({
                    "bebida_personalizada": bebida_personalizada,
                    "ingredientes": ingrs,
                    "preco_item": preco_item
                })

            pagamento = PagamentoContext(forma_pagamento)
            resultado_pagamento = pagamento.processar_pagamento(valor_bruto_total)
            pedido.valor_total = resultado_pagamento["valor_final"]
            pedido.desconto = int(resultado_pagamento["desconto"])
            pedido.forma_pagamento = resultado_pagamento["tipo_pagamento"]

            for item in itens_criados:
                bebida_personalizada = item["bebida_personalizada"]
                ingrs = item["ingredientes"]
                preco = item["preco_item"]

                bebida = self.bebida_dao.insert_bebida(
                    nome =  bebida_personalizada.get_nome(),
                    descricao=bebida_personalizada.get_descricao(),
                    preco_base=preco,
                    categoria=bebida_personalizada.get_categoria()
                )

                self.item_pedido_dao.insert_item_pedido(
                    pedido_id=pedido.id,
                    preco=preco,
                    bebida_id=bebida.id
                )

                item_pedido = self.item_pedido_dao.get_ultimo_item_pedido()

                for ingrediente_id in ingrs:
                    self.personalizacao_dao.insert_personalizacao(
                        item_pedido_id=item_pedido.id,
                        ingredientes_id=ingrediente_id
                    )

            pedido.registrar_observadores()
            pedido.notificar_observadores()

            return pedido

        except Exception as e:
            print(f"[PedidoBO] Erro ao criar pedido: {e}")
            raise


    def avancar_status(self, pedido_id: int):
        pedido = self.dao.buscar_por_id(pedido_id)
        if pedido:
            pedido.avancar_estado()
            self.dao.atualizar(pedido.id, pedido.status)
            pedido.notificar_observadores()
    
    def cancelar_pedido(self, pedido_id: int):
        pedido = self.dao.buscar_por_id(pedido_id)
        if not pedido:
            print("Pedido não encontrado.")
            return

        if pedido.status != "Recebido":
            print("Só é possível cancelar pedidos no estado 'Recebido'.")
            return

        pedido.set_estado(CanceladoState())
        self.dao.atualizar(pedido.id,pedido.status)
        pedido.notificar_observadores()
        print("Pedido cancelado com sucesso.")
