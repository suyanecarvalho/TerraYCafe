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
from terraycafe.service.pedido_temp_service import pedido_temp_service_global

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])
invoker = Invoker()

class PrepararBebidaRequest(BaseModel):
    cliente_id: int
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

class PedidoRequest(BaseModel):
    cliente_id: int
    forma_pagamento: str

class BebidaResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float
    ingredientes: List[int]
    
@router.patch("/{pedido_id}/status")
async def avancar_status_pedido(pedido_id: int, db: Session = Depends(get_db)):
    try:
        pedido_bo = PedidoBO(db)
        comando = AvancarStatusPedido(pedido_bo, pedido_id)
        await invoker.executar(comando)
        return {"message": f"Status do pedido {pedido_id} atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao avançar status: {e}")

@router.patch("/{pedido_id}")
async def cancelar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    try:
        pedido_bo = PedidoBO(db)
        comando = CancelarPedido(pedido_bo, pedido_id)
        await invoker.executar(comando)
        return {"message": f"Pedido {pedido_id} cancelado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao cancelar pedido: {e}")

@router.post("/bebida/preparar", response_model=BebidaResponse)
def preparar_bebida(request: PrepararBebidaRequest, db: Session = Depends(get_db)):
    print("Request recebido:", request)
    try:
        pedido_bo = PedidoBO(db)
        resultado = pedido_bo.preparar_bebida(
            cliente_id=request.cliente_id,  
            tipo_bebida=request.tipo_bebida,
            ingredientes=request.ingredientes,
            db=db
        )
        pedido_temp_service_global.adicionar_bebida_temp(request.cliente_id, resultado)

        print("Bebidas temporárias do cliente:", pedido_temp_service_global.get_bebidas_temp(request.cliente_id))

        if not resultado or not isinstance(resultado, dict):
            raise HTTPException(status_code=400, detail="Falha ao preparar bebida.")

        print("Resultado da preparação:", resultado)
        return BebidaResponse(**resultado)

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao preparar bebida: {e}")


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
                "cliente_id": p.cliente_id
            }
            for p in pedidos
        ]

        return {"pedidos": pedidos_formatados}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos: {e}")

@router.post("/criar")
async def criar_pedido(request: PedidoRequest, db: Session = Depends(get_db)):
    try:
        pedido_bo = PedidoBO(db)
        # Garanta que o BO usa o serviço global
        pedido_bo.pedido_temp_service = pedido_temp_service_global
        bebidas_temp = pedido_temp_service_global.get_bebidas_temp(request.cliente_id)
        if not bebidas_temp:
            raise HTTPException(status_code=400, detail="Nenhuma bebida preparada para este cliente.")
        print("Bebidas temporárias do cliente antes de criar pedido:", bebidas_temp)
        novo_pedido = await pedido_bo.finalizar_pedido(
        cliente_id=request.cliente_id,
        forma_pagamento=request.forma_pagamento
        )
        return {
            "pedido_id": novo_pedido.id,
            "message": "Pedido criado com sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar pedido: {e}")

@router.get("/cliente/{cliente_id}")
def listar_pedidos_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    try:
        pedido_bo = PedidoBO(db)
        pedidos_info = pedido_bo.listar_pedidos_por_cliente(cliente_id)
        return {"pedidos": pedidos_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos do cliente {cliente_id}: {e}")