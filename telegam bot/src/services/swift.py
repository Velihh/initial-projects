
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle
import hashlib
from config import Config
from aiogram import Router, F
import re
from utils.filters import IsTrueContact


router = Router()
router.inline_query.filter(
	IsTrueContact()
)


@router.inline_query(F.query.startswith('users'))
async def inline_echo(inline_query: InlineQuery):
    try:
        data = await Config.db.get_names(re.findall(r'users (.+)',inline_query.query)[0])
    except:
        data = await Config.db.get_names()
    item = [InlineQueryResultArticle(
        id=str(hashlib.md5(data[i][1].encode()).hexdigest()),
        title=f'Игрок: {data[i][1]}, персонаж: {data[i][2]}',
        input_message_content=InputTextMessageContent(
            message_text=Config.db.get_stateA(data[i][0])),
    ) for i in range(len(data))]
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await inline_query.answer(results=item, cache_time=10)

@router.inline_query(F.query.startswith('dis'))
async def inline_echo(inline_query: InlineQuery):
    data = await Config.db.get_dist()
    item = [InlineQueryResultArticle(
        id=str(hashlib.md5(data[i][1].encode()).hexdigest()),
        title=data[i][1],
        input_message_content=InputTextMessageContent(
            message_text=Config.db.get_statedis(data[i][0])),
    ) for i in range(len(data))]
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await inline_query.answer(results=item, cache_time=10)


