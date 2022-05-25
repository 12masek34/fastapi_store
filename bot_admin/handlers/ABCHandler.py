from abc import ABC, abstractmethod

import typing

if typing.TYPE_CHECKING:
    from pyrogram.types.messages_and_media.message import Message
    from applications.application import Client
    from pyrogram.types.bots_and_keyboards.callback_query import CallbackQuery


class MyHandler(ABC):

    def __init__(self, app: 'Client'):
        self._app = app


class MyHandlerText(MyHandler):
    def __init__(self, app: 'Client', message: 'Message'):
        super().__init__(app)
        self._message = message


class MyHandlerCallbackData(MyHandler):
    def __init__(self, app: 'Client', callback_query: 'CallbackQuery'):
        super().__init__(app)
        self._callback_data = callback_query
