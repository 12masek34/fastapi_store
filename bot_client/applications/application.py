import os
import typing
from pprint import pprint

from pyrogram import Client as PyrogramClient
from applications.commands import Command
from applications.keyboards import Keyboard
from applications.cache import Deque
from applications.api_query import Api
from schemas.schema import TokenUserSchema
from dotenv import load_dotenv

if typing.TYPE_CHECKING:
    from pyrogram.types.messages_and_media.message import Message
    from pyrogram.types.bots_and_keyboards.callback_query import CallbackQuery

load_dotenv()


class Client(PyrogramClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = Command()
        self.keyboard = Keyboard()
        self.cache = Deque()
        self.query_to_api = Api()
        self.user = TokenUserSchema()

    async def parse_message_text(self, message: 'Message') -> None:
        '''Обработчик текста сообщений.'''

        if message.text.lower() in self.command.START:
            self.query_to_api.get_token(self.user)
            await self.send_message(message.chat.id, self.command.START_MESSAGE, reply_markup=self.keyboard.START)

    async def parser_callback_data(self, callback_query: 'CallbackQuery') -> None:
        '''Обработчик данных от клавиатуры'''

        if callback_query.data == self.command.CATEGORY:
            categories = self.query_to_api.get_all_category()
            keyboard = self.keyboard.create_keyboard_category(categories)
            await self.send_message(callback_query.message.chat.id, self.command.CHOICE_CATEGORY_MESSAGE,
                                    reply_markup=keyboard)
            self.cache.append(self.command.CATEGORY)

        elif self.command.SELECTED_CATEGORY_PATTERN in callback_query.data:
            category_id = self.command.get_category_id(callback_query.data)
            posts = self.query_to_api.get_posts_filter_by_category_id(category_id)

            msg = ''
            for post in posts:
                msg = msg + (f'{post["title"]}\n'
                             f'{post["text"]}\n'
                             f'{post["created_at"]}'
                             f'\n')
            await self.send_message(callback_query.message.chat.id, msg)


app = Client('my_bot',
             api_id=int(os.getenv('api_id')),
             api_hash=os.getenv('api_hash'),
             bot_token=os.getenv('bot_token')
             )
