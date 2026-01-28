from aiogram.filters.callback_data import CallbackData


class ProductCallback(CallbackData, prefix='product'):
    id: int
    action: str
