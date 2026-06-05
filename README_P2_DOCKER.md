# Bella Tavola API - Entrega P2 Docker

## Rodar localmente sem Docker

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn FastAPI.main:app --reload
```

## Rodar com Docker

```bash
cp .env.example .env
docker build -t bella-tavola:v3 .
docker run --rm -p 8000:8000 --env-file .env bella-tavola:v3
```

Teste:

```bash
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/pratos
curl -X POST http://localhost:8000/ml/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"valor_transacao\":2500,\"hora_transacao\":3,\"distancia_ultima_compra\":50,\"tentativas_senha\":5,\"pais_diferente\":1}"
```

## Rodar com Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

Serviços:

- `api`: FastAPI Bella Tavola.
- `db`: PostgreSQL 15 com volume persistente.
- `nginx`: proxy reverso na porta 80.

Teste via Nginx:

```bash
curl http://localhost/
curl http://localhost/pratos
```

Para limpar contêineres sem apagar dados:

```bash
docker compose down
```

Para limpar também o banco de desenvolvimento:

```bash
docker compose down -v
```

## Publicar imagem no Docker Hub

Crie um repositório no Docker Hub chamado `bella-tavola` e gere um access token.

No GitHub, cadastre estes secrets em `Settings > Secrets and variables > Actions`:

- `DOCKER_USERNAME`: seu usuário do Docker Hub.
- `DOCKER_PASSWORD`: token de acesso do Docker Hub.

Push manual:

```bash
docker login
docker build -t SEU_USUARIO_DOCKER/bella-tavola:v1 .
docker push SEU_USUARIO_DOCKER/bella-tavola:v1
```

Publicação automática:

O arquivo `.github/workflows/ci.yml` tem o job `docker`, que roda em push para `main` depois de `full-tests`. Ele publica duas tags:

- `SEU_USUARIO_DOCKER/bella-tavola:${GITHUB_SHA}`
- `SEU_USUARIO_DOCKER/bella-tavola:latest`
