from terraycafe.model.sqlite.entity.personalizacao import Personalizacao


class PersonalizacaoDAO:
    def __init__(self, db_connection):
        self.__db_connection = db_connection

    def insert_personalizacao(self, ingredientes_id: int, item_pedido_id: int) -> None:
        with self.__db_connection as database:
            try:
                personalizacao_data = Personalizacao(
                    Ingredientes_id=ingredientes_id,
                    item_pedido_id=item_pedido_id
                )
                database.add(personalizacao_data)
                database.commit()
                print(f"Inseriu personalização: {personalizacao_data}")
            except Exception as e:
                database.rollback()
                print(f"Erro ao inserir personalização: {e}")
                raise e
    
    def get_personalizacao_by_id(self, personalizacao_id: int) -> Personalizacao:
        with self.__db_connection as database:
            try:
                personalizacao = database.query(Personalizacao).filter(Personalizacao.id == personalizacao_id).first()
                if personalizacao:
                    return personalizacao
                else:
                    print(f"Personalização com ID {personalizacao_id} não encontrada.")
                    return None
            except Exception as e:
                print(f"Erro ao buscar personalização: {e}")
                raise e
    
    def update_personalizacao(self, personalizacao_id: int, ingredientes_id: int, item_pedido_id: int) -> None: 
        with self.__db_connection as database:
            try:
                personalizacao = database.query(Personalizacao).filter(Personalizacao.id == personalizacao_id).first()
                if personalizacao:
                    personalizacao.Ingredientes_id = ingredientes_id
                    personalizacao.item_pedido_id = item_pedido_id
                    database.commit()
                    print(f"Atualizou personalização: {personalizacao}")
                else:
                    print(f"Personalização com ID {personalizacao_id} não encontrada.")
            except Exception as e:
                database.rollback()
                print(f"Erro ao atualizar personalização: {e}")
                raise e
    
    def delete_personalizacao(self, personalizacao_id: int) -> None:
        with self.__db_connection as database:
            try:
                personalizacao = database.query(Personalizacao).filter(Personalizacao.id == personalizacao_id).first()
                if personalizacao:
                    database.delete(personalizacao)
                    database.commit()
                    print(f"Deletou personalização: {personalizacao}")
                else:
                    print(f"Personalização com ID {personalizacao_id} não encontrada.")
            except Exception as e:
                database.rollback()
                print(f"Erro ao deletar personalização: {e}")
                raise e
    