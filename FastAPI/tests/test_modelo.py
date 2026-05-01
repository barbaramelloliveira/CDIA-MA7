import pytest
import numpy as np

from projeto_mlops.model_utils import load_model

REPO_ID = "Barbz2605/fraud-detector-v1"


# 👇 carrega o modelo UMA vez (melhor prática de CI)
@pytest.fixture(scope="module")
def modelo():
    return load_model(REPO_ID)


# 👇 amostra mais limpa e reutilizável
@pytest.fixture
def amostra_valida():
    return np.array([[250.0, 14, 12.5, 1, 0]])


# -----------------------------
# TESTES
# -----------------------------

@pytest.mark.integracao
def test_modelo_nao_e_none(modelo):
    assert modelo is not None


@pytest.mark.integracao
def test_modelo_tem_predict(modelo):
    assert hasattr(modelo, "predict")
    assert callable(modelo.predict)


@pytest.mark.integracao
def test_modelo_tem_predict_proba(modelo):
    assert hasattr(modelo, "predict_proba")
    assert callable(modelo.predict_proba)


@pytest.mark.integracao
def test_predict_formato_saida(modelo, amostra_valida):
    resultado = modelo.predict(amostra_valida)

    assert isinstance(resultado, np.ndarray)
    assert resultado.shape == (1,)


@pytest.mark.integracao
def test_predict_proba_formato(modelo, amostra_valida):
    probas = modelo.predict_proba(amostra_valida)

    assert isinstance(probas, np.ndarray)
    assert probas.shape[0] == 1
    assert probas.shape[1] >= 2
    assert abs(probas[0].sum() - 1.0) < 1e-6

import pytest
import numpy as np

from projeto_mlops.model_utils import load_model

REPO_ID = "Barbz2605/fraud-detector-v1"


@pytest.fixture(scope="module")
def modelo():
    return load_model(REPO_ID)


@pytest.fixture
def amostra_valida():
    return np.array([[250.0, 14, 12.5, 1, 0]])


@pytest.mark.integracao
def test_modelo_nao_e_none(modelo):
    assert modelo is not None


@pytest.mark.integracao
def test_modelo_tem_predict(modelo):
    assert hasattr(modelo, "predict")
    assert callable(modelo.predict)


@pytest.mark.integracao
def test_modelo_tem_predict_proba(modelo):
    assert hasattr(modelo, "predict_proba")
    assert callable(modelo.predict_proba)


@pytest.mark.integracao
def test_predict_formato_saida(modelo, amostra_valida):
    resultado = modelo.predict(amostra_valida)

    assert isinstance(resultado, np.ndarray)
    assert resultado.shape == (1,)


@pytest.mark.integracao
def test_predict_proba_formato(modelo, amostra_valida):
    probas = modelo.predict_proba(amostra_valida)

    assert isinstance(probas, np.ndarray)
    assert probas.shape[0] == 1
    assert probas.shape[1] >= 2
    assert abs(probas[0].sum() - 1.0) < 1e-6


# ============================
# TESTES DO ENDPOINT
# ============================

PAYLOAD_VALIDO = {
    "valor_transacao": 120.0,
    "hora_transacao": 20,
    "distancia_ultima_compra": 2.5,
    "tentativas_senha": 1,
    "pais_diferente": 0
}


@pytest.mark.integracao
def test_predict_retorna_200(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    assert response.status_code == 200


@pytest.mark.integracao
def test_predict_campos_existem(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)

    dados = response.json()

    assert "prediction" in dados
    assert "probability" in dados
    assert "label" in dados
    assert "model_version" in dados


@pytest.mark.integracao
def test_predict_binario(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)

    prediction = response.json()["prediction"]
    assert prediction in [0, 1]


@pytest.mark.integracao
def test_probability_intervalo(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)

    prob = response.json()["probability"]
    assert isinstance(prob, float)
    assert 0.0 <= prob <= 1.0


@pytest.mark.integracao
def test_label_valido(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)

    label = response.json()["label"]
    assert isinstance(label, str)
    assert len(label) > 0