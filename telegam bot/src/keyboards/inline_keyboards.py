from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional
import random
import string

class unyversal_uny(CallbackData, prefix ="uny"):
	a: str
	v: Optional[str]
	b: Optional[str]
	t: Optional[int]

def verstka_uny(col, v: str = None, b: str = None, t: int = 0):
	builder = InlineKeyboardBuilder()
	for i in col:
		builder.button(
			text=i, callback_data=unyversal_uny(a=i, v=v, b=b, t=t))
	builder.adjust(1)
	return builder.as_markup()

def zna_uny(col, v: str = None, b: str = None, t: int = 0):
	builder = InlineKeyboardBuilder()
	for i in col:
		builder.button(
			text=i, callback_data=unyversal_uny(a=i, v=v, b=b, t=t))
	builder.adjust(6)
	return builder.as_markup()

def verstka_uny1(col, t, v: str = None, b: str = None):
	builder = InlineKeyboardBuilder()
	for i, row in zip(col,t):
		builder.button(
			text=i, callback_data=unyversal_uny(a=i, t=row, b=b, v=v))
	builder.adjust(1)
	return builder.as_markup()

class yes_no_dec(CallbackData, prefix="dec"):
	a: str
	v: Optional[str]
	i: Optional[int]

def get_yes_no_dec(val: str = None, ids: int = 0):
	builder = InlineKeyboardBuilder()
	builder.button(
		text="Да", callback_data=yes_no_dec(a="Yes", v=val, i=ids)
	)
	builder.button(
		text="Нет", callback_data=yes_no_dec(a="No", v=val, i=ids)
	)
	# Выравнивание по 2 в ряд
	builder.adjust(2)
	return builder.as_markup()

class UsCallback(CallbackData, prefix="us"):
	action: str
	value: Optional[str]

