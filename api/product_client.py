import os
import httpx
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()
PRODUCT_SERVICE_URL = os.getenv('PRODUCT_SERVICE_URL', 'http://127.0.0.1:8001')

async def get_product(product_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{PRODUCT_SERVICE_URL}/products/{product_id}/')
    if response.status_code != 200:
        raise HTTPException(detail='Такого продукта нету', status_code=404)
    return response.json()