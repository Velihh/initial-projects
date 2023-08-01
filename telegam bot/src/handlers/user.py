from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, chat
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from aiogram.filters.callback_data import CallbackData
from typing import Optional
import re
from random import choice
from aiogram.utils.keyboard import InlineKeyboardBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from aiogram import Router

from src.bot import bot
from src.config import Config
from keyboards import usersMenu,get_keyboard_us
from keyboards.inline_keyboards import unyversal_uny, verstka_uny, verstka_uny1, zna_uny
from states.user import UserStates
from utils.out_fin import live_priverka
from utils.out_fin import Send_msg

router = Router()


@router.message(Text(text='Назад', ignore_case=True))
async def showMenu(message: Message, state: FSMContext):
	await state.clear()
	try:
		await Config.db.get_name(message.from_user.id)
		await message.answer('Основное меню', reply_markup=usersMenu.menu0)
	except Exception as f:
		print(f'{message.from_user.id} пытается зарегистрироваться', f)

@router.callback_query(unyversal_uny.filter(F.a == 'Отменить'))
async def deduction0(query: CallbackQuery, state=FSMContext):
	await state.clear()
	await query.message.edit_text('Операция отменена')

'''@router.message(F.content_type.in_({'location'}))
async def get_clair_us(message: Message):
	lat = message.location.latitude
	lon = message.location.longitude
	try:
		await Config.db.up_geo(message.from_user.id, lat, lon)
	except:
		await message.answer('Вы не прошли регистрацию')
		return'''
	# сюда можно вставить названине района


@router.message(Command(commands=['start']))
async def showMenu(message: Message, state: FSMContext):
	await state.clear()
	try:
		await Config.db.get_name(message.from_user.id)
		await message.answer('Основное меню', reply_markup=usersMenu.menu0)
	except Exception as f:
		print(f'{message.from_user.id} пытается зарегистрироваться', f)

@router.message(Text(text=['активности'], ignore_case=True))  # страновится пофиг на регистр
async def map_menu(message: Message, state: FSMContext):
	await state.clear()
	loc = message.location
	print(loc)
	await message.answer(f"С помощью данного меню можно:\n1) Осуществить сбор зарядов с района, в котором вы сейчас находитесь\n"
						 f"2) Зарегистрировать ритуал\n"
						 f"3) Провести зачарование предмета\n"
						 f"4) Передать свои заряды другому игроку\n"
						 f"Для дальнейшего использования данного меню, необходима трансляция геопозиции",
						 reply_markup=usersMenu.menu1)

@router.message(Text(text=['мое состояние'], ignore_case=True))  # страновится пофиг на регистр
async def my_state(message: Message):
	df = await Config.db.get_state(message.from_user.id)
	await message.answer(f"{df[0]}, {df[1]}\n"
						 f"Зарядов: {df[2]}\n"
						 f"Максимальное количество зарядов: {df[3]}\n"
						 f"Район: {df[4]}")

@router.message(Text(text=['Списать заряды'], ignore_case=True))
async def deduction(message: Message, state: FSMContext):
	await state.set_state(UserStates.charge)
	charge = await Config.db.get_one(message.from_user.id, 'charge')
	id_m = await message.answer(f'Введи число на которое ты списываешь свои заряды.\nТекущее значение: {charge}',
						 reply_markup=verstka_uny(['Отменить']))
	await state.update_data(id_m=id_m.message_id)

@router.message(UserStates.charge)
async def deduction1(message: Message, state: FSMContext):
	df = await state.get_data()
	count = await Config.db.change_charge(message.from_user.id, abs(int(message.text)))
	try:

		await bot.edit_message_text(chat_id=message.from_user.id, message_id=df['id_m'],
									text=f'<b>УСПЕХ.</b> Вы изменили свое значение зарядов.\nТекущее значение: {count}')
		await state.clear()
	except:
		await message.answer(f'Введи такое число, что итоговая сумма была не меньше нуля')
		return

