from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, chat
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
import asyncio
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
from keyboards.admin_menu import adminMenu
from keyboards.inline_keyboards import unyversal_uny, verstka_uny, verstka_uny1, yes_no_dec, get_yes_no_dec, zna_uny
from states.admin_stats import AdminStates
from utils.filters import IsTrueContact, ChatTypeFilter
from utils.commands import set_commands
from utils.out_fin import Send_msg

router = Router()
router.message.filter(
	IsTrueContact()
)



@router.message(Command(commands=['Назад']))
async def test(message: Message, state: FSMContext):
	await state.clear()
	await message.answer('Основное меню', reply_markup=adminMenu.admin_panel)

@router.callback_query(unyversal_uny.filter(F.a == 'Отмена'))
async def deduction0(query: CallbackQuery, state=FSMContext):
	await state.set_state(AdminStates.zag)
	await query.message.edit_text('Операция отменена')

@router.message(F.reply_to_message)
async def link_to_mg(message: Message):
	msq = await Config.db.get_msq(message.reply_to_message.message_id)
	try:
		await bot.send_message(chat_id=msq[1], text=message.text, reply_to_message_id=msq[3])
		await bot.edit_message_text(chat_id=Config.chatMG_id, message_id=msq[0],
									text=f'{msq[2].split("🔴")[0]}\nЗаявку обработал: {message.from_user.full_name}')
	except(TypeError):
		await message.answer('Cообщение не отправлено')

@router.message(Command(commands=['update_admin']))
async def update_admin(message: Message, state: FSMContext):
	t = await bot.get_chat_administrators(Config.chatMG_id)
	admins = []
	for i in t:
		if i.user.id != 6043223939:
			admins.append(i.user.id)
	Config.chatMG_id = admins
	await set_commands(bot)
	await message.answer('Список администраторов обновлен')


@router.message(Command(commands=['admin_panel']))
async def admin_panel(message: Message, state: FSMContext):
	await message.answer('С кем будешь работать?', reply_markup=adminMenu.admin_panel)

@router.message(Text(text=['Персонажи']))
async def admin_panel1(message: Message, state: FSMContext):
	await message.answer(
		'Выберите игрока в поиске, тыкнув на кнопку ниже',
		reply_markup=adminMenu.switch_keyboard_users)
	await state.set_state(AdminStates.find_user)

@router.message(AdminStates.find_user)
async def my_callback_foo(message: Message,  state: FSMContext):
	try:
		id = re.findall(r'id (\d{1,})', message.text)[0]
	except:
		await state.clear()
		await message.answer('Что-то пошло не так, вас вернуло в Админ панель и все сбросило', reply_markup=adminMenu.admin_panel)
		return
	data = await Config.db.print_spesh_geo(id)
	try:
		longitude = re.findall(r'\[(\d+\.\d+)', data)[0]
		latitude = re.findall(r',(\d+\.\d+)', data)[0]
		await message.answer_location(latitude=latitude, longitude=longitude)
	except(TypeError):
		await message.answer('Данный игрок сейчас не транслирует свою геолокацию')

	await message.answer('Какой параметр игрока хочешь изменить?',
						 reply_markup=adminMenu.pers)
	await state.set_state(AdminStates.zag)
	await state.update_data(user_id=id)

@router.message(Text(text=['Заряды']))
async def charge0(message: Message, state: FSMContext):
	df = await state.get_data()
	data = await Config.db.get_name_max_on_id(df['user_id'])
	col = []
	for i in range(data[1]+1):
		col.append(i)
	col.append('Отмена')
	await message.answer(f'Какое новое количество зарядов установим для {data[0]}?', reply_markup=zna_uny(col, v='char_up'))

@router.callback_query(unyversal_uny.filter(F.v == 'char_up'))
async def charge1(query: CallbackQuery, callback_data=unyversal_uny, state=FSMContext):
	df = await state.get_data()
	await Config.db.up_us_charge(callback_data.a, df['user_id'])
	name = await Config.db.get_name_on_id(df['user_id'])
	await query.message.edit_text(f'Текущее количество зарядов у {name}: {callback_data.a}')

