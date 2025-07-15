from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from terraycafe.model.sqlite.settings.connection import get_db
from terraycafe.model.sqlite.DAO.bebidaDAO import BebidaDAO

router = APIRouter(prefix="/drinks", tags=["Bebidas"])


class BebidaCreateRequest(BaseModel):
    nome: str
    descricao: str
    categoria: str
    preco_base: float

@router.get("/", response_model=List[dict])
def listar_bebidas(db: Session = Depends(get_db)):
    try:
        bebidas = BebidaDAO(db).get_all_bebidas()
        return [
            {
                "id": b.id,
                "nome": b.nome,
                "descricao": b.descricao,
                "categoria": b.categoria,
                "preco_base": b.preco_base
            }
            for b in bebidas
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar bebidas: {e}")


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
