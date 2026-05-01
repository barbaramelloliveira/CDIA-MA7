import pytest

@pytest.mark.contrato
def test_contrato_get_prato(client):
    response = client.get("/pratos/1")
    assert response.status_code == 200

    prato = response.json()

    campos_obrigatorios = {"id", "nome", "categoria", "preco", "disponivel"}
    assert campos_obrigatorios.issubset(prato.keys())

    assert isinstance(prato["id"], int)
    assert isinstance(prato["nome"], str)
    assert isinstance(prato["categoria"], str)
    assert isinstance(prato["preco"], (int, float))
    assert isinstance(prato["disponivel"], bool)

    assert prato["preco"] > 0
    assert len(prato["nome"]) >= 3


def test_contrato_post_prato(client):
    novo = {
        "nome": "Prato Contrato Teste",
        "categoria": "massa",
        "preco": 45.0
    }

    response = client.post("/pratos", json=novo)
    assert response.status_code in [200, 201]

    prato = response.json()

    assert "id" in prato
    assert isinstance(prato["id"], int)
    assert prato["nome"] == novo["nome"]
    assert prato["categoria"] == novo["categoria"]
    assert prato["preco"] == novo["preco"]

    # campo opcional
    if "disponivel" in prato:
        assert isinstance(prato["disponivel"], bool)

    if "criado_em" in prato:
        assert isinstance(prato["criado_em"], str)
        assert len(prato["criado_em"]) > 0


def test_contrato_erro_404(client):
    response = client.get("/pratos/9999")
    assert response.status_code == 404

    corpo = response.json()

    assert "detail" in corpo or "erro" in corpo

    mensagem = corpo.get("detail") or corpo.get("erro")
    assert isinstance(mensagem, str)
    assert len(mensagem) > 0


def test_contrato_erro_422(client):
    response = client.post("/pratos", json={
        "nome": "X",   # inválido
        "preco": -1    # inválido
    })

    assert response.status_code == 422

    corpo = response.json()

    erros = corpo.get("detail") or corpo.get("detalhes")
    assert erros is not None

    assert isinstance(erros, list)
    assert len(erros) > 0

    # valida estrutura padrão FastAPI
    if "detail" in corpo:
        for erro in erros:
            assert "loc" in erro
            assert "msg" in erro

            assert isinstance(erro["loc"], list)
            assert isinstance(erro["msg"], str)
            assert len(erro["msg"]) > 0