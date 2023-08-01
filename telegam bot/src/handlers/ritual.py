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
from states.user import UserStates

router = Router()

async def ritual1(msg,id_us, dis):
	charge_geo, power = await Config.db.up_charge_rit(id_us, dis)
	if charge_geo == -1:
		await bot.send_message(chat_id=Config.chatMG_id,
							   text=f'В {dis} исчерпали заряды до минусового значения')
	if charge_geo == -10:
		await bot.send_message(chat_id=Config.chatMG_id,
							   text=f'В {dis} исчерпали заряды до минус 10')
		await msg.answer(
			f'Магическая энергия в районе истощена, ритуал перестал собирать магическую энергию')
	'''try:
		
	except:
		await msg.answer(
			f'Магическая энергия в районе полностью истощена. Пора заканчивать ритуал')
		return'''
	try:
		await msg.edit_text(f'Творение обретает силу! Текущая сила ритуала: {power}', reply_markup=verstka_uny(col=['Закончить'], v='ritual'))
	except:
		await msg.answer('Магическая энергия в районе истощена, ритуал перестал собирать магическую энергию')



@router.message(Text(text=['Ритуал']))
async def ritual0(message: Message, state: FSMContext):
	await state.set_state(UserStates.purpose)
	m = await message.answer('Введи цель ритуала', reply_markup=verstka_uny(col=['Отменить']))
	await state.update_data(m0=m.message_id)

@router.message(UserStates.purpose)
async def ritual3(message: Message, state: FSMContext):
	await state.update_data(pur=message.text)
	await state.set_state(UserStates.resources)
	m = await message.answer('Какие ингредиенты и прочие дополнительные особенности используешь в ритуале? '
						 'Также укажи дополнительных участников ритуала, если вы проводите групповой ритуал.\n'
						 'Перед тем как отправить сообщение, проверь, что у тебя включена трансляция геопозиции.', reply_markup = verstka_uny(['Отменить']))

	await state.update_data(m1=m.message_id)

@router.message(UserStates.resources)
async def ritual4(message: Message, state: FSMContext, apscheduler: AsyncIOScheduler):
	res = message.text
	if res:
		if await live_priverka(message.from_user.id):
			dis = await dis_priverka(message.from_user.id)
			if dis:
				await state.update_data(res=res, dis=dis)
				await state.set_state(UserStates.zag)
				id_j = str(message.from_user.id) + 'coll'
				msg = await message.answer(f'Начинай творить! Текущая сила ритуала:0', reply_markup=verstka_uny(col=['Закончить'], v='ritual'))
				name = await Config.db.get_name(message.from_user.id)
				df = await state.get_data()
				await bot.delete_message(chat_id=message.from_user.id, message_id=df['m0'])
				await bot.delete_message(chat_id=message.from_user.id, message_id=df['m1'])
				await bot.send_message(chat_id=Config.chatMG_id ,text=f"Персонаж {name} начал ритуал\n"
																	  f"Место ритуала: {dis}.\n"
									   f"Цель ритуала: {df['pur']}\n"
									   f"Используемые ресурсы и прочие особенности: {res}")
				try:
					apscheduler.add_job(ritual1, id=id_j, trigger='interval', minutes=1, replace_existing=True,
										coalesce=True, misfire_grace_time=10801,
										kwargs={'msg': msg, "id_us": message.from_user.id, "dis": dis})
				except:
					apscheduler.remove_job(id_j)
					apscheduler.add_job(ritual1, id=id_j, trigger='interval', minutes=1, replace_existing=True,
										coalesce=True, misfire_grace_time=10801,
										kwargs={'msg': msg, "id_us": message.from_user.id, "dis": dis})


# noinspection PyUnresolvedReferences
@router.callback_query(unyversal_uny.filter(F.v=='ritual'))
async def ritual2(query: CallbackQuery, apscheduler: AsyncIOScheduler, state: FSMContext):
	id_j = str(query.from_user.id) + 'coll'
	apscheduler.remove_job(id_j)
	tgid = query.from_user.id
	power = await Config.db.get_one(tgid, 'power')
	name = await Config.db.get_name(tgid)
	msg0 = await query.message.edit_text(f'Ритуал завершен, ожидается ответ мироздания')
	df = await state.get_data()
	msg = await bot.send_message(chat_id= Config.chatMG_id, text=f"Персонаж {name} закончил ритуал\n"
																 f"Место ритуала: {df['dis']}\n"
											 f"Цель ритуала: {df['pur']}\n"
											 f"Особенности ритуала: {df['res']}\n"
											 f"Итоговая сила ритуала: {power}\n🔴"
                                             f"<b>НЕЗАКРЫТАЯ ЗАЯВКА</b>\n"
                                             f"Для отправки результатов ритуала ответьте на это сообщение")
	await Config.db.save_msg(msg.message_id, tgid, msg.text, msg0.message_id)
	await Config.db.null_power(tgid)
	await state.clear()


