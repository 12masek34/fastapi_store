from pyrogram.types import InlineKeyboardButton

from pyrogram.types import InlineKeyboardMarkup


class Keyboard:
    START = InlineKeyboardMarkup([
        [InlineKeyboardButton('Объявления', callback_data='post')],
        [InlineKeyboardButton('Категории', callback_data='category')]
    ])

    CRUD = InlineKeyboardMarkup([
        [InlineKeyboardButton('создать', callback_data='create')],
        [InlineKeyboardButton('изменить', callback_data='update')],
        [InlineKeyboardButton('удалить', callback_data='delete')]
    ])

    SAVE_CANCEL = InlineKeyboardMarkup([
        [InlineKeyboardButton('Сохранить', callback_data='save')],
        [InlineKeyboardButton('Отмена', callback_data='cancel')]
    ])

    DELETE_CANCEL = InlineKeyboardMarkup([
        [InlineKeyboardButton('Удалить', callback_data='delete')],
        [InlineKeyboardButton('Отмена', callback_data='cancel')]
    ])

    @staticmethod
    def create_keyboard_add_category(categories: dict):

        res = []
        for category in categories:
            res.append([InlineKeyboardButton(category['title'], callback_data=f'add_category_to_post{category["id"]}')])
        return InlineKeyboardMarkup(res)

    @staticmethod
    def create_keyboard_count_category(categories: list, count: dict):

        gather_list = categories.copy()
        index = 0
        for cat in categories:
            for c in count:
                if cat['title'] == c['title']:
                    gather_list.pop(index)
                    index -= 1
            index += 1

        for c in count:
            gather_list.append(c)

        gather_list.reverse()
        res = []

        for i in gather_list:
            if i['count'] is None:
                res.append([InlineKeyboardButton(i['title'] + f'(0)',
                                                 callback_data=f'add_category_to_post{i["id"]}')])
            else:
                res.append([InlineKeyboardButton(i['title'] + f'({i["count"]})',
                                                 callback_data=f'add_category_to_post{i["id"]}')])

        return InlineKeyboardMarkup(res)

    @staticmethod
    def delete_keyboard_category(categories: dict):
        res = []
        for category in categories:
            res.append([InlineKeyboardButton(category['title'], callback_data=f'delete_category{category["id"]}')])
        return InlineKeyboardMarkup(res)
