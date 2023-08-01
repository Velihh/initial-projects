from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

class adminMenu:
    admin_panel = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Персонажи'),
                KeyboardButton(text='Районы'),
            ],
            [
                KeyboardButton(text='Игроки на карте'),
            ]
        ],
        resize_keyboard=True
    )
    switch_keyboard_users = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="Найти игрока", switch_inline_query_current_chat="users")
        ]]
    )
    switch_keyboard_dis = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="Найти район", switch_inline_query_current_chat="dis")
        ]]
    )
    pers = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Заряды'),
                KeyboardButton(text='Max зарядов'),
                KeyboardButton(text='Традиция'),
            ],
            [
                KeyboardButton(text='Имя'),
                KeyboardButton(text='/Назад')
            ]

        ],
        resize_keyboard=True)

    district = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Общая сводка'),
                KeyboardButton(text='Изменить район'),
            ],
            [
                KeyboardButton(text='/Назад')
            ]

        ],
        resize_keyboard=True)

    district1 = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Название'),
                KeyboardButton(text='Цикл'),
                KeyboardButton(text='Аномалии'),
            ],
            [
                KeyboardButton(text='Заряд'),
                KeyboardButton(text='Max_зарядов'),
                KeyboardButton(text='/Назад')
            ]

        ],
        resize_keyboard=True)

    pn_size = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='0'),
                KeyboardButton(text='50'),
                KeyboardButton(text='100'),
                KeyboardButton(text='250'),
                KeyboardButton(text='500')
            ],
            [
                KeyboardButton(text='1000'),
                KeyboardButton(text='3000')
            ]
        ], resize_keyboard=True)
