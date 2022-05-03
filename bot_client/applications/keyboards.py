from pyrogram.types import InlineKeyboardButton

from pyrogram.types import InlineKeyboardMarkup


class Keyboard:
    START = InlineKeyboardMarkup([
        [InlineKeyboardButton('Все объявления', callback_data='all_post')],
        [InlineKeyboardButton('Категории', callback_data='category')]
    ])

    @staticmethod
    def create_keyboard_category(categories: dict):
        res = []
        for category in categories:
            res.append([InlineKeyboardButton(category['title'], callback_data=f'category_{category["id"]}')])
        return InlineKeyboardMarkup(res)
