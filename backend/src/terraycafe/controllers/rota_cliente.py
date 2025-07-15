# routers/cliente_router.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from terraycafe.model.sqlite.settings.connection import db_connection
from terraycafe.model.sqlite.BO.ClienteBO import ClienteBO
from terraycafe.model.sqlite.BO.pedidoBO import PedidoBO
from sqlalchemy.orm import Session

router = APIRouter(prefix="/cliente", tags=["Cliente"])

def get_db():
    db = db_connection
    return db

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
        
        # Se chegou aqui, é um objeto cliente válido
        return {
            "id": resultado.id,
            "nome": resultado.nome,
            "email": resultado.email,
            "telefone": resultado.telefone,
            "pontos_fidelidade": resultado.pontos_fidelidade
        }
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/me")
def obter_usuario_atual(db=Depends(get_db)):
    """Endpoint para obter dados do usuário logado"""
    # Por enquanto, vamos simular um usuário logado
    # Em uma implementação real, você pegaria o ID do token JWT
    try:
        # Simulando um usuário logado (você pode ajustar isso)
        # Para teste, vamos buscar o primeiro cliente da base
        cliente = ClienteBO(db).buscar_por_id(1)  # Temporário para teste
        
        if not cliente:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
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
    