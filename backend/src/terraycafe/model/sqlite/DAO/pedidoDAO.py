from terraycafe.model.sqlite.entity.pedido import Pedidos
from terraycafe.patterns.state.recebido_state import RecebidoState


class PedidoDAO:
    def __init__(self, db_connection):
        self.__db_connection = db_connection
        self.estado = RecebidoState()
        self.observadores = []
        
    def insert_pedido(self, status: str, valor_total: float, forma_pagamento: str, desconto: int, data_hora, cliente_id: int) -> None:
        with self.__db_connection as database:
            try:
                pedido_data = Pedidos(
                    status=status,
                    valor_total=valor_total,
                    forma_pagamento=forma_pagamento,
                    desconto=desconto,
                    data_hora=data_hora,
                    Cliente_id=cliente_id
                )
                database.add(pedido_data)
                database.commit()
                print(f"Inseriu pedido: {pedido_data}")
            except Exception as e:
                database.rollback()
                print(f"Erro ao inserir pedido: {e}")
                raise e

    def buscar_por_id(self, pedido_id: int) -> Pedidos:
        with self.__db_connection as database:
            try:
                pedido = database.query(Pedidos).filter(Pedidos.id == pedido_id).first()
                if pedido:
                    return pedido
                else:
                    print(f"Pedido com ID {pedido_id} não encontrado.")
                    return None
            except Exception as e:
                print(f"Erro ao buscar pedido: {e}")
                raise e

    def atualizar(self, pedido_id: int, status: str, valor_total: float, forma_pagamento: str, desconto: int, data_hora, cliente_id: int) -> None:
        with self.__db_connection as database:
            try:
                pedido = database.query(Pedidos).filter(Pedidos.id == pedido_id).first()
                if pedido:
                    pedido.status = status
                    pedido.valor_total = valor_total
                    pedido.forma_pagamento = forma_pagamento
                    pedido.desconto = desconto
                    pedido.data_hora = data_hora
                    pedido.cliente_id = cliente_id
                    database.commit()
                    print(f"Atualizou pedido: {pedido}")
                else:
                    print(f"Pedido com ID {pedido_id} não encontrado.")
            except Exception as e:
                database.rollback()
                print(f"Erro ao atualizar pedido: {e}")
                raise e

    def delete_pedido(self, pedido_id: int) -> None:
        with self.__db_connection as database:
            try:
                pedido = database.query(Pedidos).filter(Pedidos.id == pedido_id).first()
                if pedido:
                    database.delete(pedido)
                    database.commit()
                    print(f"Deletou pedido: {pedido}")
                else:
                    print(f"Pedido com ID {pedido_id} não encontrado.")
            except Exception as e:
                database.rollback()
                print(f"Erro ao deletar pedido: {e}")
                raise e
    
    def salvar(self, pedido: Pedidos) -> None:
        from terraycafe.model.sqlite.DAO.bebidaDAO import BebidaDAO  # Importação local para evitar ciclos
        with self.__db_connection as database:
            try:
                bebida_dao = BebidaDAO(self.__db_connection)
                # Verifica e evita bebidas duplicadas nos itens do pedido
                if hasattr(pedido, "itens"):
                    for item in pedido.itens:
                        bebida = item.bebida
                        if bebida:
                            bebida_existente = bebida_dao.buscar_por_nome_descricao_preco(
                                nome=bebida.nome,
                                descricao=bebida.descricao,
                                preco_base=bebida.preco_base
                            )
                            if bebida_existente:
                                # Usa a bebida existente em vez de criar uma nova
                                item.bebida_id = bebida_existente.id
                                item.bebida = bebida_existente
                            else:
                                # Adiciona a bebida nova normalmente
                                database.add(bebida)
                if database.get(Pedidos, pedido.id):
                    pedido_existente = database.query(Pedidos).filter(Pedidos.id == pedido.id).first()
                    if pedido_existente:
                        for attr, value in vars(pedido).items():
                            if attr != "_sa_instance_state":
                                setattr(pedido_existente, attr, value)
                        print(f"Atualizou pedido: {pedido_existente}")
                else:
                    database.add(pedido)
                database.commit()
                database.refresh(pedido)
            except Exception as e:
                database.rollback()
                raise e
        
    def listar_por_cliente(self, cliente_id: int):
        return self.__db_connection.query(Pedidos).filter(Pedidos.cliente_id == cliente_id).all()

    def listar_todos(self) -> list[Pedidos]:  
        with self.__db_connection as database:
            try:
                pedidos = database.query(Pedidos).all()
                return pedidos
            except Exception as e:
                print(f"Erro ao listar pedidos: {e}")
                raise e
