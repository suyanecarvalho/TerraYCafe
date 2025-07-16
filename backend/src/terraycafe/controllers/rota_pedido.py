# routers/pedido_router.py
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from terraycafe.model.sqlite.settings.connection import db_connection
from terraycafe.model.sqlite.BO.pedidoBO import PedidoBO
from terraycafe.patterns.command.fazer_pedido import FazerPedido
from terraycafe.patterns.command.cancelar_pedido import CancelarPedido
from terraycafe.patterns.command.invoker import Invoker
from terraycafe.patterns.command.avancar_status_pedido import AvancarStatusPedido
from terraycafe.model.sqlite.settings.connection import get_db

router = APIRouter(prefix="/orders", tags=["Pedidos"])
invoker = Invoker()

class ItemPedidoRequest(BaseModel):
    tipo_bebida: str
    ingredientes: Optional[List[int]] = []

class PedidoCreateRequest(BaseModel):
    cliente_id: int
    forma_pagamento: str
    itens: List[ItemPedidoRequest] = Field(..., min_items=1)

@router.post("/", status_code=status.HTTP_201_CREATED)
def criar_pedido(request: PedidoCreateRequest, db: Session = Depends(get_db)):
    try:
        pedido_bo = PedidoBO(db)
        comando = FazerPedido(pedido_bo, {
            "cliente_id": request.cliente_id,
            "forma_pagamento": request.forma_pagamento,
            "itens": [item.dict() for item in request.itens]
        })
        pedido = invoker.executar(comando)

        return {
            "pedido_id": pedido.id,
            "status": pedido.status,
            "valor_total": pedido.valor_total,
            "forma_pagamento": pedido.forma_pagamento,
            "desconto": pedido.desconto,
            "data_hora": pedido.data_hora
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar pedido: {e}")


@router.patch("/{pedido_id}/status")
def avancar_status_pedido(pedido_id: int, db: Session = Depends(get_db)):
    try:
        pedido_bo = PedidoBO(db)
        comando = AvancarStatusPedido(pedido_bo, pedido_id)
        invoker.executar(comando)
        return {"message": f"Status do pedido {pedido_id} atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao avançar status: {e}")


@router.patch("/{pedido_id}")
def cancelar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    try:
        pedido_bo = PedidoBO(db)
        comando = CancelarPedido(pedido_bo, pedido_id)
        invoker.executar(comando)
        return {"message": f"Pedido {pedido_id} cancelado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao cancelar pedido: {e}")
