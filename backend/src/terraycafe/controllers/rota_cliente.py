# routers/cliente_router.py
from fastapi import APIRouter, Depends, HTTPException
from terraycafe.model.sqlite.settings.connection import db_connection
from terraycafe.model.sqlite.BO.ClienteBO import ClienteBO

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def criar_cliente(payload: dict, db=db_connection()):
    try:
        return ClienteBO(db).cadastrar_cliente(payload["nome"], payload["email"], payload["telefone"], payload["senha"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{cliente_id}/pedido")
def registrar_pedido(cliente_id: int, db=db_connection()):
    return ClienteBO(db).registrar_pedido(cliente_id)

@router.get("/{cliente_id}/fidelidade")
def verificar_fidelidade(cliente_id: int, db=db_connection()):
    return {"elegivel": ClienteBO(db).tem_desconto_fidelidade(cliente_id)}