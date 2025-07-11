"""
Teste REAL do ClienteBO - inserindo n        # Tentar cadastrar cliente
        print("\n🔄 Inserindo cliente no banco...")
        cliente_bo.cadastrar_cliente(nome, email, telefone, senha)anco de dados
"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.terraycafe.model.sqlite.BO.ClienteBO import ClienteBO
from src.terraycafe.model.sqlite.settings.connection import DBConnection


def teste_inserir_cliente_real():
    """Testa inserção REAL de cliente no banco"""
    print("🧪 TESTE REAL - Inserindo cliente no banco")
    print("=" * 50)
    
    try:
        # Criar conexão real com o banco
        print("Conectando ao banco de dados...")
        db_connection = DBConnection()
        db_connection.connect_to_db()
        print("✅ Conexão estabelecida")
        
        # Criar ClienteBO com conexão real
        print("🔧 Criando ClienteBO...")
        cliente_bo = ClienteBO(db_connection)
        print("✅ ClienteBO criado")
        
        # Dados do cliente para teste
        nome = "Maria Silva"
        email = "maria.etes@email.com"
        telefone = "11999999999"
        senha = "senha123"
        
        print(f"\n Dados do cliente:")
        print(f"   Nome: {nome}")
        print(f"   Email: {email}")
        print(f"   Telefone: {telefone}")
        
        # Tentar cadastrar cliente
        print("\n Inserindo cliente no banco...")
        cliente_bo.cadastrar_cliente(nome, email, telefone, senha)
        
        print("🎉 CLIENTE INSERIDO COM SUCESSO!")
        print("✅ Verificar no banco de dados para confirmar")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False


def teste_buscar_clientes():
    """Busca todos os clientes para verificar se foi inserido"""
    print("\n� VERIFICANDO CLIENTES NO BANCO")
    print("-" * 40)
    
    try:
        # Conectar ao banco
        db_connection = DBConnection()
        db_connection.connect_to_db()
        
        # Usar sessão para buscar diretamente
        with db_connection as session:
            from src.terraycafe.model.sqlite.entity.cliente import Cliente
            clientes = session.query(Cliente).all()
            
            if clientes:
                print(f"📊 Total de clientes encontrados: {len(clientes)}")
                print("\n� Lista de clientes:")
                for i, cliente in enumerate(clientes, 1):
                    print(f"   {i}. ID: {cliente.id} | Nome: {cliente.nome} | Email: {cliente.email}")
            else:
                print("� Nenhum cliente encontrado no banco")
                
    except Exception as e:
        print(f"❌ Erro ao buscar clientes: {e}")


def main():
    """Função principal"""
    print("🚀 TESTE COM BANCO REAL")
    print("=" * 50)
    
    # Teste 1: Inserir cliente
    sucesso = teste_inserir_cliente_real()
    
    # Teste 2: Verificar se foi inserido
    teste_buscar_clientes()
    
    print("\n" + "=" * 50)
    if sucesso:
        print("✅ TESTE CONCLUÍDO - Cliente inserido no banco!")
    else:
        print("❌ TESTE FALHOU - Verifique os erros acima")
    print("=" * 50)


if __name__ == "__main__":
    main()
