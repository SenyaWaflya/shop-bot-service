from httpx import AsyncClient

from src.schemas.carts import Cart
from src.settings import settings


class CartsApi:
    @staticmethod
    async def get_active(user_id: int) -> Cart:
        async with AsyncClient() as client:
            resp = await client.get(url=f'{settings.SHOP_BACKEND_API_URL}/carts/{user_id}')
            resp.raise_for_status()
            cart = Cart.model_validate(resp.json())
            return cart
