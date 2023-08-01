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

async def enchant1(msg,id_us, dis):
    charge_geo, power = await Config.db.up_charge_rit(id_us, dis)
    try:
        if charge_geo == -1:
            await bot.send_message(chat_id=Config.chatMG_id,
                                   text=f'В {dis} исчерпали заряды до минусового значения')
        if charge_geo == -10:
            await bot.send_message(chat_id=Config.chatMG_id,
                                   text=f'В {dis} исчерпали заряды до минус 10')
            await msg.answer(
                f'Магическая энергия в районе истощена, ритуал перестал собирать магическую энергию')
    except:
        await msg.answer(
            f'Магическая энергия в районе истощена. Пора заканчивать ритуал зачарования')
        return
    try:
        await msg.edit_text(f'Творение обретает силу! Текущая сила ритуала зачарования: {power}', reply_markup=verstka_uny(col=['Закончить'], v='enchant'))
    except:
        await msg.answer('Магическая энергия в районе истощена, ритуал перестал собирать магическую энергию')



@router.message(Text(text=['Зачарование']))
async def enchant0(message: Message, state: FSMContext):
    await state.set_state(UserStates.item)
    m = await message.answer('Какой предмет зачаровываешь?', reply_markup=verstka_uny(col=['Отменить']))
    await state.update_data(m0=m.message_id)

@router.message(UserStates.item)
async def enchant0_0(message: Message, state: FSMContext):
    await state.set_state(UserStates.purpose1)
    await state.update_data(item=message.text)
    m = await message.answer('Какой эффект хочешь получить на предмете?', reply_markup=verstka_uny(col=['Отменить']))
    await state.update_data(m3=m.message_id)

@router.message(UserStates.purpose1)
async def enchant3(message: Message, state: FSMContext):
    await state.update_data(pur=message.text)
    await state.set_state(UserStates.resources1)
    m = await message.answer('Какие ингредиенты и прочие дополнительные особенности используешь в ритуале? '
                         'Также укажи дополнительных участников ритуала, если вы проводите групповой ритуал.\n'
                         'Перед тем как отправить сообщение, проверь, что у тебя включена трансляция геопозиции.', reply_markup = verstka_uny(['Отменить']))

    await state.update_data(m1=m.message_id)

@router.message(UserStates.resources1)
async def enchant4(message: Message, state: FSMContext, apscheduler: AsyncIOScheduler):
    res = message.text
    if res:
        if await live_priverka(message.from_user.id):
            dis = await dis_priverka(message.from_user.id)
            if dis:
                await state.update_data(res=res, dis=dis)
                await state.set_state(UserStates.zag)
                id_j = str(message.from_user.id) + 'coll'
                msg = await message.answer(f'Начинай творить! Текущая сила ритуала зачарования:0', reply_markup=verstka_uny(col=['Закончить'], v='enchant'))
                name = await Config.db.get_name(message.from_user.id)
                df = await state.get_data()
                await bot.delete_message(chat_id=message.from_user.id, message_id=df['m0'])
                await bot.delete_message(chat_id=message.from_user.id, message_id=df['m1'])
                await bot.delete_message(chat_id=message.from_user.id, message_id=df['m3'])
                await bot.send_message(chat_id=Config.chatMG_id ,text=f"Персонаж {name} начал ритуал зачарования предмета: {df['item']}\n"
                                                                      f"Место ритуала: {dis}.\n"
                                                                      f"Эффект зачарования: {df['pur']}\n"
                                       f"Используемые ресурсы и прочие особенности: {res}")
                try:
                    apscheduler.add_job(enchant1, id=id_j, trigger='interval', minutes=1, replace_existing=True,
                                        coalesce=True, misfire_grace_time=10801,
                                        kwargs={'msg': msg, "id_us": message.from_user.id, "dis": dis})
                except:
                    apscheduler.remove_job(id_j)
                    apscheduler.add_job(enchant1, id=id_j, trigger='interval', minutes=1, replace_existing=True,
                                        coalesce=True, misfire_grace_time=10801,
                                        kwargs={'msg': msg, "id_us": message.from_user.id, "dis": dis})
    else:
        await message.answer(
            'Включите трансляцию геопозиции или, если она уже включена потрясите телефон, и попробуйте еще раз')


# noinspection PyUnresolvedReferences
@router.callback_query(unyversal_uny.filter(F.v=='enchant'))
async def enchant2(query: CallbackQuery, apscheduler: AsyncIOScheduler, state: FSMContext):
    id_j = str(query.from_user.id) + 'coll'
    apscheduler.remove_job(id_j)
    tgid = query.from_user.id
    power = await Config.db.get_one(tgid, 'power')
    name = await Config.db.get_name(tgid)
    df = await state.get_data()
    msg0 = await query.message.edit_text(f'Ритуал зачарования завершен\n'
                                         f'Предмет: {df["item"]}\n'
                                         f'Желаемый эффект: {df["pur"]}\n'
                                         f'Место ритуала: {df["dis"]}\n'
                                         f'Используемые ресурсы и прочие особенности: {df["res"]}\nОжидается ответ мироздания')
    msg = await bot.send_message(chat_id= Config.chatMG_id, text=f"Персонаж {name} закончил ритуал\n"
                                                                 f"Место ритуала: {df['dis']}\n"
                                                                 f"Предмет: {df['item']}"
                                             f"Эффект: {df['pur']}\n"
                                             f"Используемые ресурсы и прочие особенности: {df['res']}\n"
                                             f"Итоговая сила ритуала: {power}\n🔴"
                                             f"<b>НЕЗАКРЫТАЯ ЗАЯВКА</b>\n"
                                             f"Для отправки результатов ритуала ответьте на это сообщение")
    await Config.db.save_msg(msg.message_id, tgid, msg.text, msg0.message_id)
    await state.clear()
    await Config.db.null_power(tgid)
