from src.bot import bot
from src.config import Config

async def live_priverka(tgid):
	flag = await Config.db.get_one(tgid, 'live_time')
	if flag == 1:
		return True
	else:
		await bot.send_message(chat_id=tgid, text='Для выполнения данной операции необходима трансляция геопозиции. Отправте трансляцию и попробуйте еще раз')
		return False


async def dis_priverka(tgid):
	flag = await Config.db.get_one(tgid, 'district')
	if flag != 'Неопределен':
		print(flag)
		return flag
	else:
		print('no')
		await bot.send_message(chat_id=tgid, text='Вы не чувствуете подходящей для сбора магической энергии в окружающем вас пространстве. '
												  '[Вы находитесь за пределами районов]')
		return False

async def Send_msg(msq,text):
	MESS_MAX_LENGTH = 4096
	for x in range(0, len(text), MESS_MAX_LENGTH):
		mess = text[x: x + MESS_MAX_LENGTH]
		msg = await bot.send_message(chat_id=msq,text=mess)
	return msg
