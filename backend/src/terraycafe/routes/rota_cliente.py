# routers/cliente_router.py
from fastapi import APIRouter, Depends, HTTPException
from terraycafe.model.sqlite.settings.connection import get_db
from model.sqlite.bo.cliente_bo import ClienteBO

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/")
def criar_cliente(payload: dict, db=Depends(get_db)):
    try:
        return ClienteBO(db).criar_cliente(payload["nome"], payload["email"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{cliente_id}/pedido")
def registrar_pedido(cliente_id: int, db=Depends(get_db)):
    return ClienteBO(db).registrar_pedido(cliente_id)

@router.get("/{cliente_id}/fidelidade")
def verificar_fidelidade(cliente_id: int, db=Depends(get_db)):
    return {"elegivel": ClienteBO(db).cliente_tem_fidelidade(cliente_id)}
