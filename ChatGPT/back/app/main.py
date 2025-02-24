from fastapi import FastAPI
from app.api.v1.routes import orders, users

app = FastAPI(
    title="Finance Simulator API",
    description="API para simulação do mercado financeiro",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Incluir rotas da API
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
