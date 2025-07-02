from terraycafe.model.sqlite.settings.connection import Base, db_connection
from terraycafe.model.sqlite.entity.cliente import Cliente
from terraycafe.model.sqlite.entity.pedido import Pedidos
from terraycafe.model.sqlite.DAO.ingredientesDAO import IngredientesDAO
from terraycafe.model.sqlite.DAO.pedidoDAO import PedidoDAO
from terraycafe.model.sqlite.DAO.bebidaDAO import BebidaDAO
from terraycafe.model.sqlite.DAO.personalizacaoDAO import PersonalizacaoDAO

db_connection.connect_to_db()
print("conectou")

Base.metadata.create_all(bind=db_connection.get_engine())
print("tabelas criadas")

dao = PersonalizacaoDAO(db_connection)
print("DAO criado")