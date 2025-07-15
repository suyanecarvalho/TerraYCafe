from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from terraycafe.model.sqlite.settings.connection import get_db
from terraycafe.model.sqlite.entity.ingredientes import Ingredientes as IngredienteDB

router = APIRouter(prefix="/decorator", tags=["ingredientes"])

class IngredienteCreateRequest(BaseModel):
    nome: str = Field(..., min_length=1)
    preco_adicional: float = Field(..., ge=0)

@router.post("/", status_code=201)
def criar_ingrediente(request: IngredienteCreateRequest, db: Session = Depends(get_db)):
    try:
        ingrediente = IngredienteDB(
            nome=request.nome,
            preco_adicional=request.preco_adicional
        )
        db.add(ingrediente)
        db.commit()
        db.refresh(ingrediente)
        return {
            "id": ingrediente.id,
            "nome": ingrediente.nome,
            "preco_adicional": ingrediente.preco_adicional
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar ingrediente: {e}")

@router.get("/")
def listar_ingredientes(db: Session = Depends(get_db)):
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
