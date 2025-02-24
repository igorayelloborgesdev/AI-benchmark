from fastapi import FastAPI
from app.interfaces.api.v1.ativos import router as ativos_router
from app.interfaces.api.v1.ordens import router as ordens_router

app = FastAPI(
    title="Simulador de Mercado Financeiro",
    description="API para simulação do mercado financeiro",
    version="1.0.0",
    docs_url="/docs",  # Habilita o Swagger em /docs
    redoc_url="/redoc",  # Habilita o ReDoc em /redoc
)

# Adiciona os routers
app.include_router(ativos_router)
app.include_router(ordens_router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Simulador de Mercado Financeiro"}