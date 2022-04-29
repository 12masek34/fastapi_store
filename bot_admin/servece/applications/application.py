from pyrogram import Client as Pyrogram_Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from servece.applications.commands import Command
from servece.applications.mesages import Message
from servece.applications.deques import Deque
from servece.schemas.schema import PostSchema
from servece.applications.apies import Api
from servece.applications.keyboards import Keyboard


class Client(Pyrogram_Client, Message):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = Deque()
        self.cache.append('start')
        self.post = PostSchema()
        self.command = Command()
        self.query_to_api = Api()
        self.keyboard = Keyboard()

    async def parse_message_text(self) -> None:
        if self.text_message in self.command.START:
            await self.send_message(self.chat_id, self.command.START_MESSAGE,
                                    reply_markup=InlineKeyboardMarkup(self.keyboard.START))

        elif self.cache.last_element == self.command.ADD_CATEGORY_TO_POST:
            self.post.title = self.to_capitalize(self.text_message)
            await self.send_message(self.chat_id, self.command.CREATE_POST_TEXT)
            self.cache.append(self.command.ADD_TITLE)

        elif self.cache.last_element == self.command.ADD_TITLE:
            self.post.text = self.to_capitalize(self.text_message)
            self.create_preview_post()
            await self.send_message(self.chat_id, self.preview_post,
                                    reply_markup=InlineKeyboardMarkup(self.keyboard.SAVE_CANCEL))
            self.cache.append(self.command.ADD_TEXT)
            self.cache.append(self.command.NEW_POST)

    async def parser_callback_data(self):
        if self.callback_data.data == self.command.POST:
            await self.delete_messages(self.chat_id, self.message_id)
            await self.send_message(self.chat_id, self.command.POST_MESSAGE,
                                    reply_markup=InlineKeyboardMarkup(self.keyboard.CRUD))
            self.cache.append(self.callback_data.data)

        elif self.callback_data == self.command.CATEGORY:
            await self.delete_messages(self.chat_id, self.message_id)
            await self.send_message(self.chat_id, self.command.CATEGORY_MESSAGE,
                                    reply_markup=InlineKeyboardMarkup(self.keyboard.CRUD))
            self.cache.append(self.callback_data.data)

        elif self.callback_data.data == self.command.CREATE and self.cache.last_element == self.command.POST:
            self.query_to_api.get_all_category()
            self.keyboard.create_keyboard_category(self.query_to_api.categories)
            await self.delete_messages(self.chat_id, self.message_id)
            await self.send_message(self.chat_id, self.command.CHOICE_CATEGORY,
                                    reply_markup=InlineKeyboardMarkup(self.keyboard.category))
            self.cache.append(self.command.NEW_POST)

        elif self.command.ADD_CATEGORY_TO_POST in self.callback_data.data:

            self.callback_data.parse_category_id()
            self.post.category_id = self.callback_data.category_id
            await self.delete_messages(self.chat_id, self.message_id)
            await self.send_message(self.chat_id, self.command.CREATE_POST_TITLE)
            self.cache.append(self.command.ADD_CATEGORY_TO_POST)

        elif self.callback_data.data == self.command.SAVE and self.command.CREATE in self.cache.last_element:
            self.query_to_api.add_post(self.post)
            await self.delete_messages(self.chat_id, self.message_id)
            await self.send_message(self.chat_id, self.command.CREATE_POST)
            self.cache.append(self.command.CREATE_POST_COMPLETED)
            await self.send_message(self.chat_id, self.command.START_MESSAGE,
                                    reply_markup=InlineKeyboardMarkup(self.keyboard.START))

    async def send_start_message(self) -> None:
        await self.send_message(self.chat_id, self.command.START_MESSAGE)

    def create_preview_post(self):
        title_category = ''
        for category in self.query_to_api.categories:
            if category['id'] == self.post.category_id:
                title_category = category['title']

        self.preview_post = (f'Категория:  {title_category}\n Заголовок объявления: {self.post.title}'
                             f'\nТекст объявления: {self.post.text}\n')


bot = Client('my_bot',
             api_id=13542258,
             api_hash='a5fbecad0687312eb8fea06d7a88b399',
             bot_token='5279728090:AAF_0JTxKynunlPiB1KPidXsxloFoIrcvrA'
             )
