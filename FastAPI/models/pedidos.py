from pydantic import BaseModel, Field
from typing import Optional


class PedidoInput(BaseModel):
    prato_id: int
    quantidade: int = Field(gt=0)
    observacao: Optional[str] = None
