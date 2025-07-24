from terraycafe.model.sqlite.entity.item_pedido import Item_pedido   
from typing import List


class ItemPedidoDAO:
    def __init__(self, db_connection):
        self.__db_connection = db_connection

    def insert_item_pedido(self, pedido_id: int, preco: float, bebida_id: int) -> Item_pedido:
        with self.__db_connection as database:
            try:
                item_pedido_data = Item_pedido(
                    pedido_id=pedido_id,
                    preco=preco,
                    bebida_id=bebida_id
                )
                database.add(item_pedido_data)
                database.commit()
                database.refresh(item_pedido_data)
                print(f"Inseriu item de pedido: {item_pedido_data}")
                return item_pedido_data  # <-- Retorne o objeto criado!
            except Exception as e:
                database.rollback()
                print(f"Erro ao inserir item de pedido: {e}")
                raise e
    
    def get_item_pedido_by_id(self, item_pedido_id: int) -> Item_pedido:
        with self.__db_connection as database:
            try:
                item_pedido = database.query(Item_pedido).filter(Item_pedido.id == item_pedido_id).first()
                if item_pedido:
                    return item_pedido
                else:
                    print(f"Item de pedido com ID {item_pedido_id} não encontrado.")
                    return None
            except Exception as e:
                print(f"Erro ao buscar item de pedido: {e}")
                raise e
            
    def update_item_pedido(self, item_pedido_id: int, pedido_id: int, preco: float, bebida_id: int) -> None:
        with self.__db_connection as database:
            try:
                item_pedido = database.query(Item_pedido).filter(Item_pedido.id == item_pedido_id).first()
                if item_pedido:
                    item_pedido.pedido_id = pedido_id
                    item_pedido.preco = preco
                    item_pedido.Bebida_id = bebida_id
                    database.commit()
                    print(f"Atualizou item de pedido: {item_pedido}")
                else:
                    print(f"Item de pedido com ID {item_pedido_id} não encontrado.")
            except Exception as e:
                database.rollback()
                print(f"Erro ao atualizar item de pedido: {e}")
                raise e
                
    def get_ultimo_item_pedido(self) -> Item_pedido:
            with self.__db_connection as database:
                try:
                    item = database.query(Item_pedido).order_by(Item_pedido.id.desc()).first()
                    if item:
                        return item
                    else:
                        print("Nenhum item de pedido encontrado.")
                        return None
                except Exception as e:
                    print(f"Erro ao buscar o último item de pedido: {e}")
                    raise e

    def listar_por_pedido(self, pedido_id: int) -> List[Item_pedido]:
        with self.__db_connection as database:
            try:
                itens = database.query(Item_pedido).filter(Item_pedido.pedido_id == pedido_id).all()
                if itens:
                    return itens
                else:
                    print(f"Nenhum item de pedido encontrado para o pedido ID {pedido_id}.")
                    return []
            except Exception as e:
                print(f"Erro ao listar itens de pedido: {e}")
                raise e
    def delete_item_pedido(self, item_pedido_id: int) -> None:
        """Remove um item de pedido por ID"""
        with self.__db_connection as database:
            try:
                item_pedido = database.query(Item_pedido).filter(Item_pedido.id == item_pedido_id).first()
                if item_pedido:
                    database.delete(item_pedido)
                    database.commit()
                    print(f"Removeu item de pedido: {item_pedido}")
                else:
                    print(f"Item de pedido com ID {item_pedido_id} não encontrado.")
            except Exception as e:
                database.rollback()
                print(f"Erro ao remover item de pedido: {e}")
                raise e