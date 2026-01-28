from aiogram.filters.callback_data import CallbackData


class BrandCallback(CallbackData, prefix='brand'):
    title: str
    action: str
