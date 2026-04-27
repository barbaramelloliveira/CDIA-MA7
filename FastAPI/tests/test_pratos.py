from fastapi.testclient import TestClient
from FastAPI.main import app  # 👈 ajuste aqui

client = TestClient(app)


def test_listar_pratos_retorna_200():
    response = client.get("/pratos")
    assert response.status_code == 200


def test_listar_pratos_retorna_lista():
    response = client.get("/pratos")
    assert isinstance(response.json(), list)


def test_listar_pratos_retorna_pelo_menos_um_prato():
    response = client.get("/pratos")
    assert len(response.json()) > 0


def test_filtro_por_categoria_retorna_apenas_categoria_correta():
    response = client.get("/pratos?categoria=pizza")
    assert response.status_code == 200
    pratos = response.json()
    for prato in pratos:
        assert prato["categoria"] == "pizza"


def test_buscar_prato_existente_retorna_campos_esperados():
    response = client.get("/pratos/1")
    assert response.status_code == 200
    prato = response.json()
    assert "id" in prato
    assert "nome" in prato
    assert "preco" in prato


def test_buscar_prato_inexistente_retorna_404():
    response = client.get("/pratos/9999")
    assert response.status_code == 404

def test_criar_prato_valido_retorna_sucesso():
    novo_prato = {
        "nome": "Pizza Teste 123",
        "categoria": "pizza",
        "preco": 59.9,
        "disponivel": True
    }

    response = client.post("/pratos", json=novo_prato)

    assert response.status_code in [200, 201]

    data = response.json()
    assert data["nome"] == "Pizza Teste 123"
    assert data["categoria"] == "pizza"
    assert data["preco"] == 59.9

def test_criar_prato_preco_negativo_retorna_422():
    prato_invalido = {
        "nome": "Pizza Invalida",
        "categoria": "pizza",
        "preco": -10.0
    }

    response = client.post("/pratos", json=prato_invalido)

    assert response.status_code == 422

def test_criar_prato_com_nome_curto_retorna_422():
    prato_invalido = {
        "nome": "AB",   # menos de 3 caracteres
        "categoria": "pizza",
        "preco": 40.0
    }
    response = client.post("/pratos", json=prato_invalido)
    assert response.status_code == 422

def test_criar_prato_categoria_invalida_retorna_422():
    prato_invalido = {
        "nome": "Prato Teste Categoria",
        "categoria": "sobremesa_errada",  # ❌ inválida
        "preco": 25.0
    }

    response = client.post("/pratos", json=prato_invalido)

    assert response.status_code == 422

def test_prato_criado_aparece_na_listagem():
    # Nome único para não colidir com outros testes ou dados iniciais
    nome_unico = "Tagliatelle Teste XYZ-9871"
    
    client.post("/pratos", json={
        "nome": nome_unico,
        "categoria": "massa",
        "preco": 68.0
    })

    response = client.get("/pratos")
    nomes = [p["nome"] for p in response.json()]

    assert nome_unico in nomes