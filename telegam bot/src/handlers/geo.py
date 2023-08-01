import re
from aiogram import F
from aiogram import Router
from aiogram.types import Message

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

from config import Config

router = Router()

async def stop_live(id_us):
	print(f'stop_live {id_us}')
	await Config.db.stop_live(id_us)

@router.edited_message(F.content_type.in_({'location'}))
async def geo_edit(message: Message, apscheduler: AsyncIOScheduler):
	lat = message.location.latitude
	lon = message.location.longitude
	id_tg = message.from_user.id
	live = message.location.live_period
	print(id_tg)
	try:
		flag = await Config.db.up_geo(id_tg, lat, lon)
	except:
		return
	if flag == 0:
		try:
			date = datetime.now() + timedelta(seconds=live+3)
		except(TypeError):
			await stop_live(id_tg)
			return
		#job_id = 'geo' + str(id_tg)
		apscheduler.add_job(stop_live, trigger="date", run_date=date,
							kwargs={'id_us': id_tg})
	return
