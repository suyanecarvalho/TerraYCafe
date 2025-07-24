from datetime import datetime
from terraycafe.patterns.factory.selecionar_fabrica import get_fabrica
from terraycafe.patterns.decorator.decorator import BebidaDecorator, aplicar_personalizacoes
from terraycafe.model.sqlite.entity.pedido import Pedidos
from terraycafe.model.sqlite.BO.PagamentoBO import PagamentoContext
from terraycafe.model.sqlite.DAO.pedidoDAO import PedidoDAO
from terraycafe.patterns.observer.websocket_observer import WebSocketObserver
from terraycafe.patterns.state.estado_cancelado import CanceladoState
from terraycafe.model.sqlite.DAO.bebidaDAO import BebidaDAO
from terraycafe.model.sqlite.DAO.item_pedidoDAO import ItemPedidoDAO
from terraycafe.model.sqlite.DAO.personalizacaoDAO import PersonalizacaoDAO
from terraycafe.model.sqlite.DAO.ingredientesDAO import IngredientesDAO
from terraycafe.service.pedido_temp_service import pedido_temp_service_global
from terraycafe.model.sqlite.entity.bebida import Bebida
from sqlalchemy.orm import Session

    
class PedidoBO:
    def __init__(self, db_connection):
        self.dao = PedidoDAO(db_connection)
        self.bebida_dao = BebidaDAO(db_connection)
        self.item_pedido_dao = ItemPedidoDAO(db_connection)
        self.personalizacao_dao = PersonalizacaoDAO(db_connection)
        self.ingredientes_dao = IngredientesDAO(db_connection)
        self.websocket_observer = WebSocketObserver()
        self.pedido_temp_service = pedido_temp_service_global

    def preparar_bebida(self, cliente_id: int, tipo_bebida: str, ingredientes: list[int] | None, db: Session) -> dict:
        fabrica = get_fabrica(tipo_bebida)

        if not fabrica:
            raise ValueError(f"Tipo de bebida inválido: {tipo_bebida}")

        bebida = fabrica.criar_bebida()
        ingredientes_aplicados = []

        if ingredientes:
            ingredientes_objs = []
            for ingr_id in ingredientes:
                ingrediente = IngredientesDAO(db).get_ingrediente_by_id(ingr_id)
                if ingrediente:
                    ingredientes_objs.append(ingrediente)
                else:
                    raise ValueError(f"Ingrediente com ID {ingr_id} não encontrado.")

            bebida = aplicar_personalizacoes(bebida, ingredientes_objs)
            ingredientes_aplicados = [i.id for i in ingredientes_objs]

        preco = bebida.get_preco()
        nome = bebida.get_nome()
        descricao = bebida.get_descricao()

        # 🎯 Criação da bebida no banco
        nova_bebida = Bebida(
            nome=nome,
            descricao=descricao,
            preco_base=preco  # ← aqui foi o ajuste principal
        )
        db.add(nova_bebida)
        db.commit()
        db.refresh(nova_bebida)  # pega o ID gerado

        return {
            "id": nova_bebida.id,
            "nome": nova_bebida.nome,
            "descricao": nova_bebida.descricao,
            "preco": nova_bebida.preco_base, 
            "ingredientes": ingredientes_aplicados
        }



    async def finalizar_pedido(self, cliente_id: int, forma_pagamento: str) -> Pedidos:
        # Recupera bebidas temporárias já preparadas
        bebidas_temp = self.pedido_temp_service.get_bebidas_temp(cliente_id)
        print("Bebidas temporárias no momento do pedido:", bebidas_temp)
        if not bebidas_temp:
            raise ValueError("Nenhuma bebida preparada para este cliente.")

        try:
            pedido = Pedidos(
                status="Recebido",
                valor_total=0.0,
                forma_pagamento=forma_pagamento,
                desconto=0,
                data_hora=datetime.now(),
                cliente_id=cliente_id
            )
            print("Criando pedido:", pedido)

            valor_bruto_total = sum(b["preco"] for b in bebidas_temp)
            pagamento = PagamentoContext(forma_pagamento)
            resultado_pagamento = pagamento.processar_pagamento(valor_bruto_total)

            pedido.valor_total = resultado_pagamento["valor_final"]
            pedido.desconto = resultado_pagamento["desconto"]
            pedido.forma_pagamento = forma_pagamento

            self.dao.salvar(pedido)
            print("Pedido salvo:", pedido)

            for bebida_temp in bebidas_temp:
                print("Processando bebida:", bebida_temp)
                # Use o ID salvo, não tente buscar/inserir de novo
                bebida_id = bebida_temp["id"]
                item_pedido = self.item_pedido_dao.insert_item_pedido(
                    pedido_id=pedido.id,
                    preco=bebida_temp["preco"],
                    bebida_id=bebida_id
                )
                print("Item pedido salvo:", item_pedido)

                for ingrediente_id in bebida_temp.get("ingredientes", []):
                    print("Inserindo personalização:", ingrediente_id)
                    self.personalizacao_dao.insert_personalizacao(
                        item_pedido_id=item_pedido.id,
                        ingredientes_id=ingrediente_id
                    )


            self.pedido_temp_service.limpar_bebidas_temp(cliente_id)
            pedido.registrar_observadores()
            pedido.adicionar_observador(self.websocket_observer)
            await pedido.notificar_observadores((pedido.id, pedido.status, pedido.cliente_id))


            return pedido

        except Exception as e:
            print("Erro interno ao finalizar pedido:", e)
            raise
    async def avancar_status(self, pedido_id: int):
        pedido = self.dao.buscar_por_id(pedido_id)
        if pedido:
            pedido.adicionar_observador(self.websocket_observer)  # Adiciona o observer websocket
            await pedido.avancar_estado()
            self.dao.atualizar(pedido.id,pedido.status,pedido.valor_total, pedido.forma_pagamento, pedido.desconto, pedido.data_hora, pedido.cliente_id)
            await pedido.notificar_observadores((pedido.id, pedido.status))  # Notifica todos observers

    async def alterar_pedido(self, pedido_id: int, novos_dados: dict) -> Pedidos:
        """
        Altera um pedido existente se ele estiver no status 'Recebido'
        """
        pedido = self.dao.buscar_por_id(pedido_id)
        if not pedido:
            raise ValueError("Pedido não encontrado.")
        
        if pedido.status != "Recebido":
            raise ValueError("Pedido não pode ser alterado após o preparo começar.")
        
        # Backup dos dados originais para possível rollback
        dados_originais = {
            "status": pedido.status,
            "valor_total": pedido.valor_total,
            "forma_pagamento": pedido.forma_pagamento,
            "desconto": pedido.desconto,
            "data_hora": pedido.data_hora,
            "cliente_id": pedido.cliente_id
        }
        
        try:
            # Se alterando itens do pedido, recalcular valor total
            if "itens" in novos_dados:
                # Remover itens antigos
                itens_antigos = self.item_pedido_dao.listar_por_pedido(pedido_id)
                for item in itens_antigos:
                    # Remover personalizações do item
                    self.personalizacao_dao.delete_por_item_pedido(item.id)
                    # Remover item
                    self.item_pedido_dao.delete_item_pedido(item.id)
                
                # Adicionar novos itens
                novos_itens = novos_dados["itens"]
                valor_bruto_total = 0
                
                for item in novos_itens:
                    if isinstance(item, dict):
                        ingredientes = item.get("ingredientes", [])
                        tipo = item["tipo_bebida"]
                        bebida_id = item.get("id")  # <-- Pegue o id da bebida já criada
                    else:
                        ingredientes = getattr(item, "ingredientes", [])
                        tipo = getattr(item, "tipo_bebida")
                        bebida_id = getattr(item, "id", None)

                    # Buscar bebida pelo ID, se existir
                    bebida_db = None
                    if bebida_id:
                        bebida_db = self.bebida_dao.buscar_por_id(bebida_id)

                    if not bebida_db:
                        # Se não existir, crie uma nova
                        fabrica = get_fabrica(tipo)
                        if not fabrica:
                            raise ValueError(f"Tipo de bebida inválido: {tipo}")
                        bebida = fabrica.criar_bebida()
                        bebida_personalizada = aplicar_personalizacoes(bebida, ingredientes)
                        nome = bebida_personalizada.get_nome()
                        descricao = bebida_personalizada.get_descricao()
                        preco_item = round(bebida_personalizada.get_preco(), 2)
                        # Tente buscar por nome/descrição/preço antes de criar
                        bebida_db = self.bebida_dao.buscar_por_nome_descricao_preco(
                            nome=nome,
                            descricao=descricao,
                            preco_base=preco_item
                        )
                        if not bebida_db:
                            bebida_db = self.bebida_dao.insert_bebida(
                                nome=nome,
                                descricao=descricao,
                                preco_base=preco_item,
                            )
                    else:
                        preco_item = round(bebida_db.preco_base, 2)
                    valor_bruto_total += preco_item

                    # Sempre crie o item do pedido, independente de ser bebida nova ou existente
                    self.item_pedido_dao.insert_item_pedido(
                        pedido_id=pedido_id,
                        preco=preco_item,
                        bebida_id=bebida_db.id
                    )

                    # Buscar o item recém-criado
                    item_pedido = self.item_pedido_dao.get_ultimo_item_pedido()

                    # Salvar personalizações
                    for ingrediente_id in ingredientes:
                        self.personalizacao_dao.insert_personalizacao(
                            item_pedido_id=item_pedido.id,
                            ingredientes_id=ingrediente_id
                        )
                
                # Recalcular valor total com pagamento
                forma_pagamento = novos_dados.get("forma_pagamento", pedido.forma_pagamento)
                pagamento = PagamentoContext(forma_pagamento)
                resultado_pagamento = pagamento.processar_pagamento(valor_bruto_total)
                
                # Atualizar valores do pedido
                pedido.valor_total = resultado_pagamento["valor_final"]
                pedido.desconto = int(resultado_pagamento["desconto"])
                pedido.forma_pagamento = resultado_pagamento["tipo_pagamento"]
            
            # Atualizar outros campos se fornecidos
            if "forma_pagamento" in novos_dados and "itens" not in novos_dados:
                # Se só mudou forma de pagamento, recalcular desconto
                forma_pagamento = novos_dados["forma_pagamento"]
                valor_atual = pedido.valor_total + pedido.desconto  # Valor bruto
                pagamento = PagamentoContext(forma_pagamento)
                resultado_pagamento = pagamento.processar_pagamento(valor_atual)
                
                pedido.valor_total = resultado_pagamento["valor_final"]
                pedido.desconto = int(resultado_pagamento["desconto"])
                pedido.forma_pagamento = resultado_pagamento["tipo_pagamento"]
            
            # Salvar alterações
            self.dao.salvar(pedido)
            
            # Notificar observadores sobre a alteração
            await pedido.notificar_observadores()
            
            return pedido
            
        except Exception as e:
            # Em caso de erro, fazer rollback
            print(f"Erro ao alterar pedido. Fazendo rollback: {e}")
            # Restaurar dados originais
            for campo, valor in dados_originais.items():
                setattr(pedido, campo, valor)
            self.dao.salvar(pedido)
            raise e

    def buscar_pedido(self, pedido_id: int) -> Pedidos:
        """
        Busca um pedido por ID (método que estava sendo chamado no comando)
        """
        return self.dao.buscar_por_id(pedido_id)

    async def cancelar_pedido(self, pedido_id: int):
        pedido = self.dao.buscar_por_id(pedido_id)
        if not pedido:
            print("Pedido não encontrado.")
            return

        if pedido.status != "Recebido":
            print("Só é possível cancelar pedidos no estado 'Recebido'.")
            return

        await pedido.set_estado(CanceladoState())
        self.dao.atualizar(pedido.id,pedido.status,pedido.valor_total, pedido.forma_pagamento, pedido.desconto, pedido.data_hora, pedido.cliente_id)
        await pedido.notificar_observadores()
        print("Pedido cancelado com sucesso.")

    def listar_pedidos_por_cliente(self, cliente_id: int):
        pedidos = self.dao.listar_por_cliente(cliente_id)
        if not pedidos:
            return []

        pedidos_info = []
        for pedido in pedidos:
            itens = self.item_pedido_dao.listar_por_pedido(pedido.id)
            itens_info = []
            for item in itens:
                bebida = self.bebida_dao.buscar_por_id(item.bebida_id)
                ingredientes_personalizados = self.personalizacao_dao.listar_por_item_pedido(item.id)
                ingredientes_nomes = []
                for p in ingredientes_personalizados:
                    ingrediente = self.ingredientes_dao.get_ingrediente_by_id(p.ingredientes_id)
                    if ingrediente:
                        ingredientes_nomes.append(ingrediente.nome)
                itens_info.append({
                    "bebida": bebida.nome if bebida else "Bebida não encontrada",
                    "preco": item.preco,
                    "ingredientes": ingredientes_nomes
                })

            pedidos_info.append({
                "id": pedido.id,
                "status": pedido.status,
                "valor_total": pedido.valor_total,
                "forma_pagamento": pedido.forma_pagamento,
                "desconto": pedido.desconto,
                "data_hora": pedido.data_hora,
                "itens": itens_info
            })

        return pedidos_info
