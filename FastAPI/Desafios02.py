from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

reservas = [
    {"id": 1, "mesa": 5, "nome": "Silva", "pessoas": 4, "ativa": True},
    {"id": 2, "mesa": 3, "nome": "Costa", "pessoas": 2, "ativa": False},
]

# ✅ Validação de entrada (robustez)
class ReservaInput(BaseModel):
    mesa: int = Field(gt=0)
    nome: str = Field(min_length=2, max_length=100)
    pessoas: int = Field(gt=0)


# ✅ GET por ID com 404 correto
@app.get("/reservas/{reserva_id}")
async def buscar_reserva(reserva_id: int):
    reserva = next((r for r in reservas if r["id"] == reserva_id), None)

    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")

    return reserva


# ✅ POST com geração de ID segura
@app.post("/reservas", status_code=201)
async def criar_reserva(reserva: ReservaInput):
    novo_id = max(r["id"] for r in reservas) + 1 if reservas else 1

    nova = {
        "id": novo_id,
        **reserva.model_dump(),
        "ativa": True
    }

    reservas.append(nova)
    return nova


# ✅ DELETE com tratamento de erro
@app.delete("/reservas/{reserva_id}")
async def cancelar_reserva(reserva_id: int):
    reserva = next((r for r in reservas if r["id"] == reserva_id), None)

    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")

    reserva["ativa"] = False

    return {"mensagem": "Reserva cancelada com sucesso"}


# ✅ GET com filtro correto
@app.get("/reservas")
async def listar_reservas(apenas_ativas: bool = False):
    if apenas_ativas:
        return [r for r in reservas if r["ativa"]]

    return reservas