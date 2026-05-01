from fastapi import APIRouter, HTTPException
from datetime import datetime
from FastAPI.models.bebidas import BebidaInput, BebidaOutput

# Bebidas

router = APIRouter()

bebidas = [
    {
        "id": 1,
        "nome": "Água Mineral",
        "categoria": "Água",
        "preco": 6.00,
        "alcoolica": False,
        "ml": 500,
        "disponivel": True,
        "criado_em": "2024-06-01T12:00:00",
    },
    {
        "id": 2,
        "nome": "Coca-Cola",
        "categoria": "Refrigerante",
        "preco": 10.00,
        "alcoolica": False,
        "ml": 350,
        "disponivel": True,
        "criado_em": "2024-06-01T12:05:00",
    },
    {
        "id": 3,
        "nome": "Suco de Laranja",
        "categoria": "Suco",
        "preco": 12.00,
        "alcoolica": False,
        "ml": 300,
        "disponivel": False,
        "criado_em": "2024-06-01T12:10:00",
    },
    {
        "id": 4,
        "nome": "Cerveja",
        "categoria": "Cerveja",
        "preco": 15.00,
        "alcoolica": True,
        "ml": 500,
        "disponivel": True,
        "criado_em": "2024-06-01T12:15:00",
    },
    {
        "id": 5,
        "nome": "Vinho Tinto",
        "categoria": "Vinho",
        "preco": 50.00,
        "alcoolica": True,
        "ml": 750,
        "disponivel": False,
        "criado_em": "2024-06-01T12:20:00",
    },
    {
        "id": 6,
        "nome": "Espumante",
        "categoria": "Vinho",
        "preco": 60.00,
        "alcoolica": True,
        "ml": 750,
        "disponivel": True,
        "criado_em": "2024-06-01T12:25:00",
    },
]

@router.get("/")
async def listar_bebidas(tipo: str = None, alcoolica: bool = None):
    resultado = bebidas

    if tipo:
        resultado = [b for b in resultado if b.get("categoria").lower() == tipo.lower()]

    if alcoolica is not None:
        resultado = [b for b in resultado if b["alcoolica"] == alcoolica]

    # 👇 traduz categoria -> tipo
    return [
        {**b, "tipo": b["categoria"]} for b in resultado
    ]

@router.get("/{bebida_id}")
async def buscar_bebida(bebida_id: int):
    bebida = next((b for b in bebidas if b["id"] == bebida_id), None)

    if not bebida:
        raise HTTPException(status_code=404, detail="Bebida não encontrada")

    return bebida


@router.post("/", response_model=BebidaOutput)
async def criar_bebida(bebida: BebidaInput):

    novo_id = max(b["id"] for b in bebidas) + 1

    nova_bebida = {
        "id": novo_id,
        "criado_em": datetime.now().isoformat(),
        "categoria": bebida.categoria,  # 👈 conversão aqui
        "nome": bebida.nome,
        "preco": bebida.preco,
        "alcoolica": bebida.alcoolica,
        "ml": bebida.ml,
        "disponivel": bebida.disponivel,
    }

    bebidas.append(nova_bebida)

    return {**nova_bebida, "tipo": nova_bebida["categoria"]}
