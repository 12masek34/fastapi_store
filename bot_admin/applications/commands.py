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
    CREATE_IMAGE_POST_MESSAGE = 'Добавьте фото объявления.'
    SAVE_MESSAGE = 'Сохранить?'
    EMPTY_CATEGORY_MESSAGE = 'Ни чего нет.'

    ERROR_CATEGORY = 'Нет не одной категории.'

    TITLE = 'title'
    TEXT = 'text'

    CATEGORY = 'category'
    POST = 'post'
    PHOTO = 'photo'

    SEND = 'send'
    ADD = 'add'
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    SAVE = 'save'
    COMPLETED = 'completed'

    ADD_CATEGORY_TO_POST = 'add_category_to_post'

    DELETE_AND_SEND_MESSAGE = 'delete_and_send_message'

    def gather_command(self) -> None:
        self.new_command = self.callback_data + '_' + self.location

    @property
    def add_text(self) -> str:
        return self.ADD + '_' + self.TEXT

    @property
    def add_text_post(self) -> str:
        return self.add_text + '_' + self.POST

    @property
    def add_title(self) -> str:
        return self.ADD + '_' + self.TITLE

    @property
    def add_title_category(self) -> str:
        return self.ADD + '_' + self.TITLE + '_' + self.CATEGORY

    @property
    def create_post(self) -> str:
        return self.CREATE + '_' + self.POST

    @property
    def create_category(self) -> str:
        return self.CREATE + '_' + self.CATEGORY

    @property
    def delete_category(self) -> str:
        return self.DELETE + '_' + self.CATEGORY

    @property
    def delete_category_completed(self) -> str:
        return self.DELETE + '_' + self.CATEGORY + '_' + self.COMPLETED

    @property
    def create_category_completed(self) -> str:
        return self.CREATE + '_' + self.CATEGORY + '_' + self.COMPLETED

    @property
    def create_post_completed(self) -> str:
        return self.CREATE + '_' + self.POST + '_' + self.COMPLETED

    @property
    def add_photo(self) -> str:
        return self.ADD + '_' + self.PHOTO

    @property
    def send_photo(self) -> str:
        return self.SEND + '_' + self.PHOTO
