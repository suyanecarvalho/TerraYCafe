
from src.terraycafe.model.sqlite.DAO.clienteDAO import ClienteDAO

class ClienteBO:
    def __init__(self, db_connection):
        self.dao = ClienteDAO(db_connection)

    def cadastrar_cliente(self, nome: str, email: str,telefone: str, senha: str):
        if self.dao.get_cliente_by_email(email):
            raise ValueError("Cliente já cadastrado com este email.")
        self.dao.insert_cliente(nome=nome, email=email,telefone=telefone,senha=senha, ponto_fidelidade=0)

    def registrar_pedido(self, cliente_id: int):
        cliente = self.dao.incrementar_pedidos(cliente_id)
        if not cliente:
            raise ValueError("Cliente não encontrado")

    def tem_desconto_fidelidade(self, cliente_id: int) -> bool:
        qtd = self.dao.get_qtd_pedidos(cliente_id)
        return qtd >= 3

    def get_cliente_info(self, cliente_id: int):
        return self.dao.get_cliente_by_id(cliente_id)
