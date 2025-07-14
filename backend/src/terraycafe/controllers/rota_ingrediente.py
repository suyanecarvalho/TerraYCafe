from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from terraycafe.model.sqlite.settings.connection import db_connection
from terraycafe.model.sqlite.entity.ingredientes import Ingredientes as IngredienteDB

router = APIRouter(prefix="/decorator", tags=["ingredientes"])

@router.get("/")
def listar_ingredientes(db: Session = Depends(db_connection)):
    try:
        ingredientes = db.query(IngredienteDB).all()
        return [
            {
                "id": ing.id,
                "nome": ing.nome,
                "preco_adicional": ing.preco_adicional
            }
            for ing in ingredientes
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar ingredientes: {e}")
