from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.api.shop_backend.users import UsersApi
from src.kb import main_kb
from src.schemas.users import UserDto

users_router = Router(name='users')


@users_router.message(CommandStart())
async def start(message: Message) -> None:
    user_dto = UserDto(tg_id=message.from_user.id, username=message.from_user.username)
    await UsersApi.add(user_dto)
    await message.answer(text=f'Привет, <b>{message.from_user.first_name}</b>', reply_markup=main_kb)


@users_router.message(F.text == 'Профиль 🧑‍💻')
async def show_profile(message: Message) -> None:
    user = await UsersApi.get(message.from_user.id)
    await message.answer(text=f'Имя пользователя: {user.username}\nTelegram ID: {user.tg_id}')


@users_router.message(F.text == 'Контакты ℹ️')
async def show_contacts(message: Message) -> None:
    await message.answer(
        text='По вопросам писать:\nTelegram : @golychh\nEmail: fathat2013.ag@gmail.com\nТелефон: +7(977)108-82-48'
    )
