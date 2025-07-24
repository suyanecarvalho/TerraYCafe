from terraycafe.model.sqlite.entity.ingredientes import Ingredientes


class IngredientesDAO:
    def __init__(self, db_connection):
        self.__db_connection = db_connection

    def insert_ingrediente(self, nome: str, preco_adicional: float) -> None:
        with self.__db_connection as database:
            try:
                ingrediente_data = Ingredientes(nome=nome, preco_adicional=preco_adicional)
                database.add(ingrediente_data)
                database.commit()
                print(f"Inseriu ingrediente: {ingrediente_data}")
            except Exception as e:
                database.rollback()
                print(f"Erro ao inserir ingrediente: {e}")
                raise e
            
    def get_ingrediente_by_id(self, ingrediente_id: int) -> Ingredientes:
        with self.__db_connection as database:
            try:
                ingrediente = database.query(Ingredientes).filter(Ingredientes.id == ingrediente_id).first()
                if ingrediente:
                    return ingrediente
                else:
                    print(f"Ingrediente com ID {ingrediente_id} não encontrado.")
                    return None

            except Exception as e:
                print(f"Erro ao buscar ingrediente: {e}")
                raise e
    
    def update_ingrediente(self, ingrediente_id: int, nome: str, preco_adicional: float) -> None:
        with self.__db_connection as database:
            try:
                ingrediente = database.query(Ingredientes).filter(Ingredientes.id == ingrediente_id).first()
                if ingrediente:
                    ingrediente.nome = nome
                    ingrediente.preco_adicional = preco_adicional
                    database.commit()
                    print(f"Atualizou ingrediente: {ingrediente}")
                else:
                    print(f"Ingrediente com ID {ingrediente_id} não encontrado.")
            except Exception as e:
                database.rollback()
                print(f"Erro ao atualizar ingrediente: {e}")
                raise e
            
    def delete_ingrediente(self, ingrediente_id: int) -> None:
        with self.__db_connection as database:
            try:
                ingrediente = database.query(Ingredientes).filter(Ingredientes.id == ingrediente_id).first()
                if ingrediente:
                    database.delete(ingrediente)
                    database.commit()
                    print(f"Deletou ingrediente: {ingrediente}")
                else:
                    print(f"Ingrediente com ID {ingrediente_id} não encontrado.")

            except Exception as e:
                database.rollback()
                print(f"Erro ao deletar ingrediente: {e}")
                raise e 
            
    def get_all_ingredientes(self) -> list[Ingredientes]:
        with self.__db_connection as database:
            try:
                ingredientes = database.query(Ingredientes).all()
                return ingredientes

            except Exception as e:
                print(f"Erro ao buscar todos os ingredientes: {e}")
                raise e
            
    def get_ingrediente_by_name(self, nome: str) -> Ingredientes:
        with self.__db_connection as database:
            try:
                ingrediente = database.query(Ingredientes).filter(Ingredientes.nome == nome).first()
                if ingrediente:
                    return ingrediente
                else:
                    print(f"Ingrediente com nome '{nome}' não encontrado.")
                    return None

            except Exception as e:
                print(f"Erro ao buscar ingrediente por nome: {e}")
                raise e
