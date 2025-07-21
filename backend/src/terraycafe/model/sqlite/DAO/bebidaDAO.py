from terraycafe.model.sqlite.entity.bebida import Bebida

class BebidaDAO:
    def __init__(self, db_connection):
        self.__db_connection = db_connection

    def insert_bebida(self, nome: str, descricao: str, preco_base: float) -> None:
        with self.__db_connection as database:
            try:
                bebida_data = Bebida(
                    nome=nome,
                    descricao=descricao,
                    preco_base=preco_base,
                )
                database.add(bebida_data)
                database.commit()
                print(f"Inseriu bebida: {bebida_data}")
            except Exception as e:
                database.rollback()
                print(f"Erro ao inserir bebida: {e}")
                raise e
    
    def get_bebida_by_id(self, bebida_id: int) -> Bebida:
        with self.__db_connection as database:
            try:
                bebida = database.query(Bebida).filter(Bebida.id == bebida_id).first()
                if bebida:
                    return bebida
                else:
                    print(f"Bebida com ID {bebida_id} não encontrada.")
                    return None
            except Exception as e:
                print(f"Erro ao buscar bebida: {e}")
                raise e
            
    def update_bebida(self, bebida_id: int, nome: str, descricao: str, preco_base: float) -> None:
        with self.__db_connection as database:
            try:
                bebida = database.query(Bebida).filter(Bebida.id == bebida_id).first()
                if bebida:
                    bebida.nome = nome
                    bebida.descricao = descricao
                    bebida.preco_base = preco_base
                    database.commit()
                    print(f"Atualizou bebida: {bebida}")
                else:
                    print(f"Bebida com ID {bebida_id} não encontrada.")
            except Exception as e:
                database.rollback()
                print(f"Erro ao atualizar bebida: {e}")
                raise e
            
    def delete_bebida(self, bebida_id: int) -> None:
        with self.__db_connection as database:
            try:
                bebida = database.query(Bebida).filter(Bebida.id == bebida_id).first()
                if bebida:
                    database.delete(bebida)
                    database.commit()
                    print(f"Deletou bebida: {bebida}")
                else:
                    print(f"Bebida com ID {bebida_id} não encontrada.")
            except Exception as e:
                database.rollback()
                print(f"Erro ao deletar bebida: {e}")
                raise e
    
    def get_all_bebidas(self) -> list[Bebida]:
        with self.__db_connection as database:
            try:
                bebidas = database.query(Bebida).all()
                return bebidas
            except Exception as e:
                print(f"Erro ao buscar todas as bebidas: {e}")
                raise e
    
    def buscar_por_id(self, bebida_id: int) -> Bebida:
        with self.__db_connection as database:
            try:
                bebida = database.query(Bebida).filter(Bebida.id == bebida_id).first()
                if bebida:
                    return bebida
                else:
                    print(f"Bebida com ID {bebida_id} não encontrada.")
                    return None
            except Exception as e:
                print(f"Erro ao buscar bebida: {e}")
                raise e
    
    def buscar_por_nome_descricao_preco(self, nome, descricao, preco_base):
        with self.__db_connection as database:
            return database.query(Bebida).filter(
                Bebida.nome == nome,
                Bebida.descricao == descricao,
                Bebida.preco_base == preco_base
            ).first()