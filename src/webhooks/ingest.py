from fastapi import APIRouter, Request

router = APIRouter()

@router.post('/webhooks/ingest')
async def handle_webhook(request: Request):
    payload = await request.json()
    return {'status': 'ok', 'items': len(payload)}