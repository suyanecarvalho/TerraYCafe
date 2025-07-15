from src.terraycafe.model.sqlite.DAO.clienteDAO import ClienteDAO

class ClienteBO:
    def __init__(self, db_connection):
        self.dao = ClienteDAO(db_connection)

    def cadastrar_cliente(self, nome: str, email: str, telefone: str, senha: str):
        if self.dao.get_cliente_by_email(email):
            raise ValueError("Cliente já cadastrado com este email.")
        cliente = self.dao.insert_cliente(nome=nome, email=email, telefone=telefone, senha=senha, ponto_fidelidade=0)
        return cliente

    def autenticar_cliente(self, email: str, senha: str):
        """Autentica um cliente pelo email e senha"""
        # Buscar cliente pelo email
        cliente = self.dao.get_cliente_by_email(email)
        print("cliente autenticado")
        
        if not cliente:
            return "cliente não encontrado"  # Cliente não encontrado

        # Verificar se a senha está correta
        if cliente.senha == senha:
            print("senha correta")
            return cliente
        else:
            return "senha incorreta"  # Senha incorreta

    def buscar_por_email(self, email: str):
        """Busca um cliente pelo email"""
        return self.dao.get_cliente_by_email(email)

    def buscar_por_id(self, cliente_id: int):
        """Busca um cliente pelo ID"""
        return self.dao.get_cliente_by_id(cliente_id)

    def registrar_pedido(self, cliente_id: int):
        cliente = self.dao.incrementar_pedidos(cliente_id)
        if not cliente:
            raise ValueError("Cliente não encontrado")

    def tem_desconto_fidelidade(self, cliente_id: int) -> bool:
        qtd = self.dao.get_qtd_pedidos(cliente_id)
        return qtd >= 3

    def get_cliente_info(self, cliente_id: int):
        return self.dao.get_cliente_by_id(cliente_id)
