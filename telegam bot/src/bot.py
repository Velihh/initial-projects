import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler_di import ContextSchedulerDecorator
#from aiogram.methods.get_chat_administrators import GetChatAdministrators
from config import Config


import asyncio
bot = Bot(Config.token, parse_mode='HTML')
jobstores = {
    'default': RedisJobStore(jobs_key='dispatched_trips_jobs6',
                             run_times_key='example.run_times5',
                             db=2,
                             port=6379)}

from handlers import user
from handlers import collecting_charges
from handlers import enchantment
from handlers import ritual
from handlers import registration
from handlers import admin
from handlers import geo
from services import swift
from services.sched_file import distrit_acive
from handlers import us_swift
from utils.commands import set_commands
from middlewares.middleware_ALL import SchedulerMiddleware


storage = RedisStorage.from_url('redis://localhost:6379/0')
scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone="Asia/Yekaterinburg", jobstores=jobstores))

async def on_startup():
    #logging.basicConfig(level=logging.INFO,
     #                   format="%(asctime)s - [%(levelname)s] - %(name)s - "
      #                         "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    await Config.db.stop_live_all()
    await distrit_acive(scheduler)
    t = await bot.get_chat_administrators(Config.chatMG_id)
    admins = []
    for i in t:
        if i.user.id != 6043223939:
            admins.append(i.user.id)
    Config.admins_id = admins
    await set_commands(bot)
    await bot.send_message(chat_id=Config.admin_id, text='Идет разработка')




async def main():
    dp = Dispatcher(bot=bot, storage=storage)
    scheduler.start()
    # dp.message.middleware.register(ChatActionMiddleware())
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    dp.startup.register(on_startup)
    dp.include_router(geo.router)
    dp.include_router(user.router)
    dp.include_router(collecting_charges.router)
    dp.include_router(enchantment.router)
    dp.include_router(ritual.router)
    dp.include_router(registration.router)
    dp.include_router(admin.router)
    dp.include_router(swift.router)
    dp.include_router(us_swift.router)
    try:
        await dp.start_polling(bot, timeout=200)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped!')
