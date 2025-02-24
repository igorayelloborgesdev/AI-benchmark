from fastapi import APIRouter

router = APIRouter(prefix="/ativos", tags=["ativos"])

@router.get("/")
def listar_ativos():
    return {"message": "Lista de ativos"}