from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from ..core.memory import Memory


reset_router = Router()


@reset_router.message(Command('reset'))
async def reset(message: Message) -> None:
    user_id = message.from_user.id

    Memory(user_id).reset_memory()

    await message.reply("<b>😢 | Жаль, что ты стёр сомной историю.</b>")
