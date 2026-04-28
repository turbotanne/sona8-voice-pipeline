from fastapi import APIRouter

router = APIRouter()

@router.post('/events')
def create_event(event: dict):
    return event