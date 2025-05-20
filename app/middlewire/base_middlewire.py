import os
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

from ...config_reader import config


class MainMiddlware(BaseMiddleware):
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        user_id = str(event.from_user.id)
        whitelist_path = "AIO-Natsuki/app/white_list"
        owner_ids = config.owner.get_secret_value().split(",")

        if user_id in owner_ids:
            return await handler(event, data)

        matching_files = [f for f in os.listdir(whitelist_path) if user_id in f]

        if not matching_files:
            await event.reply("Э, ты чего лезешь? Вообще офигел? Я люблю только @korol044! А ты.. Брысь отсюда..")
            return

        return await handler(event, data)