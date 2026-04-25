import httpx

async def post_alert(webhook_url: str, text: str):
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(webhook_url, json={"text": text})