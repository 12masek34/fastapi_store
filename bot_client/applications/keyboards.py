from pyrogram.types import InlineKeyboardButton

from pyrogram.types import InlineKeyboardMarkup


class Keyboard:
    START = InlineKeyboardMarkup([
        [InlineKeyboardButton('Все объявления', callback_data='all_post')],
        [InlineKeyboardButton('Категории', callback_data='category')]
    ])

    BACK_NEXT_MAIN = InlineKeyboardMarkup([[InlineKeyboardButton('<<<<<', callback_data='back'),
                                            InlineKeyboardButton('>>>>>', callback_data='next')],
                                           [InlineKeyboardButton('Главная', callback_data='main')]])

    @staticmethod
    def create_keyboard_category(categories: dict):
        res = []
        for category in categories:
            if category['count'] is None:
                continue
            else:
                res.append([InlineKeyboardButton(category['title'] + f'({category["count"]})',
                                                 callback_data=f'category_{category["id"]}')])
        return InlineKeyboardMarkup(res)
