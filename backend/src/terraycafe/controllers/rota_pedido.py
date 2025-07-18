from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session

from terraycafe.model.sqlite.settings.connection import get_db
from terraycafe.model.sqlite.BO.pedidoBO import PedidoBO
from terraycafe.patterns.command.alterar_pedido import AlterarPedido
from terraycafe.patterns.command.cancelar_pedido import CancelarPedido
from terraycafe.patterns.command.invoker import Invoker
from terraycafe.patterns.command.avancar_status_pedido import AvancarStatusPedido
from terraycafe.model.sqlite.DAO.ingredientesDAO import IngredientesDAO

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])
invoker = Invoker()

class PrepararBebidaRequest(BaseModel):
    tipo_bebida: str
    ingredientes: Optional[List[int]] = []

class CarrinhoItemRequest(BaseModel):
    tipo_bebida: str
    ingredientes: Optional[List[int]] = []

class ItemCarrinho(BaseModel):
    tipo_bebida: str
    ingredientes: List[int]
    preco: float

class SimulacaoPagamentoRequest(BaseModel):
    itens: List[ItemCarrinho]
    forma_pagamento: str


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
@router.patch("/{pedido_id}/alterar")
def alterar_pedido(pedido_id: int, request: dict, db: Session = Depends(get_db)):
    """Altera um pedido existente (apenas se status for 'Recebido')"""
    try:
        pedido_bo = PedidoBO(db)
        

        comando = AlterarPedido(pedido_bo, pedido_id, request)
        invoker.executar(comando)
        
        return {"message": f"Pedido {pedido_id} alterado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao alterar pedido: {e}")
    
@router.post("/bebida/preparar")
def preparar_bebida(request: PrepararBebidaRequest, db: Session = Depends(get_db)):
    try:
        pedido_bo = PedidoBO(db)
        resultado = pedido_bo.preparar_bebida(
            tipo_bebida=request.tipo_bebida,
            ingredientes=request.ingredientes,
            db=db
        )
        return resultado
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao preparar bebida: {e}")


@router.get("/cliente/{cliente_id}")
def listar_pedidos_cliente(cliente_id: int, db: Session = Depends(get_db)):
    try:
        if cliente_id <= 0:
            raise HTTPException(status_code=400, detail="ID do cliente inválido")
        
        pedido_bo = PedidoBO(db)
        pedidos = pedido_bo.listar_pedidos_por_cliente(cliente_id)
        return {"pedidos": pedidos}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos: {e}")

@router.get("/")
def listar_todos_pedidos(db: Session = Depends(get_db)):
    try:
        pedido_bo = PedidoBO(db)
        pedidos = pedido_bo.dao.listar_todos()

        pedidos_formatados = [
            {
                "id": p.id,
                "status": p.status,
                "valor_total": p.valor_total,
                "forma_pagamento": p.forma_pagamento,
                "desconto": p.desconto,
                "data_hora": p.data_hora,
                "cliente_id": p.Cliente_id
            }
            for p in pedidos
        ]

        return {"pedidos": pedidos_formatados}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos: {e}")

@router.get("/{pedido_id}")
def buscar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    try:
        if pedido_id <= 0:
            raise HTTPException(status_code=400, detail="ID do pedido inválido")

        pedido_bo = PedidoBO(db)
        pedido = pedido_bo.dao.buscar_por_id(pedido_id)

        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")

        return {
            "id": pedido.id,
            "status": pedido.status,
            "valor_total": pedido.valor_total,
            "forma_pagamento": pedido.forma_pagamento,
            "desconto": pedido.desconto,
            "data_hora": pedido.data_hora,
            "cliente_id": pedido.cliente_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar pedido: {e}")
