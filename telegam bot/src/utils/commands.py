from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from config import Config

async def set_commands(bot: Bot):
    admincommands = [
        BotCommand(
            command='start',
            description='панель игроков'
        ),
        BotCommand(
            command='admin_panel',
            description='админ панель'
        ),
        BotCommand(
            command='add_mag',
            description='Создать персонажа'
        )
        ,
        BotCommand(
            command='update_admin',
            description='Обновить список администраторов'
        )
    ]
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='add_mag',
            description='Создать персонажа'
        )

    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
    #await bot.set_my_commands(admincommands, BotCommandScopeChat(chat_id=Config.admin_id))
    for i in Config.admins_id:
        await bot.set_my_commands(admincommands, BotCommandScopeChat(chat_id=i))