@router.message(Text(text=['Max зарядов']))
async def maxcharge0(message: Message, state: FSMContext):
	df = await state.get_data()
	name = await Config.db.get_name_on_id(df['user_id'])
	col = []
	for i in range(51):
		col.append(i)
	col.append('Отмена')
	await message.answer(f'Какое максимальное количество зарядов установим для {name}?', reply_markup=zna_uny(col, v='mchar_up'))

@router.callback_query(unyversal_uny.filter(F.v == 'mchar_up'))
async def maxcharge1(query: CallbackQuery, callback_data=unyversal_uny, state=FSMContext):
	df = await state.get_data()
	await Config.db.up_us_maxcharge(callback_data.a, df['user_id'])
	name = await Config.db.get_name_on_id(df['user_id'])
	await query.message.edit_text(f'Максимальное количество зарядов у {name}: {callback_data.a}')

@router.message(Text(text=['Традиция']))
async def tradition(message: Message, state: FSMContext):
	df = await state.get_data()
	name = await Config.db.get_name_on_id(df['user_id'])
	col = ['Исторический факультет', 'Философский факультет', 'Искусствоведение','Отмена']
	await message.answer(f'Какую традицию установим для {name}?', reply_markup=verstka_uny(col, v='tradish'))

@router.callback_query(unyversal_uny.filter(F.v == 'tradish'))
async def tradition1(query: CallbackQuery, callback_data=unyversal_uny, state=FSMContext):
	df = await state.get_data()
	await Config.db.up_one_on_id('tradition', callback_data.a, df['user_id'])
	name = await Config.db.get_name_on_id(df['user_id'])
	await query.message.edit_text(f'Традиция у {name} изменена на {callback_data.a}')
	
@router.message(Text(text=['Имя']))
async def tradition(message: Message, state: FSMContext):
	df = await state.get_data()
	name = await Config.db.get_name_on_id(df['user_id'])
	col = ['Отмена']
	await state.set_state(AdminStates.new_name)
	msg = await message.answer(f'Вы хотите сменить имя персонажу {name}? Тогда введите новое имя', reply_markup=verstka_uny(col))
	await state.update_data(msg=msg.message_id)

@router.message(AdminStates.new_name)
async def tradition1(message: Message, state=FSMContext):
	df = await state.get_data()
	await Config.db.up_one_on_id('hero', message.text, df['user_id'])
	await bot.delete_message(chat_id=message.from_user.id, message_id=df['msg'])
	await state.set_state(AdminStates.zag)
	await message.answer(f'Имя персонажа изменено на {message.text}')


@router.message(Text(text=['Районы']))
async def district(message: Message, state: FSMContext):
	await message.answer('Меню управления районами', reply_markup=adminMenu.district)

@router.message(Text(text=['Общая сводка']))
async def district(message: Message, state: FSMContext):
	df = await Config.db.admin_get_map()
	text = 'Районы:\n'
	flag = False
	for i in df:
		text = text + f'\n{i[0]}\nЗарядов: {i[1]}\nМаксимальное количество зарядов: {i[3]}\n' \
					  f'Цикл района равен: {i[4]} минутам\n'
		if i[2] != 'miss':
			flag = True
	if flag:
		text += '\nАномалии есть в районах:\n'
		for i in df:
			if i[2] != 'miss':
				text = text + f'{i[0]} - {i[2]}\n'
	else:
		text += 'Аномалий в районах нет'
	await Send_msg(message.from_user.id,text + '\nhttps://www.google.ru/maps/d/u/0/edit?mid=1ExV_WWScfvLDxj27PyiU5FKnX4H3RK0&usp=sharing')

@router.message(Text(text=['Изменить район']))
async def district(message: Message, state: FSMContext):
	await message.answer(
		'Выберите район в поиске, тыкнув на кнопку ниже',
		reply_markup=adminMenu.switch_keyboard_dis)
	await state.set_state(AdminStates.find_dis)

