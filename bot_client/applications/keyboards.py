from pyrogram.types import InlineKeyboardButton

from pyrogram.types import InlineKeyboardMarkup


class Keyboard:
    def __init__(self):
        self.category: list | None = None

    START = InlineKeyboardMarkup([
        [InlineKeyboardButton('Все объявления', callback_data='all_post')],
        [InlineKeyboardButton('Категории', callback_data='category')]
    ])
