from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import random
import re
from aiogram import Router
from aiogram.filters import Text, Command
from aiogram.filters.callback_data import CallbackData

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from typing import Optional

from src.bot import bot
from keyboards.inline_keyboards import unyversal_uny, verstka_uny, verstka_uny1, yes_no_dec, get_yes_no_dec
from keyboards.users_menu import usersMenu
from states.user import regist
from config import Config



router = Router()

'''@router.message(Command(commands=['start']))
async def send_main(message: Message, state: FSMContext):
	await state.clear()
	try:
		await Config.db.get_user_tg(message.from_user.id)
		await message.answer('Основное меню', reply_markup = usersMenu.menu0)
	except Exception:
		print('Кто-то пытается зарегистрироваться')'''


@router.message(Command(commands=['add_mag']))
async def send_main(message: Message, state: FSMContext):
	await state.clear()
	try:
		await Config.db.get_name(message.from_user.id)
		await message.answer('Ваш персонаж уже создан', reply_markup=usersMenu.menu0)
	except Exception:
		await state.set_state(regist.playerFullName)
		await message.answer(
			'Приветсвую Вас в мире городской ролевой игры Городские легенды! Сейчас мы пройдем короткую регистрацию. Пожалуйста, введите имя и фамилию игрока или прозвище '
			'по которому МГ может вас опознать. Пожалуйста, используйте только кириллицу')


@router.message(regist.playerFullName)
async def req0(message: Message, state: FSMContext):
	await state.update_data(user = message.text)
	await state.set_state(regist.character)
	await message.answer('Отлично! А теперь общеизвестное имя вашего персонажа')


@router.message(regist.character)
async def req1(message: Message, state: FSMContext):
	await state.update_data(character = message.text)
	await state.set_state(regist.tradition)
	col = ['Исторический факультет', 'Философский факультет', 'Искусствоведение']
	await message.answer('Выбери магическую традицию, к которой принадлежит твой персонаж', reply_markup=verstka_uny(col, 'req'))

@router.callback_query(unyversal_uny.filter(F.v=='req'))
async def req2(query: CallbackQuery, callback_data: unyversal_uny, state: FSMContext):
	await state.update_data(tradition=callback_data.a)
	data = await state.get_data()
	await query.message.edit_text('Итого:\n'
						 f'Игрок {str(data["user"])}\nПерсонаж {str(data["character"])}\n{data["tradition"]}\nВсе верно?'
						 , reply_markup = get_yes_no_dec('req1'))

@router.callback_query(yes_no_dec.filter(F.v=='req1'))
async def req3(query: CallbackQuery, state: FSMContext, callback_data: yes_no_dec):
	await query.message.edit_text(text=f'{query.message.text}')
	if callback_data.a == 'Yes':
		data = await state.get_data()
		await bot.send_message(Config.chatMG_id, f"Игрок {str(data['user'])} пробует зарегестрироваться как "
												 f"{str(data['character'])} на {data['tradition']}.\nПотвердить регистрацию?"
							   , reply_markup=get_yes_no_dec('req2', query.from_user.id))
		await query.message.answer('Отлично! Ожидайте потверждения')
	else:

		await query.message.answer('Тогда попробуйте заново.', reply_markup=usersMenu.startButton)
	await state.clear()


@router.callback_query(yes_no_dec.filter(F.v=='req2'))
async def callback_YES_func(query: CallbackQuery, callback_data: yes_no_dec):
	idTG = callback_data.i
	if callback_data.a == 'Yes':
		user = str(re.findall(r'Игрок (.{1,}) пробует', query.message.text)[0])
		character = str(re.findall(r'как (.{1,}) на', query.message.text)[0])
		tradition = str(re.findall(r'на (.{1,}).', query.message.text)[0])
		await Config.db.add_users(user, character, tradition, idTG)
		await bot.send_message(idTG, 'Заявка подтверждена', reply_markup=usersMenu.menu0)
		await query.message.answer("Игрок зарегистрирован")
	else:
		await bot.send_message(idTG, 'Ваша заявка не удовлетворена, скорей всего с ней что-то не так. '
									 'Можете попробовать подумать и заново отправить заявку',
							   reply_markup=usersMenu.startButton)
		await query.message.answer("Заявка отклонена")
	await query.message.edit_text(text=f"{query.message.text}\n<b>Заявку обработал {query.from_user.full_name}</b>")