@router.message(Text(text=['Передача зарядов']))
async def transfer0(message: Message, callback_data=unyversal_uny, state=FSMContext):
	if await live_priverka(message.from_user.id):
		df = await Config.db.transfer_of_charges(message.from_user.id)
		val = []
		col = []

		for i in df:
			val.append(int(i[0]))
			col.append(i[1])
		col.append('Отменить')
		val.append(0)
		print(val, df)
		await message.answer('Кому передашь заряды? За передачу зарядов магу своей традиции тратится 1 заряд, '
							 'а за передачу зарядов магу другой традиции тратится 2 заряда.'
							 ' Ниже отображаются все маги рядом с тобой, '
							 'у которых включена трансляция геопозиции.', reply_markup=verstka_uny1(col=col, t=val, b='trans'))

@router.callback_query(unyversal_uny.filter(F.b == 'trans'))
async def transfer1(query: CallbackQuery, callback_data=unyversal_uny, state=FSMContext):
	await state.update_data(id_=callback_data.t)
	t = await Config.db.get_tarif(query.from_user.id, callback_data.t)
	col = []
	if t > 0:
		for i in range(1,t+1):
			col.append(i)
		col.append('Отменить')
		await query.message.edit_text('Сколько зарядов передашь?', reply_markup=zna_uny(col, v='transfer'))
	else:
		await query.message.edit_text('У тебя недостаточно зарядов для передачи')

@router.callback_query(unyversal_uny.filter(F.v == 'transfer'))
async def transfer3(query: CallbackQuery, callback_data=unyversal_uny, state=FSMContext):
	data = await state.get_data()
	charge = await Config.db.transfer_of_charges1(query.from_user.id, data['id_'], callback_data.a)
	await query.message.edit_text(f'Вы успешно передали {callback_data.a} единицы заряда. Остаток зарядов: {charge}')
	tgid = await Config.db.get_tgid(data['id_'])
	await bot.send_message(chat_id=tgid, text=f'Вам передано {callback_data.a} единицы заряда')

@router.message(Text(text=['Карта']))
async def map(message: Message, state: FSMContext):
	df = await Config.db.get_map()
	text = 'Количество зарядов в районах:\n'
	flag = False
	for i in df:
		text = text + f'{i[0]}: {i[1]}\n'
		if i[2] != 'miss':
			flag = True
	if flag:
		text += '\nОбнаружены аномалии:\n'
		for i in df:
			if i[2] != 'miss':
				text = text + f'{i[0]} - {i[2]}\n'
	await Send_msg(message,text + '\nhttps://www.google.ru/maps/d/u/0/edit?mid=1ExV_WWScfvLDxj27PyiU5FKnX4H3RK0&usp=sharing')

### ЗАЯВКИ

@router.message(Text(text=['Вопрос мастерам']))
async def link_to_mg1(message: Message, state=FSMContext):
	await state.clear()
	await state.set_state(UserStates.question)
	await message.answer('Следущим сообщением отправте текстом ваш вопрос')

@router.message(UserStates.question)
async def link_to_mg1(message: Message, state=FSMContext):
	col = ['Да', "Нет"]
	await state.set_state(UserStates.zag)
	await state.update_data(text=message.text)
	await message.answer(f"Вы хотите отправить следующий вопрос мастерам: {message.text}\nВсе верно?",
						 reply_markup=verstka_uny(col=col, v='МГ_заявка'))

@router.callback_query(unyversal_uny.filter(F.v == 'МГ_заявка'))
async def link_to_mg1(query: CallbackQuery, callback_data=unyversal_uny, state=FSMContext):
	if callback_data.a == 'Да':
		tgid = query.from_user.id
		df = await state.get_data()
		name = await Config.db.get_name(tgid)
		await bot.send_message(Config.chatMG_id,
							   f'[{name}](tg://user?id={tgid})',
							   parse_mode='Markdown')
		await query.message.delete()
		msg0 = await query.message.answer(f'Отлично! Ваш вопрос: <i>{df["text"]}</i> - отправлен мастерам, в скором времени вам придет ответ')

		msg = await Send_msg(Config.chatMG_id,
							   f"{name} задал следующий вопрос мастерам:\n"
							   f"<i>{df.get('text')}</i>\n"
							   f"🔴<b>НЕЗАКРЫТАЯ ЗАЯВКА</b>\n"
							   f"Для отправки ответа ответьте на это сообщение")
		await Config.db.save_msg(msg.message_id, tgid, msg.text, msg0.message_id)
	else:
		await query.message.edit_text('Тогда в другой раз')
	await state.clear()