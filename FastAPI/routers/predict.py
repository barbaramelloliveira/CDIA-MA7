from fastapi import APIRouter
from pydantic import BaseModel, Field
import numpy as np

router = APIRouter()

REPO_ID = "Barbz2605/fraud-detector-v1"
_model = None

def get_model():
    global _model
    if _model is None:
        from projeto_mlops.model_utils import load_model
        _model = load_model(REPO_ID)
    return _model


class PredictInput(BaseModel):
    valor_transacao: float = Field(gt=0)
    hora_transacao: int = Field(ge=0, le=23)
    distancia_ultima_compra: float = Field(ge=0)
    tentativas_senha: int = Field(ge=1)
    pais_diferente: int = Field(ge=0, le=1)


class PredictOutput(BaseModel):
    prediction: int
    probability: float
    label: str
    model_version: str


@router.post("/predict", response_model=PredictOutput)
async def predict(input: PredictInput):
    model = get_model()

    features = np.array([[
        input.valor_transacao,
        input.hora_transacao,
        input.distancia_ultima_compra,
        input.tentativas_senha,
        input.pais_diferente
    ]])

    prediction = int(model.predict(features)[0])
    probability = float(model.predict_proba(features)[0][0])

    label = "fraude" if prediction == 0 else "legitimo"

    return PredictOutput(
        prediction=prediction,
        probability=round(probability, 4),
        label=label,
        model_version=REPO_ID
    )

@router.get("/health")
async def health():
    try:
        model = get_model()

        # input fake só pra testar se o modelo responde
        test_input = np.zeros((1, 5))
        model.predict(test_input)

        model_status = "ok"
        model_info = REPO_ID

    except Exception as e:
        model_status = "degraded"
        model_info = str(e)

    return {
        "api": "ok",
        "model": model_status,
        "model_repo": model_info
    }
