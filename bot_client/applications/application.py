import os
import typing
from pprint import pprint
from collections.abc import Generator
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
        self.msg: Generator | None = None


app = Client('my_bot',
             api_id=int(os.getenv('api_id')),
             api_hash=os.getenv('api_hash'),
             bot_token=os.getenv('bot_token')
             )

CHANNEL = os.getenv('CHANNEL')
NAME_CHANNEL = os.getenv('NAME_CHANEL')
