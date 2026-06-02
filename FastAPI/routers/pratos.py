from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import os

import psycopg
from psycopg.rows import dict_row

from FastAPI.models.prato import PratoInput, PratoOutput

# PRATOS

router = APIRouter()
DATABASE_URL = os.getenv("DATABASE_URL")
_db_ready = False

pratos = [
    {
        "id": 1,
        "nome": "Margherita",
        "categoria": "pizza",
        "preco": 45.0,
        "disponivel": True,
    },
    {
        "id": 2,
        "nome": "Carbonara",
        "categoria": "massa",
        "preco": 52.0,
        "disponivel": False,
    },
    {
        "id": 3,
        "nome": "Tiramisù",
        "categoria": "sobremesa",
        "preco": 28.0,
        "disponivel": True,
    },
    {
        "id": 4,
        "nome": "Lasagna alla Bolognese",
        "categoria": "massa",
        "preco": 55.0,
        "disponivel": True,
    },
    {
        "id": 5,
        "nome": "Cannoli",
        "categoria": "sobremesa",
        "preco": 22.0,
        "disponivel": False,
    },
    {
        "id": 6,
        "nome": "Panna Cotta",
        "categoria": "sobremesa",
        "preco": 25.0,
        "disponivel": True,
    },
]


def _use_db():
    return bool(DATABASE_URL)


def _connect():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def _init_db():
    global _db_ready
    if _db_ready or not _use_db():
        return

    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS pratos (
                    id SERIAL PRIMARY KEY,
                    nome TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    preco DOUBLE PRECISION NOT NULL,
                    disponivel BOOLEAN NOT NULL DEFAULT TRUE,
                    criado_em TIMESTAMP NOT NULL DEFAULT NOW()
                )
                """
            )
            cur.execute("SELECT COUNT(*) AS total FROM pratos")
            if cur.fetchone()["total"] == 0:
                cur.executemany(
                    """
                    INSERT INTO pratos (nome, categoria, preco, disponivel)
                    VALUES (%(nome)s, %(categoria)s, %(preco)s, %(disponivel)s)
                    """,
                    pratos,
                )
        conn.commit()

    _db_ready = True


def _serialize_prato(row):
    item = dict(row)
    if hasattr(item.get("criado_em"), "isoformat"):
        item["criado_em"] = item["criado_em"].isoformat()
    return item


class DisponibilidadeInput(BaseModel):
    disponivel: bool


@router.get("/")
async def listar_pratos(
    categoria: Optional[str] = None,
    preco_maximo: Optional[float] = None,
    apenas_disponiveis: Optional[bool] = False,
):
    if _use_db():
        _init_db()
        query = "SELECT * FROM pratos WHERE TRUE"
        params = {}

        if categoria:
            query += " AND categoria = %(categoria)s"
            params["categoria"] = categoria

        if preco_maximo:
            query += " AND preco <= %(preco_maximo)s"
            params["preco_maximo"] = preco_maximo

        if apenas_disponiveis:
            query += " AND disponivel = TRUE"

        query += " ORDER BY id"
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return [_serialize_prato(row) for row in cur.fetchall()]

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
    if _use_db():
        _init_db()
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM pratos WHERE id = %s", (prato_id,))
                prato = cur.fetchone()

        if not prato:
            raise HTTPException(status_code=404, detail="Prato nÃ£o encontrado")

        prato = _serialize_prato(prato)
        if formato == "resumido":
            return {"nome": prato["nome"], "preco": prato["preco"]}
        return prato

    prato = next((p for p in pratos if p["id"] == prato_id), None)

    if not prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")

    if formato == "resumido":
        return {"nome": prato["nome"], "preco": prato["preco"]}

    return prato


@router.put("/{prato_id}/disponibilidade")
async def alterar_disponibilidade(prato_id: int, dados: DisponibilidadeInput):
    if _use_db():
        _init_db()
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE pratos
                    SET disponivel = %s
                    WHERE id = %s
                    RETURNING *
                    """,
                    (dados.disponivel, prato_id),
                )
                prato = cur.fetchone()
            conn.commit()

        if not prato:
            raise HTTPException(status_code=404, detail="Prato nÃ£o encontrado")

        return _serialize_prato(prato)

    prato = next((p for p in pratos if p["id"] == prato_id), None)

    if not prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")

    prato["disponivel"] = dados.disponivel
    return prato


@router.post("/", response_model=PratoOutput)
async def criar_prato(prato: PratoInput):
    if _use_db():
        _init_db()
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO pratos (nome, categoria, preco, disponivel)
                    VALUES (%s, %s, %s, %s)
                    RETURNING *
                    """,
                    (
                        prato.nome,
                        prato.categoria,
                        prato.preco,
                        prato.disponivel,
                    ),
                )
                novo_prato = cur.fetchone()
            conn.commit()

        return _serialize_prato(novo_prato)

    novo_id = max(p["id"] for p in pratos) + 1

    novo_prato = {
        "id": novo_id,
        "criado_em": datetime.now().isoformat(),
        **prato.model_dump(),
    }

    pratos.append(novo_prato)
    return novo_prato
