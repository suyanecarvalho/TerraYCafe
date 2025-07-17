# routers/cliente_router.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from terraycafe.model.sqlite.settings.connection import db_connection
from terraycafe.model.sqlite.BO.ClienteBO import ClienteBO
from terraycafe.model.sqlite.BO.pedidoBO import PedidoBO
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/cliente", tags=["Cliente"])
SECRET_KEY = "jbswq6387bd23b6d3b27@#@&dyg"
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
    db = db_connection
    return db

def obter_usuario_atual(token: str = Depends(oauth2_scheme), dd=Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        valor_sub = payload.get("sub")
        if valor_sub is None:
            raise ValueError("O campo 'sub' não está presente no payload.")
        cliente_id = int(valor_sub)
        if not cliente_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        cliente = ClienteBO(dd).buscar_por_id(cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return cliente
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.post("/register")
def criar_cliente(payload: dict, db=Depends(get_db)):
    try:
        cliente = ClienteBO(db).cadastrar_cliente(payload["nome"], payload["email"], payload["telefone"], payload["senha"])
        return {
            "id": cliente.id,
            "nome": cliente.nome,
            "email": cliente.email,
            "telefone": cliente.telefone,
            "pontos_fidelidade": cliente.pontos_fidelidade
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def fazer_login(payload: dict, db=Depends(get_db)):
    try:
        resultado = ClienteBO(db).autenticar_cliente(payload["email"], payload["senha"])
        
        # Verificar se o resultado é uma string de erro
        if isinstance(resultado, str):
            if resultado == "cliente não encontrado":
                raise HTTPException(status_code=404, detail="Cliente não encontrado")
            elif resultado == "senha incorreta":
                raise HTTPException(status_code=401, detail="Senha incorreta")
            else:
                raise HTTPException(status_code=400, detail="Erro desconhecido ao autenticar cliente")
        
        # Gerar token JWT
        token_data = {
            "sub": str(resultado.id),
            "exp": datetime.utcnow() + timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
        }
        token_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

        # Se chegou aqui, é um objeto cliente válido
        return {
            "acess_token": token_jwt,
            "token_type": "bearer",
        }
    
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/me")
def obter_usuario_logado(cliente=Depends(obter_usuario_atual)):
    try:
        return {
            "id": cliente.id,
            "nome": cliente.nome,
            "email": cliente.email,
            "telefone": cliente.telefone,
            "pontos_fidelidade": cliente.pontos_fidelidade
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.post("/{cliente_id}/pedido")
def registrar_pedido(cliente_id: int, db=Depends(get_db)):  
    return ClienteBO(db).registrar_pedido(cliente_id)

@router.get("/{cliente_id}/fidelidade")
def verificar_fidelidade(cliente_id: int, db=Depends(get_db)):  
    return {"elegivel": ClienteBO(db).tem_desconto_fidelidade(cliente_id)}

@router.get("/{cliente_id}/pedidos")
def listar_pedidos_cliente(cliente_id: int, db=Depends(get_db)):
    try:
        pedidos = PedidoBO(db).listar_pedidos_por_cliente(cliente_id)
        if not pedidos:
            return {"mensagem": "Nenhum pedido encontrado para este cliente."}
        
        return [
            {
                "pedido_id": pedido.id,
                "status": pedido.status,
                "valor_total": pedido.valor_total,
                "forma_pagamento": pedido.forma_pagamento,
                "desconto": pedido.desconto,
                "data_hora": pedido.data_hora
            }
            for pedido in pedidos
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar pedidos do cliente: {e}")
    