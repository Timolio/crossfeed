import os
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from db import queries

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await queries.upsert_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Открыть приложение",
            web_app=WebAppInfo(url=os.getenv("WEBAPP_URL")),
        )
    ]])

    await message.answer("Привет! Открой Mini App чтобы добавить канал:", reply_markup=keyboard)
