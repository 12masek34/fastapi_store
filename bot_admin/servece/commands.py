from .my_deque import Deque


class Command:
    def __init__(self):
        self.callback_data: str | None = None
        self.location: str | None = None
        self.new_command: str | None = None

    START = ['/start', 'start']

    START_MESSAGE = 'Приветную господин. Что будем делать?'
    POST_MESSAGE = 'Приветную господин. Что будем делать c постами?'
    CATEGORY_MESSAGE = 'Приветную господин. Что будем делать c категориями?'
    CREATE_POST_TITLE = 'Ведите заголовок объявления.'
    CREATE_POST_TEXT = 'Введите текст объявления.'
    CHOICE_CATEGORY = 'Выберите категорию.'

    TITLE = 'title'
    TEXT = 'text'
    CATEGORY = 'category'

    POST = 'post'
    CATEGORY = 'category'
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'

    CREATE_POST = 'create_post'

    def gather_command(self):
        self.new_command = self.callback_data + '_' + self.location
