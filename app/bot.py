from aiogram import Dispatcher, Router, Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from ..config_reader import config
from .handlers import natsuki_router, reset_router, white_list_router
from .middlewire.base_middlewire import MainMiddlware


async def main() -> None:
    dp = Dispatcher()
    bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    dp.include_routers(
        reset_router,
        white_list_router,
        natsuki_router
        
    )

    reset_router.message.middleware(MainMiddlware())
    white_list_router.message.middleware(MainMiddlware())
    natsuki_router.message.middleware(MainMiddlware())

    owner_ids = config.owner.get_secret_value().split(",")
    async with bot:
        for chat_id in owner_ids:
            print("chat_id:", chat_id)
            await bot.send_message(
                chat_id=int(chat_id.strip()),
                text="<b>Твоя Нацуки бодра добрости, и снова разаработала!</b>"
            )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)