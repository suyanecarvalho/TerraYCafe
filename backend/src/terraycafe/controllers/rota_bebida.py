from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from terraycafe.model.sqlite.settings.connection import get_db
from terraycafe.model.sqlite.DAO.bebidaDAO import BebidaDAO
from terraycafe.patterns.factory.fabricas import listar_tipos_bebidas_disponiveis, get_fabrica

router = APIRouter(prefix="/bebidas", tags=["Bebidas"])


class BebidaCreateRequest(BaseModel):
    nome: str
    descricao: str
    categoria: str
    preco_base: float

@router.post("/")
def criar_bebida(request: BebidaCreateRequest, db: Session = Depends(get_db)):
    try:
        BebidaDAO(db).insert_bebida(
            nome=request.nome,
            descricao=request.descricao,
            preco_base=request.preco_base,
            categoria=request.categoria
        )
        return {"message": "Bebida criada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar bebida: {e}")

@router.get("/", response_model=List[dict])
def listar_bebidas_menu():
    """Lista as bebidas disponíveis no menu usando as informações das fábricas"""
    try:
        tipos = listar_tipos_bebidas_disponiveis()
        bebidas_menu = []
        for tipo in tipos:
            fabrica = get_fabrica(tipo)
            if fabrica and hasattr(fabrica, "info_bebida"):
                info = fabrica.info_bebida()
                info["tipo"] = tipo
                bebidas_menu.append(info)
        return bebidas_menu
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar bebidas do menu: {e}")

@router.get("/banco", response_model=List[dict])
def listar_bebidas_banco(db: Session = Depends(get_db)):
    """Lista as bebidas que foram criadas no banco de dados"""
    try:
        bebidas = BebidaDAO(db).get_all_bebidas()
        bebidas_banco = []
        for bebida in bebidas:
            bebidas_banco.append({
                "id": bebida.id,
                "nome": bebida.nome,
                "descricao": bebida.descricao,
                "categoria": bebida.categoria,
                "preco_base": bebida.preco_base
            })
        return bebidas_banco
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{bebida_id}")
def buscar_bebida(bebida_id: int, db: Session = Depends(get_db)):
    try:
        bebida = BebidaDAO(db).buscar_por_id(bebida_id)
        if bebida is None:
            raise HTTPException(status_code=404, detail="Bebida não encontrada")
        return {
            "id": bebida.id,
            "nome": bebida.nome,
            "descricao": bebida.descricao,
            "categoria": bebida.categoria,
            "preco_base": bebida.preco_base
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar bebida: {e}")

