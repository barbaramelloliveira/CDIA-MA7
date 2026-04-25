from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# 1.1
app = FastAPI(
    title="Bella Tavola API",
    description="API do restaurante Bella Tavola",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "restaurante": "Bella Tavola",
        "mensagem": "Bem-vindo à nossa API",
        "chef": "Bárbara Passini",
        "cidade": "São Paulo",
        "especialidade": "Culinária Italiana"
    }

#1.2 pratos
pratos = [
    {"id": 1, "nome": "Margherita", "categoria": "pizza", "preco": 45.0, "disponivel": True},
    {"id": 2, "nome": "Carbonara", "categoria": "massa", "preco": 52.0, "disponivel": False},
    {"id": 3, "nome": "Tiramisù", "categoria": "sobremesa", "preco": 28.0, "disponivel": True},
    {"id": 4, "nome": "Lasagna alla Bolognese", "categoria": "massa", "preco": 55.0, "disponivel": True},
    {"id": 5, "nome": "Cannoli", "categoria": "sobremesa", "preco": 22.0, "disponivel": False},
    {"id": 6, "nome": "Panna Cotta", "categoria": "sobremesa", "preco": 25.0, "disponivel": True},
]

#1.6 e 1.7 pydantic models
class PratoInput(BaseModel):
    nome: str
    categoria: str
    preco: float
    descricao: Optional[str] = None
    disponivel: bool = True

class PratoOutput(BaseModel):
    id: int
    nome: str
    categoria: str
    preco: float
    descricao: Optional[str] = None
    disponivel: bool
    criado_em: str

#Rotas para pratos
#1.4 e 1.5
@app.get("/pratos")
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

#1.3 e 1.5
@app.get("/pratos/{prato_id}")
async def buscar_prato(prato_id: int, formato: str = "completo"):
    for prato in pratos:
        if prato["id"] == prato_id:
            if formato == "resumido":
                return {"nome": prato["nome"], "preco": prato["preco"]}
            return prato
    return {"mensagem": "Prato não encontrado"}

    # Quando aparece o status 200 para um recuso que não existe, os cliente que só verificando o status code podem pensar que a requisição foi bem sucedida
    # Para evitar isso, é recomendado retornar um status code 404 para recursos não encontrados
    # return {"mensagem": "Prato não encontrado"}, 404

@app.post("/pratos", response_model=PratoOutput)
async def criar_prato(prato: PratoInput):
    from datetime import datetime
    novo_id = max(p["id"] for p in pratos) + 1
    novo_prato = {
        "id": novo_id,
        "criado_em": datetime.now().isoformat(),
        **prato.model_dump()
    }
    pratos.append(novo_prato)
    return novo_prato

#1.8
bebidas =[
    {"id": 1, "nome": "Água Mineral", "categoria": "Água", "preco": 6.00, "alcoolica": False, "ml": 500, "disponivel": True, "criado_em": "2024-06-01T12:00:00"},
    {"id": 2, "nome": "Coca-Cola", "categoria": "Refrigerante", "preco": 10.00, "alcoolica": False, "ml": 350, "disponivel": True, "criado_em": "2024-06-01T12:05:00"},
    {"id": 3, "nome": "Suco de Laranja", "categoria": "Suco", "preco": 12.00, "alcoolica": False, "ml": 300, "disponivel": False, "criado_em": "2024-06-01T12:10:00"},
    {"id": 4, "nome": "Cerveja", "categoria": "Cerveja", "preco": 15.00, "alcoolica": True, "ml": 500, "disponivel": True, "criado_em": "2024-06-01T12:15:00"},
    {"id": 5, "nome": "Vinho Tinto", "categoria": "Vinho", "preco": 50.00, "alcoolica": True, "ml": 750, "disponivel": False, "criado_em": "2024-06-01T12:20:00"},
    {"id": 6, "nome": "Espumante", "categoria": "Vinho", "preco": 60.00, "alcoolica": True, "ml": 750, "disponivel": True, "criado_em": "2024-06-01T12:25:00"}
]

@app.get("/bebidas")
async def listar_bebidas(
    categoria: Optional[str] = None,
    alcoolica: Optional[bool] = None
):

    resultado = bebidas

    if categoria:
        resultado = [b for b in resultado if b["categoria"] == categoria]

    if alcoolica is not None:
        resultado = [b for b in resultado if b["alcoolica"] == alcoolica]

    return resultado

@app.get("/bebidas/{bebida_id}")
async def buscar_bebida(bebida_id: int):

    for bebida in bebidas:
        if bebida["id"] == bebida_id:
            return bebida

    return {"mensagem": "Bebida não encontrada"}

class BebidaInput(BaseModel):
    nome: str
    categoria: str
    preco: float
    alcoolica: bool
    ml: int
    disponivel: bool = True

class BebidaOutput(BaseModel):
    id: int
    nome: str
    categoria: str
    preco: float
    alcoolica: bool
    ml: int
    disponivel: bool
    criado_em: str


@app.post("/bebidas", response_model=BebidaOutput)
async def criar_bebida(bebida: BebidaInput):

    novo_id = max(b["id"] for b in bebidas) + 1

    nova_bebida = {
        "id": novo_id,
        "criado_em": datetime.now().isoformat(),
        **bebida.model_dump()
    }

    bebidas.append(nova_bebida)

    return nova_bebida