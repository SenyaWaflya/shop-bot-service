from httpx import AsyncClient

from src.settings import settings


class ProductsApi:
    @staticmethod
    async def get_all() -> list[dict]:
        async with AsyncClient() as client:
            resp = await client.get(f'{settings.API_URL}/products/')
            return resp.json()

    @staticmethod
    async def get(product_id: int) -> dict:
        async with AsyncClient() as client:
            resp = await client.get(f'{settings.API_URL}/products/{product_id}')
            return resp.json()

    @staticmethod
    async def get_brands() -> list[str]:
        async with AsyncClient() as client:
            resp = await client.get(f'{settings.API_URL}/products/brands')
            return resp.json()
