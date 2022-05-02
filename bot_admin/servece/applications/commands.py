class Command:
    def __init__(self):
        self.callback_data: str | None = None
        self.location: str | None = None
        self.new_command: str | None = None

    START = ['/start', 'start']

    START_MESSAGE = 'Что будем делать?'
    POST_MESSAGE = 'Приветную господин. Что будем делать c постами?'
    CATEGORY_MESSAGE = 'Приветную господин. Что будем делать c категориями?'
    CREATE_POST_TITLE_MESSAGE = 'Ведите заголовок объявления.'
    CREATE_POST_TEXT_MESSAGE = 'Введите текст объявления.'
    CHOICE_CATEGORY_MESSAGE = 'Выберите категорию.'
    CREATE_POST_MESSAGE = 'Объявление успешно добавлено.'
    CREATE_CATEGORY_MESSAGE = 'Категория успешно добавлена.'
    CREATE_CATEGORY_TITLE_MESSAGE = ' Введите название категории.'

    ADD_TITLE = 'add_title'
    ADD_TEXT = 'add_text'

    CATEGORY = 'category'
    POST = 'post'

    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    SAVE = 'save'

    NEW_POST = 'create_post'
    NEW_CATEGORY = 'create_category'
    ADD_CATEGORY_TO_POST = 'add_category_to_post'
    CREATE_POST_COMPLETED = 'create_post_completed'
    CREATE_CATEGORY_COMPLETED = 'create_category_completed'

    DELETE_AND_SEND_MESSAGE = 'delete_and_send_message'

    def gather_command(self) -> None:
        self.new_command = self.callback_data + '_' + self.location

    @property
    def add_title_category(self) -> str:
        return self.ADD_TITLE + '_' + self.CATEGORY

    @property
    def create_post(self) -> str:
        return self.CREATE + '_' + self.POST

    @property
    def create_category(self) -> str:
        return self.CREATE + '_' + self.CATEGORY