@router.message(AdminStates.find_dis)
async def my_callback_foo(message: Message, state: FSMContext):
	try:
		id = re.findall(r'id (\d{1,})', message.text)[0]
	except:
		await state.clear()
		await message.answer('Что-то пошло не так, вас вернуло в Админ панель и все сбросило',
							 reply_markup=adminMenu.admin_panel)
		return
	await message.answer('Какой параметр района хочешь изменить?',
						 reply_markup=adminMenu.district1)
	await state.set_state(AdminStates.zag)
	await state.update_data(dis_id=id)

@router.message(Text(text=['Название']))
async def district(message: Message, state: FSMContext):
	col = ['Отмена']
	await state.set_state(AdminStates.new_name1)
	msg = await message.answer(f'Вы хотите сменить название района? Тогда введите новое название',
							   reply_markup=verstka_uny(col))
	await state.update_data(msg=msg.message_id)

@router.message(AdminStates.new_name1)
async def tradition1(message: Message, state=FSMContext):
	df = await state.get_data()
	await Config.db.up_dis_on_id('dis', message.text, df['dis_id'])
	await bot.delete_message(chat_id=message.from_user.id, message_id=df['msg'])
	await message.answer(f'Название района изменено на {message.text}')
	await state.set_state(AdminStates.zag)

@router.message(Text(text=['Цикл']))
async def district(message: Message, state: FSMContext):
	col = ['Отмена']
	await state.set_state(AdminStates.timer)
	msg = await message.answer(f'Введите число, раз в сколько минут будет востанавливаться район?',
							   reply_markup=verstka_uny(col))
	await state.update_data(msg=msg.message_id)

@router.message(AdminStates.timer)
async def tradition1(message: Message, apscheduler: AsyncIOScheduler, state=FSMContext):
	try:
		timer = int(message.text)
		if timer > 0:
			df = await state.get_data()
			await Config.db.up_dis_on_id('timer', timer, df['dis_id'])
			await bot.delete_message(chat_id=message.from_user.id, message_id=df['msg'])
			await state.set_state(AdminStates.zag)
			id_ = df['dis_id'] + 'dis'
			apscheduler.reschedule_job(job_id=id_, trigger="interval", minutes=timer)
			await message.answer(f'Цикл востановления района изменен на {timer}')
		else:
			await message.answer(f'Число должно быть положительным')
	except:
		await message.answer(f'Отправте число цифрами без пробелов и букв или нажмите кнопку "Отмена"')

@router.message(Text(text=['Аномалии']))
async def district(message: Message, state: FSMContext):
	col = ['Удалить все аномалии','Отмена']
	await state.set_state(AdminStates.anomaly)
	msg = await message.answer(f'Введите текст описывающий аномалии в данном районе',
							   reply_markup=verstka_uny(col))
	await state.update_data(msg=msg.message_id)

@router.callback_query(unyversal_uny.filter(F.a == 'Удалить все аномалии'))
async def tradition1(query: CallbackQuery, callback_data=unyversal_uny, state=FSMContext):
	df = await state.get_data()
	await Config.db.up_dis_on_id('notes', 'miss', df['dis_id'])
	await query.message.edit_text(f'Аномалии в районе удалены')
	await state.set_state(AdminStates.zag)

@router.message(AdminStates.anomaly)
async def tradition1(message: Message, state=FSMContext):
	df = await state.get_data()
	await Config.db.up_dis_on_id('notes', message.text, df['dis_id'])
	await bot.delete_message(chat_id=message.from_user.id, message_id=df['msg'])
	await message.answer(f'Текущие аномалии в районе: {message.text}')
	await state.set_state(AdminStates.zag)

@router.message(Text(text=['Заряд']))
async def charge0(message: Message, state: FSMContext):
	await message.answer('Установить новое значение или прибавить/убавить к старому?',
						 reply_markup=verstka_uny(['Установить', 'Изменить']))

@router.callback_query(unyversal_uny.filter(F.a == 'Установить'))
async def charge0(query: CallbackQuery, state: FSMContext):
	df = await state.get_data()
	data = await Config.db.get_dis_max(df['dis_id'])
	col = []
	for i in range(-50, data[1]+1, 2):
		col.append(i)
	col.append('Отмена')
	await query.message.answer(f'Какое новое количество зарядов установим для {data[0]}?', reply_markup=zna_uny(col, v='charDIS_up'))


