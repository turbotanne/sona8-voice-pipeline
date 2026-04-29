from fastapi import APIRouter

router = APIRouter()

@router.get('/metrics')
def get_metrics():
    return {"latency": 4.2}