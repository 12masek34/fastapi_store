from pyrogram.types.messages_and_media.message import Message
from applications.application import Client
from pyrogram.types.bots_and_keyboards.callback_query import CallbackQuery

from handlers.handler_message import HandlerMessageText
from handlers.handler_callbackdata import HandlerCallbackData


class Handler:
    def __init__(self, app: 'Client', data: Message | CallbackQuery):
        self.message_text = HandlerMessageText(app, data)
        self.callback_data = HandlerCallbackData(app, data)
