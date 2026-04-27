from fastapi.testclient import TestClient
from FastAPI.main import app  # ajuste se necessário

client = TestClient(app)


def test_listar_bebidas_retorna_200():
    response = client.get("/bebidas")
    assert response.status_code == 200


def test_listar_bebidas_retorna_lista():
    response = client.get("/bebidas")
    assert isinstance(response.json(), list)


def test_filtro_por_tipo():
    response = client.get("/bebidas?tipo=refrigerante")
    assert response.status_code == 200

    for bebida in response.json():
        assert bebida["tipo"] == "refrigerante"


def test_filtro_por_alcoolica():
    response = client.get("/bebidas?alcoolica=true")
    assert response.status_code == 200

    for bebida in response.json():
        assert bebida["alcoolica"] is True


def test_buscar_bebida_existente():
    response = client.get("/bebidas/1")
    assert response.status_code == 200

    dados = response.json()
    assert "id" in dados
    assert "nome" in dados


def test_buscar_bebida_inexistente():
    response = client.get("/bebidas/9999")
    assert response.status_code == 404


def test_criar_bebida_valida():
    payload = {
        "nome": "Suco Teste",
        "tipo": "suco",
        "preco": 12.5,
        "alcoolica": False
    }

    response = client.post("/bebidas", json=payload)
    assert response.status_code in [200, 201]


def test_criar_bebida_preco_negativo():
    payload = {
        "nome": "Erro",
        "tipo": "suco",
        "preco": -10,
        "alcoolica": False
    }

    response = client.post("/bebidas", json=payload)
    assert response.status_code == 422