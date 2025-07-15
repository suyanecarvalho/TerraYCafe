from src.terraycafe.model.sqlite.entity.cliente import Cliente

class ClienteDAO:
    def __init__(self, db_connection):
        self.__db_connection = db_connection
        
    def insert_cliente(self, nome: str, email: str, telefone: str, senha: str, ponto_fidelidade: int = 0) -> Cliente:
        with self.__db_connection as database:
            try:
                cliente_data = Cliente(nome=nome, email=email, telefone=telefone, senha=senha, pontos_fidelidade=ponto_fidelidade)
                database.add(cliente_data)
                database.commit()
                print(f"Inseriu cliente: {cliente_data}")
                return cliente_data

            except Exception as e:
                database.rollback()
                print(f"Erro ao inserir cliente: {e}")
                raise e
            
    def get_cliente_by_id(self, cliente_id: int) -> Cliente:
        with self.__db_connection as db:
            return db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def get_cliente_by_email(self, email: str) -> Cliente:
        with self.__db_connection as db:
            return db.query(Cliente).filter(Cliente.email == email).first()

    def incrementar_pedidos(self, cliente_id: int):
        with self.__db_connection as db:
            cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
            if cliente:
                cliente.pontos_fidelidade += 1
                db.commit()
            return cliente

    def get_qtd_pedidos(self, cliente_id: int) -> int:
        with self.__db_connection as db:
            cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
            return cliente.pontos_fidelidade if cliente else 0