from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_orders():
    return {"message": "List of orders"}

@router.post("/")
def create_order(order: dict):
    return {"message": "Order created", "order": order}
