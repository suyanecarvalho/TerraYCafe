import pytest
from unittest.mock import MagicMock
from src.terraycafe.model.sqlite.BO.ClienteBO import ClienteBO

@pytest.fixture
def mock_dao():
    mock = MagicMock()
    return mock

@pytest.fixture
def cliente_bo(mock_dao):
    # ClienteBO espera um db_connection, mas vamos injetar o DAO mockado
    bo = ClienteBO.__new__(ClienteBO)
    bo.dao = mock_dao
    return bo

def test_cadastrar_cliente_novo(cliente_bo, mock_dao):
    mock_dao.get_cliente_by_email.return_value = None
    cliente_bo.cadastrar_cliente('Nome', 'email@email.com', '123', 'senha')
    mock_dao.insert_cliente.assert_called_once()

def test_cadastrar_cliente_existente(cliente_bo, mock_dao):
    mock_dao.get_cliente_by_email.return_value = True
    with pytest.raises(ValueError):
        cliente_bo.cadastrar_cliente('Nome', 'email@email.com', '123', 'senha')

def test_registrar_pedido_existente(cliente_bo, mock_dao):
    mock_dao.incrementar_pedidos.return_value = True
    cliente_bo.registrar_pedido(1)
    mock_dao.incrementar_pedidos.assert_called_once_with(1)

def test_registrar_pedido_inexistente(cliente_bo, mock_dao):
    mock_dao.incrementar_pedidos.return_value = None
    with pytest.raises(ValueError):
        cliente_bo.registrar_pedido(1)

def test_tem_desconto_fidelidade(cliente_bo, mock_dao):
    mock_dao.get_qtd_pedidos.return_value = 3
    assert cliente_bo.tem_desconto_fidelidade(1) is True
    mock_dao.get_qtd_pedidos.return_value = 2
    assert cliente_bo.tem_desconto_fidelidade(1) is False

def test_get_cliente_info(cliente_bo, mock_dao):
    mock_dao.get_cliente_by_id.return_value = {'id': 1}
    assert cliente_bo.get_cliente_info(1) == {'id': 1}
    mock_dao.get_cliente_by_id.assert_called_with(1)
