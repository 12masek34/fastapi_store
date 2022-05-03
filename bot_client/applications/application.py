import os
import typing
from pyrogram import Client as PyrogramClient
from applications.commands import Command
from applications.keyboards import Keyboard
from applications.cache import Deque
from applications.api_query import Api
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

    async def parse_message_text(self, message: 'Message') -> None:
        '''Обработчик текста сообщений.'''
        if message.text.lower() in self.command.START:
            self.query_to_api.get()
            await self.send_message(message.chat.id, self.command.START_MESSAGE, reply_markup=self.keyboard.START)

    async def parser_callback_data(self, callback_query: CallbackQuery) -> None:
        """Обработчик данных от клавиатуры"""
        if callback_query.data == self.command.CATEGORY:





app = Client('my_bot',
             api_id=int(os.getenv('api_id')),
             api_hash=os.getenv('api_hash'),
             bot_token=os.getenv('bot_token')
             )
