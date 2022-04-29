from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Keyboard:
    def __init__(self):
        self.category: list | None = None

    START = [
        [InlineKeyboardButton('Объявления', callback_data='post')],
        [InlineKeyboardButton('Категории', callback_data='category')]
    ]

    CRUD = [
        [InlineKeyboardButton('создать', callback_data='create')],
        [InlineKeyboardButton('изменить', callback_data='update')],
        [InlineKeyboardButton('удалить', callback_data='delete')]
    ]

    SAVE_CANCEL = [
        [InlineKeyboardButton('Сохранить', callback_data='save')],
        [InlineKeyboardButton('Отмена', callback_data='cancel')]
    ]

    def create_keyboard_category(self, category):
        res = []
        for i in category:
            res.append([InlineKeyboardButton(i['title'], callback_data=f'add_category_to_post{i["id"]}')])
        self.category = res
