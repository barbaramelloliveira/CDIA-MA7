from fastapi import APIRouter, HTTPException
from FastAPI.models.pedidos import PedidoInput

# IMPORTANTE: importa os pratos do outro módulo
from FastAPI.routers.pratos import pratos

router = APIRouter()


@router.post("/", status_code=201)
async def criar_pedido(pedido: PedidoInput):

    prato = next((p for p in pratos if p["id"] == pedido.prato_id), None)

    if not prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")

    if not prato["disponivel"]:
        raise HTTPException(status_code=400, detail="Prato indisponível")

    valor_total = prato["preco"] * pedido.quantidade

    return {
        "prato": prato["nome"],
        "quantidade": pedido.quantidade,
        "observacao": pedido.observacao,
        "valor_total": valor_total,
    }
