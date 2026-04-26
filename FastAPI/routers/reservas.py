from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime

from FastAPI.models.reserva import Reserva, ReservaCreate
from FastAPI.config import settings

router = APIRouter()

reservas = []
contador_id = 1


@router.post("/", response_model=Reserva)
def criar_reserva(reserva: ReservaCreate):
    global contador_id

    # REGRA 1: limite de pessoas
    if reserva.pessoas > settings.max_pessoas_por_mesa:
        raise HTTPException(
            status_code=400, detail="Número de pessoas excede o permitido por mesa"
        )

    # REGRA 2: não pode duplicar mesa no mesmo dia
    for r in reservas:
        if (
            r.mesa == reserva.mesa
            and r.data_hora.date() == reserva.data_hora.date()
            and r.status == "ativa"
        ):
            raise HTTPException(
                status_code=400,
                detail="Já existe uma reserva ativa para essa mesa nesse dia",
            )

    nova_reserva = Reserva(id=contador_id, **reserva.model_dump())

    reservas.append(nova_reserva)
    contador_id += 1

    return nova_reserva


@router.get("/", response_model=List[Reserva])
def listar_reservas(
    data: Optional[datetime] = Query(None), status: Optional[str] = Query("ativa")
):
    resultado = reservas

    if status:
        resultado = [r for r in resultado if r.status == status]

    if data:
        resultado = [r for r in resultado if r.data_hora.date() == data.date()]

    return resultado


@router.get("/{reserva_id}", response_model=Reserva)
def buscar_reserva(reserva_id: int):
    for r in reservas:
        if r.id == reserva_id:
            return r

    raise HTTPException(status_code=404, detail="Reserva não encontrada")


@router.delete("/{reserva_id}")
def cancelar_reserva(reserva_id: int):
    for r in reservas:
        if r.id == reserva_id:
            r.status = "cancelada"
            return {"mensagem": "Reserva cancelada"}

    raise HTTPException(status_code=404, detail="Reserva não encontrada")


@router.get("/mesa/{numero}", response_model=List[Reserva])
def reservas_por_mesa(numero: int):
    return [r for r in reservas if r.mesa == numero]
