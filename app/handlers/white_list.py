from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import CommandObject, Command

import os
white_list_router = Router()


@white_list_router.message(Command("wh"))
async def wh_list(message: Message, command: CommandObject) -> None:
    arg = command.args.split()

    try:
        if arg[0] == '+':
            open(f"AIO-Natsuki/app/white_list/{arg[1]}", "w")
            await message.reply(f"<b>Я добавила того индивида в свой белый список...</b>")
        else:
            os.remove(f"AIO-Natsuki/app/white_list/{arg[1]}")
            await message.reply(f"<b>Ну и пусть.. Я не хочу видеть этого придурка больше!!!</b>")
    except Exception as e:
            await message.reply(f"<b>Я... СЛОМАЛАСЬ!!!!\n{e}</b>")


