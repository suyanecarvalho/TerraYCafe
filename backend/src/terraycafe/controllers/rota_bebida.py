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

@router.get("/", response_model=List[dict])
def listar_fabricas():
    try:
        tipos = listar_tipos_bebidas_disponiveis()
        bebidas_disponiveis = []
        for tipo in tipos:
            fabrica = get_fabrica(tipo)
            bebida = fabrica.criar_bebida()
            bebidas_disponiveis.append({
                "nome": bebida.nome,
                "descricao": bebida.descricao,
                "categoria": bebida.categoria,
                "preco_base": bebida.preco_base
            })
        return bebidas_disponiveis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
