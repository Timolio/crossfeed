from aiogram import Router, F, Bot
from aiogram.types import ChatMemberUpdated
from db import queries
from api.websocket import manager

router = Router()


@router.my_chat_member(F.new_chat_member.status == "administrator")
async def bot_added_to_channel(update: ChatMemberUpdated, bot: Bot):
    chat = update.chat
    user = update.from_user

    if chat.type not in ("channel", "supergroup"):
        return

    await queries.create_channel(
        channel_id=chat.id,
        owner_id=user.id,
        username=getattr(chat, "username", None),
        title=chat.title,
    )

    await bot.send_message(
        user.id,
        f'Отлично! Вы добавили бота в канал {chat.title} (@{chat.username}). Закончи настройку в mini app.',
    )

    channels = await queries.get_user_channels(user.id)
    new_channel = channels[-1]
    new_channel["id"] = str(new_channel["id"])
    new_channel["owner_id"] = str(new_channel["owner_id"])
    if new_channel.get("created_at"):
        new_channel["created_at"] = new_channel["created_at"].isoformat()

    await manager.send_to_user(user.id, {
        "event": "channel_added",
        "channel": new_channel,
    })
