from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, CallbackGame, chat
from aiogram.fsm.context import FSMContext
from aiogram.filters import  Text, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from aiogram.filters.callback_data import CallbackData
from typing import Optional
import re
from random import choice
from aiogram.utils.keyboard import InlineKeyboardBuilder
import datetime
from aiogram.filters.state import State
import asyncio
import aioschedule as schedule
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import Config
from states.user import *

from src.bot import bot

async def dis_acive(id_):
    now = datetime.now()
    print(now)
    await Config.db.up_acive_dis(int(id_))


async def distrit_acive(apscheduler: AsyncIOScheduler):
    dis = await Config.db.get_dis()
    for i in dis:
        id = i[0] + 'dis'
        try:
            apscheduler.add_job(func=dis_acive, id=id, trigger='interval', minutes=int(i[1]), kwargs={"id_": i[0]})
        except:
            apscheduler.reschedule_job(job_id=id, trigger="interval", minutes=int(i[1]))

async def pc():
    print(datetime.now())
    await Config.db.haos()

async def aure_acive(apscheduler: AsyncIOScheduler):
    df = await Config.dbGeoUs.acive_mark()
    shed = apscheduler
    for i in df:
        try:
            shed.add_job(func=aure_acive1, id=i[0], trigger='interval', minutes=int(i[3]), kwargs={"id_us": i[1], "scan": i[2], 'id_m':i[0]})
        except:
            print(f'данное задание уже запущенно')




async def aure_stop(apscheduler):
    df = await Config.dbGeoUs.acive_mark_stop()
    print(df)
    shed = apscheduler
    for i in df:
        try:
            shed.remove_job(job_id=i[0])
        except:
            print('Задание уже удалено')

async def recovery(id_tg):
    await Config.dbGeoUs.up_recovery(id_tg)
    await bot.send_message(id_tg, 'Ты ощущаешь прилив сил и жажду деятельности [Все надрывы и их эффекты прошли]')

async def chain_on(apscheduler, name, trigger, text, id_tg, row):
    try:
        int(trigger['row'])
        shed = apscheduler
    except:
        print('заглушка')

async def del_mar(id_m):
    await Config.db.del_elem(id_m)