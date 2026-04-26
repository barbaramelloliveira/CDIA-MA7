from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from FastAPI.config import settings

from FastAPI.routers import bebidas, pratos, reservas, pedidos
from FastAPI.routers.predict import router as predict_router

app = FastAPI(title=settings.app_name, version=settings.app_version)

# 🔗 ROUTERS
app.include_router(pratos.router, prefix="/pratos", tags=["Pratos"])
app.include_router(bebidas.router, prefix="/bebidas", tags=["Bebidas"])
app.include_router(pedidos.router, prefix="/pedidos", tags=["Pedidos"])
app.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])
app.include_router(predict_router, prefix="/ml", tags=["ML"])


# EXCEPTIONS
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "erro": "Dados inválidos",
            "status": 422,
            "path": str(request.url),
            "detalhes": exc.errors(),
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "erro": exc.detail,
            "status": exc.status_code,
            "path": str(
                request.url,
            ),
            "detalhes": [{"msg": exc.detail}],
        },
    )


# ROOT
@app.get("/")
async def root():
    return {
        "restaurante": "Bella Tavola",
        "mensagem": "Bem-vindo à nossa API",
        "chef": "Bárbara Passini",
        "cidade": "São Paulo",
        "especialidade": "Culinária Italiana",
    }