@router.callback_query(unyversal_uny.filter(F.a == 'Изменить'))
async def haos(query: CallbackQuery, state: FSMContext):
	await state.set_state(AdminStates.charge_dis)
	await query.message.edit_text('Введи число на которое именяется значение зарядов района(это число прибавится к текущему значению. '
								  'Можно использовать отрицательные значениея, но в сумме итоговое число не должно уходить меньше чем в -50')

@router.message(AdminStates.charge_dis)
async def shaman0_yes_no(message: Message, state: FSMContext):
	df = await state.get_data()
	try:
		count = await Config.db.up_disChar_on_id(message.text, df['dis_id'])
	except:
		await message.answer(f'Введи такое число, что итоговая сумма была не меньше -50')
		return
	await message.answer(f'Ты успешно изменил значение зарядов района. Текущее значение: {count}')

@router.callback_query(unyversal_uny.filter(F.v == 'charDIS_up'))
async def charge1(query: CallbackQuery, callback_data=unyversal_uny, state=FSMContext):
	df = await state.get_data()
	await Config.db.up_dis_on_id("charge", callback_data.a, df['dis_id'])
	await query.message.edit_text(f'Текущее количество зарядов: {callback_data.a}')

@router.message(Text(text=['Max_зарядов']))
async def charge0(message: Message, state: FSMContext):
	col = []
	for i in range(-5, 51):
		col.append(i)
	col.append('Отмена')
	await message.answer(f'Какое максимальное количество зарядов установим?', reply_markup=zna_uny(col, v='charDISmax'))

@router.callback_query(unyversal_uny.filter(F.v == 'charDISmax'))
async def charge1(query: CallbackQuery, callback_data=unyversal_uny, state=FSMContext):
	df = await state.get_data()
	await Config.db.up_dis_on_id('max_charge', callback_data.a, df['dis_id'])
	await query.message.edit_text(f'Текущее количество зарядов: {callback_data.a}')

@router.message(Text(text=['Игроки на карте']))
async def showMenu(message: Message):
	data = Config.db.print_geo()
	if data:
		id_users = [f'1 - {data[0][0]}']
		geo = re.findall(r'(\d+\.\d+)', data[0][1])
		print(geo)
		map_request = f"[Карта](https://static-maps.yandex.ru/1.x/?lang=ru_RU&size=650,450&ll=60.61394971000122,56.835897300286256&l=map&pt={geo[0]},{geo[1]},pm2wtm1"
		for i in range(1, len(data)):
			print(data[i])
			id_users.append(f'{i+1} - {data[i][0]}')
			latitude = re.findall(r'\[(\d+\.\d+)', data[i][1])[0]
			longitude = re.findall(r',(\d+\.\d+)', data[i][1])[0]
			map_request += f"~{latitude},{longitude},pm2wtm{i+1}"
		map_request += ")"
		await message.answer(
			map_request,
			parse_mode='Markdown'
		)
		await message.answer(
			text="\n".join(id_users),
			# text="\n".join(map(str, id_users)),
			parse_mode='Markdown'
		)
	else:
		await message.answer('Никто из игроков не транслирует геопозицию')

@router.message(Command(commands=['gps']))
async def callback_reg(message: Message):
	# lat = re.findall(r'(\d+\.\d+),', message.text)[0]
	# lon = re.findall(r', (\d+\.\d+)', message.text)[0]
	await Config.db.add_geo(5696241401, 56.835146049210756, 60.59017460970266, 490877282, 56.84061731949926, 60.635415530295276)
	await message.answer('гео')

@router.message(Command(commands=['otladka_chat']))
async def get_chooseUser_func(message: Message, apscheduler: AsyncIOScheduler, state: FSMContext):
	apscheduler.remove_all_jobs()
	await message.answer('Все задачи удалены')

@router.message(Command(commands=['jobs']))
async def jobs(message: Message, apscheduler: AsyncIOScheduler):
	job = apscheduler.get_jobs()
	print(job)