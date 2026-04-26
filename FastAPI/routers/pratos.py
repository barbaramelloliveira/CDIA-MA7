from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from FastAPI.models.prato import PratoInput, PratoOutput

# PRATOS 

router = APIRouter()

pratos = [
    {"id": 1, "nome": "Margherita", "categoria": "pizza", "preco": 45.0, "disponivel": True},
    {"id": 2, "nome": "Carbonara", "categoria": "massa", "preco": 52.0, "disponivel": False},
    {"id": 3, "nome": "Tiramisù", "categoria": "sobremesa", "preco": 28.0, "disponivel": True},
    {"id": 4, "nome": "Lasagna alla Bolognese", "categoria": "massa", "preco": 55.0, "disponivel": True},
    {"id": 5, "nome": "Cannoli", "categoria": "sobremesa", "preco": 22.0, "disponivel": False},
    {"id": 6, "nome": "Panna Cotta", "categoria": "sobremesa", "preco": 25.0, "disponivel": True},
]

class DisponibilidadeInput(BaseModel):
    disponivel: bool

@router.get("/")
async def listar_pratos(
    categoria: Optional[str] = None,
    preco_maximo: Optional[float] = None,
    apenas_disponiveis: Optional[bool] = False
):
    resultado = pratos

    if categoria:
        resultado = [p for p in resultado if p["categoria"] == categoria]

    if preco_maximo:
        resultado = [p for p in resultado if p["preco"] <= preco_maximo]

    if apenas_disponiveis:
        resultado = [p for p in resultado if p["disponivel"]]

    return resultado


@router.get("/{prato_id}")
async def buscar_prato(prato_id: int, formato: str = "completo"):
    prato = next((p for p in pratos if p["id"] == prato_id), None)

    if not prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")

    if formato == "resumido":
        return {"nome": prato["nome"], "preco": prato["preco"]}

    return prato


@router.put("/{prato_id}/disponibilidade")
async def alterar_disponibilidade(prato_id: int, dados: DisponibilidadeInput):

    prato = next((p for p in pratos if p["id"] == prato_id), None)

    if not prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")

    prato["disponivel"] = dados.disponivel
    return prato


@router.post("/", response_model=PratoOutput)
async def criar_prato(prato: PratoInput):
    novo_id = max(p["id"] for p in pratos) + 1

    novo_prato = {
        "id": novo_id,
        "criado_em": datetime.now().isoformat(),
        **prato.model_dump()
    }

    pratos.append(novo_prato)
    return novo_prato

