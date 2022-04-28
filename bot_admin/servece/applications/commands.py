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
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'

    CREATE_POST = 'create_post'
    ADD_CATEGORY = 'add_category'
    CREATE_POST_COMPLETED = 'create_post_completed'
    CREATE_PREVIEW_POST = 'create_preview_post'


    def gather_command(self):
        self.new_command = self.callback_data + '_' + self.location
