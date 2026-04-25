from pydantic import BaseModel, Field

class BebidaInput(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    categoria: str = Field(pattern="^(vinho|agua|refrigerante|suco|cerveja)$")
    preco: float = Field(gt=0)
    alcoolica: bool
    ml: int = Field(ge=50, le=2000)
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