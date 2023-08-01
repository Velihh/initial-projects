from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, chat
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, CallbackGame, chat
from typing import Optional
import re
from random import choice
from aiogram.utils.keyboard import InlineKeyboardBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from aiogram import Router

from src.bot import bot
from src.config import Config
from keyboards import usersMenu
from keyboards.inline_keyboards import unyversal_uny, verstka_uny, verstka_uny1, yes_no_dec, get_yes_no_dec
from utils.out_fin import live_priverka, dis_priverka
from apscheduler.schedulers.asyncio import AsyncIOScheduler

router = Router()

async def collecting1(msg,id_us, dis):
	try:
		charge, charge_geo = await Config.db.up_charge(id_us, dis)
		if charge_geo == -1:
			await msg.answer(
				f'Магическая энергия в районе истощена, ты больше не можешь собирать заряды. Пора заканчивать сбор зарядов')
			await bot.send_message(chat_id=Config.chatMG_id,
								   text=f'В {dis} исчерпали заряды до минусового значения')
	except:
		await msg.answer(
			f'Магическая энергия в районе полностью истощена, ты больше не можешь собирать заряды. Пора заканчивать сбор зарядов')
		#name = await Config.db.get_name(id_us)
		#await bot.send_message(chat_id=Config.chatMG_id, text=f'В районе {dis} полностью закончилась магическая энергия. А персонаж {name} пытается ее там добыть.')
	try:
		await msg.edit_text(f'{msg.text.split(":")[0]}: {charge}', reply_markup=verstka_uny(col=['Закончить'], v='coll'))
	except:
		await msg.answer(f'Ты чувствуешь, что магическая энергия окужающего пространства больше не наполняет тебя')


@router.message(Text(text=['Сбор зарядов']))
async def collecting0(message: Message, apscheduler: AsyncIOScheduler):
	if await live_priverka(message.from_user.id):
		dis = await dis_priverka(message.from_user.id)
		if dis:
			tradition = await Config.db.get_one(message.from_user.id, 'tradition')
			char = await Config.db.get_one(message.from_user.id, 'charge')
			id_j = str(message.from_user.id) + 'coll'

			dict_ = {
				'Искусствоведение': "Таймер запущен. Выполняйте практику своего направления искусства, самовыражайтесь. Твое текущее количество зарядов: ",
				'Философский факультет': 'Таймер запущен. Выполняйте практику в риторике и размышлении. Это может выражаться публичными дискусами, монологими, написанием постов и т.п. Твое текущее количество зарядов: ',
				'Исторический факультет': 'Таймер запущен. Выполняй практику своей традиции, читай заклинания, проводи древние ритуалы. Твое текущее количество зарядов: '}
			msg = await message.answer(f'{dict_[tradition]}{char}', reply_markup=verstka_uny(col=['Закончить'], v='coll'))
			apscheduler.add_job(collecting1, id=id_j, trigger='interval', minutes=1, replace_existing=True,
								coalesce=True, misfire_grace_time=10801,
								kwargs={'msg': msg, "id_us": message.from_user.id, "dis": dis})
		else:
			await message.answer('Ваш район неопределен. Потрясите телефон и попробуйте еще раз')
	else:
		await message.answer('Включите трансляцию геопозиции и попробуйте еще раз')

@router.callback_query(unyversal_uny.filter(F.v=='coll'))
async def collecting2(query: CallbackQuery, apscheduler: AsyncIOScheduler):
	id_j = str(query.from_user.id) + 'coll'
	apscheduler.remove_job(id_j)
	char = await Config.db.get_one(query.from_user.id, 'charge')
	await query.message.edit_text(f'Сбор зарядов завершен, твое текущее количество зарядов: {char}')

