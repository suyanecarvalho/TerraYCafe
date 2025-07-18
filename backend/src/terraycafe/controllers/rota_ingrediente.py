from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from terraycafe.model.sqlite.settings.connection import get_db
from terraycafe.model.sqlite.entity.ingredientes import Ingredientes as IngredienteDB
from typing import List

router = APIRouter(prefix="/decorator", tags=["ingredientes"])

class IngredienteResponse(BaseModel):
    id: int
    nome: str
    preco_adicional: float
    class Config:
        orm_mode = True  

@router.get("/", response_model=List[IngredienteResponse])
def listar_ingredientes(db: Session = Depends(get_db)):
    try:
        ingredientes = db.query(IngredienteDB).all()
        return ingredientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar ingredientes: {e}")
