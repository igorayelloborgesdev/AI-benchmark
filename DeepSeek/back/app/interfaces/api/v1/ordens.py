from fastapi import APIRouter

router = APIRouter(prefix="/ordens", tags=["ordens"])

@router.get("/")
def listar_ordens():
    return {"message": "Lista de ordens"}