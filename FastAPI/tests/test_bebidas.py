import pytest


def test_listar_bebidas_retorna_200(client):
    response = client.get("/bebidas")
    assert response.status_code == 200


def test_listar_bebidas_retorna_lista(client):
    response = client.get("/bebidas")
    assert isinstance(response.json(), list)


def test_filtro_por_tipo(client):
    response = client.get("/bebidas?tipo=refrigerante")
    assert response.status_code == 200

    for bebida in response.json():
        assert bebida["tipo"].lower() == "refrigerante"   # ⚠️ corrigido


def test_filtro_por_alcoolica(client):
    response = client.get("/bebidas?alcoolica=true")
    assert response.status_code == 200

    for bebida in response.json():
        assert bebida["alcoolica"] is True


def test_buscar_bebida_existente(client):
    response = client.get("/bebidas/1")
    assert response.status_code == 200

    dados = response.json()
    assert "id" in dados
    assert "nome" in dados


def test_buscar_bebida_inexistente(client):
    response = client.get("/bebidas/9999")
    assert response.status_code == 404


def test_criar_bebida_valida(client):
    payload = {
        "nome": "Água Teste",
        "categoria": "agua",
        "preco": 10.0,
        "alcoolica": False,
        "ml": 500,
        "disponivel": True
    }

    response = client.post("/bebidas", json=payload)
    print(response.json())

    assert response.status_code in [200, 201]


def test_criar_bebida_preco_negativo(client):
    payload = {
        "nome": "Erro",
        "tipo": "suco",
        "preco": -10,
        "alcoolica": False
    }

    response = client.post("/bebidas", json=payload)
    assert response.status_code == 422

