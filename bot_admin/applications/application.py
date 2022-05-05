import os
from dotenv import load_dotenv
from pyrogram import Client as PyrogramClient
from applications.commands import Command
from applications.mesages import MessageMixin
from applications.cache import Deque
from schemas.schema import PostSchema, CategorySchema, TokenUserSchema, ImageSchema
from applications.api_query import Api
from applications.keyboards import Keyboard
from event.handler import EventHandler
from exceptions.exception import MyException

load_dotenv()


class Client(PyrogramClient, MessageMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = TokenUserSchema()
        self.cache = Deque()
        self.cache.append('start')
        self.post = PostSchema()
        self.category = CategorySchema()
        self.command = Command()
        self.query_to_api = Api()
        self.keyboard = Keyboard()
        self.event_handler = EventHandler()
        self.exception = MyException()
        self.image = ImageSchema()

    def create_preview_post(self) -> str:
        title_category = ''
        for category in self.query_to_api.categories:
            if category['id'] == self.post.category_id:
                title_category = category['title']

        return (f'Категория:  {title_category}\n Заголовок объявления: {self.post.title}'
                f'\nТекст объявления: {self.post.text}\n')

    def create_preview_category(self) -> str:
        return self.category.title

    @staticmethod
    def create_delete_response_message(text) -> str:
        return f'{text} удалена.'


app = Client('my_bot',
             api_id=int(os.getenv('api_id')),
             api_hash=os.getenv('api_hash'),
             bot_token=os.getenv('bot_token')
             )

CHANNEL = os.getenv('CHANNEL')
NAME_CHANNEL = os.getenv('NAME_CHANEL')
