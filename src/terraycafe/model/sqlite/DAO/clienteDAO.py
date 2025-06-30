from terraycafe.model.sqlite.entity.cliente import Cliente

class ClienteDAO:
    def __init__(self, db_connection):
        self.__db_connection = db_connection
        
    def insert_cliente(self, nome: str, email: str,ponto_fidelidade: int) -> None:
        with self.__db_connection as database:
            try:
                cliente_data = Cliente(nome=nome, email=email, pontos_fidelidade=ponto_fidelidade)
                database.add(cliente_data)
                database.commit()
                print(f"inseriu cliente: {cliente_data}")

            except Exception as e:
                database.rollback()
                print(f"Erro ao inserir cliente: {e}")
                raise e