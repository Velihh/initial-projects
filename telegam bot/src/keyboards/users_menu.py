from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# from aiogram.utils.callback_data import CallbackData
def get_keyboard_us():
	builder = ReplyKeyboardBuilder()
	builder.button(text="Мое состояние", callback_data='Мое состояние')
	builder.button(text="Карта", callback_data='Карта')
	builder.button(text="Запросить геолокацию", callback_data="Запросить геолокацию")

	builder.button(
		text="Активности", request_location=True
	)
	# Выравнивание
	builder.adjust(3,2)
	return builder.as_markup()

class usersMenu:
	startButton = ReplyKeyboardMarkup(
		keyboard=[
			[
				KeyboardButton(text='/add_mag'),
			]
		],
		resize_keyboard=True
	)

	menu0 = ReplyKeyboardMarkup(
		keyboard=[
			[
				KeyboardButton(text='Мое состояние'),
				KeyboardButton(text='Карта'),
				KeyboardButton(text='Списать заряды'),
			],
			[
				KeyboardButton(text='Активности'),
				KeyboardButton(text='Вопрос мастерам')
			]
		],
		resize_keyboard=True)

	menu1 = ReplyKeyboardMarkup(
		keyboard=[
			[
				KeyboardButton(text='Сбор зарядов'),
				KeyboardButton(text='Ритуал'),
				KeyboardButton(text='Зачарование'),
			],
			[
				KeyboardButton(text='Передача зарядов'),
				#KeyboardButton(text='Обновить геолокацию', request_location=True),
				KeyboardButton(text='Назад')
			]
		],
		resize_keyboard=True)

	switch_keyboard_users = InlineKeyboardMarkup(
		inline_keyboard=[[
			InlineKeyboardButton(
				text="Ближайшие персонажи", switch_inline_query_current_chat="transfer_of_charges")
		]]
	)
