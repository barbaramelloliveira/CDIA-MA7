import pytest


@pytest.mark.integracao
def test_modelo_distingue_casos_extremos(client):
    """
    Teste de sanidade: verifica se o modelo diferencia
    um caso normal de um caso suspeito.
    """

    caso_normal = {
        "valor_transacao": 80.0,
        "hora_transacao": 14,
        "distancia_ultima_compra": 2.0,
        "tentativas_senha": 1,
        "pais_diferente": 0
    }

    caso_suspeito = {
        "valor_transacao": 2500.0,
        "hora_transacao": 3,
        "distancia_ultima_compra": 50.0,
        "tentativas_senha": 5,
        "pais_diferente": 1
    }

    resp_normal = client.post("/predict", json=caso_normal)
    resp_suspeito = client.post("/predict", json=caso_suspeito)

    assert resp_normal.status_code == 200
    assert resp_suspeito.status_code == 200

    prob_normal = resp_normal.json()["probability"]
    prob_suspeito = resp_suspeito.json()["probability"]

    assert prob_suspeito > prob_normal, (
        f"Esperado: suspeito ({prob_suspeito:.3f}) > normal ({prob_normal:.3f})"
    )

@pytest.mark.integracao
def test_modelo_e_deterministico(client):
    payload = {
        "valor_transacao": 200.0,
        "hora_transacao": 12,
        "distancia_ultima_compra": 5.0,
        "tentativas_senha": 1,
        "pais_diferente": 0
    }

    r1 = client.post("/predict", json=payload)
    r2 = client.post("/predict", json=payload)

    assert r1.json()["prediction"] == r2.json()["prediction"]
    assert r1.json()["probability"] == r2.json()["probability"]