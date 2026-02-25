from aiogram.filters.callback_data import CallbackData


class AddToCartCallback(CallbackData, prefix='add_to_cart'):
    product_id: int
    quantity: int
    action: str


class CartCallback(CallbackData, prefix='cart'):
    action: str
