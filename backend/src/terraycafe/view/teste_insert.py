from terraycafe.model.sqlite.settings.connection import Base, db_connection
from terraycafe.model.sqlite.DAO.ingredientesDAO import IngredientesDAO

db_connection.connect_to_db()
print("conectou")

Base.metadata.create_all(bind=db_connection.get_engine())
print("tabelas criadas")

dao = IngredientesDAO(db_connection)
print("DAO criado")
dao.insert_ingrediente("Chocolate", "Cobertura", 1.50)
print("Teste concluído com sucesso")