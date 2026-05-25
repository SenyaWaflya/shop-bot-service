from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardBuilder,
)

from src.api.shop_backend.carts import CartsApi
from src.api.shop_backend.products import ProductsApi
from src.callbacks.brand import BrandCallback
from src.callbacks.cart import AddToCartCallback, CartCallback
from src.callbacks.product import ProductCallback

catalog = KeyboardButton(text='Каталог 🔍')
profile = KeyboardButton(text='Профиль 🧑‍💻')
cart = KeyboardButton(text='Корзина 🛒')
contacts = KeyboardButton(text='Контакты ℹ️')
main_kb = ReplyKeyboardBuilder([[catalog], [profile, cart], [contacts]]).as_markup(resize_keyboard=True)

prev_item = InlineKeyboardButton(text='⬅️', callback_data=CartCallback(action='prev').pack())
next_item = InlineKeyboardButton(text='➡️', callback_data=CartCallback(action='next').pack())
delete = InlineKeyboardButton(text='Убрать из корзины', callback_data=CartCallback(action='delete').pack())
order = InlineKeyboardButton(text='Оформить заказ', callback_data=CartCallback(action='order').pack())
cart_kb = InlineKeyboardBuilder().row(delete).row(prev_item, next_item).row(order).as_markup()


async def product_kb(product_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    to_cart = InlineKeyboardButton(
        text='Добавить в корзину 🛒', callback_data=ProductCallback(id=product_id, action='to_cart').pack()
    )
    back = InlineKeyboardButton(text='Назад ⏪', callback_data=ProductCallback(id=0, action='back').pack())
    return builder.row(to_cart, back).adjust(1).as_markup()


async def brands_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    brands = await ProductsApi.get_brands()
    for brand in brands:
        builder.button(text=brand, callback_data=BrandCallback(title=brand, action='open'))
    return builder.adjust(1).as_markup()


async def products_kb(brand: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    products = await ProductsApi.get_all()
    for product in products:
        if product.brand == brand:
            builder.button(
                text=product.title,
                callback_data=ProductCallback(id=product.id, action='open'),
            )
    builder.row(InlineKeyboardButton(text='Назад ⏪', callback_data=BrandCallback(title='all', action='back').pack()))
    return builder.adjust(1).as_markup()


async def quantity_of_product_kb(product_id: int, user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    active_cart = await CartsApi.get_active(user_id=user_id)
    if active_cart is None:
        product = await ProductsApi.get(product_id=product_id)
        for i in range(product.quantity):
            builder.button(
                text=str(i + 1),
                callback_data=AddToCartCallback(product_id=product_id, quantity=i + 1, action='add_to_cart'),
            )
    else:
        products_ids_in_cart = [item.product_id for item in active_cart.items]
        if product_id not in products_ids_in_cart:
            product = await ProductsApi.get(product_id=product_id)
            for i in range(product.quantity):
                builder.button(
                    text=str(i + 1),
                    callback_data=AddToCartCallback(product_id=product_id, quantity=i + 1, action='add_to_cart'),
                )
        else:
            for item in active_cart.items:
                if item.product.id == product_id:
                    for i in range(item.product.quantity - item.quantity):
                        builder.button(
                            text=str(i + 1),
                            callback_data=AddToCartCallback(product_id=product_id, quantity=i + 1, action='add_to_cart'),
                        )
    builder.row(
        InlineKeyboardButton(
            text='Назад ⏪', callback_data=AddToCartCallback(product_id=product_id, quantity=0, action='back').pack()
        )
    )
    return builder.as_markup()
