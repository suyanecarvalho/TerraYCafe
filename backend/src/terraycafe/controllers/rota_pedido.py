from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from pydantic import BaseModel 
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List

from terraycafe.model.sqlite.settings.connection import db_connection
from terraycafe.model.sqlite.BO.pedidoBO import PedidoBO

router = APIRouter(prefix="/orders", tags=["Pedidos"])


class ItemPedidoRequest(BaseModel):
    tipo_bebida: str
    ingredientes: Optional[List[int]] = []

class PedidoCreateRequest(BaseModel):
    cliente_id: int
    forma_pagamento: str
    itens: List[ItemPedidoRequest] = Field(..., min_items=1)


@router.post("/", status_code=status.HTTP_201_CREATED)
def criar_pedido(request: PedidoCreateRequest, db: Session = Depends(db_connection)):
    try:
        pedido = PedidoBO(db).criar_pedido(
            cliente_id=request.cliente_id,
            itens=[item.dict() for item in request.itens],  
            forma_pagamento=request.forma_pagamento
        )
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
def avancar_status_pedido(pedido_id: int, db: Session = Depends(db_connection)):
    try:
        PedidoBO(db).avancar_status(pedido_id)
        return {"message": f"Status do pedido {pedido_id} atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao avançar status: {e}")

@router.patch("/{pedido_id}")
def cancelar_pedido(pedido_id: int, db: Session = Depends(db_connection)):
    try:
        PedidoBO(db).cancelar_pedido(pedido_id)
        return {"message": f"Pedido {pedido_id} cancelado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao cancelar pedido: {e}")
    
    