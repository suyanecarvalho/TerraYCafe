from terraycafe.model.sqlite.settings.connection import Base, db_connection
from terraycafe.model.sqlite.DAO.clienteDAO import ClienteDAO

db_connection.connect_to_db()
print("conectou")

Base.metadata.create_all(bind=db_connection.get_engine())
print("tabelas criadas")

dao = ClienteDAO(db_connection)
print("DAO criado")
dao.insert_cliente("maria Silva", "maria@teste.com", 10)
print("Teste concluído com sucesso")
        