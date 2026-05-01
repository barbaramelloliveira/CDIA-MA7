from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime, timedelta


class ReservaBase(BaseModel):
    nome: str = Field(..., min_length=2)
    mesa: int = Field(..., gt=0)
    pessoas: int = Field(..., gt=0)
    data_hora: datetime


class ReservaCreate(ReservaBase):

    @field_validator("data_hora")
    @classmethod
    def validar_antecedencia(cls, value: datetime):
        if value < datetime.now() + timedelta(hours=1):
            raise ValueError(
                "Reserva deve ser feita com pelo menos 1 hora de antecedência"
            )
        return value


class Reserva(ReservaBase):
    id: int
    status: str = "ativa"

    model_config = ConfigDict(from_attributes=True)
