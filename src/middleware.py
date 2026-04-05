from fastapi import Request

async def log_request(request: Request):
    return await request.body()