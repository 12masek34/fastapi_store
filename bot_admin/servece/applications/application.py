from pyrogram import Client as Pyrogram_Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from servece.applications.commands import Command
from servece.applications.mesages import Message
from servece.applications.deques import Deque
from servece.schemas.schema import Post
from servece.applications.apies import Api
from servece.applications.keyboards import Keyboard


class Client(Pyrogram_Client, Message):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = Deque()
        self.cache.append('start')
        self.post = Post()
        self.command = Command()
        self.api = Api()
        self.keyboard = Keyboard()

    async def parse_message_text(self) -> None:
        if self.text_message in self.command.START:
            await self.send_message(self.chat_id, self.command.START_MESSAGE,
                                    reply_markup=InlineKeyboardMarkup(self.keyboard.START))
        elif self.cache.get_last_element() == self.command.CREATE_POST:
            self.post.title = self.text_message
            await self.send_message(self.chat_id, self.command.CREATE_POST_TEXT)
            self.cache.append(self.command.TITLE)
        elif self.cache.get_last_element() == self.command.TITLE:
            self.post.text = self.text_message
            self.cache.append(self.command.TEXT)
            self.api.get_all_category()
            self.keyboard.create_keyboard_category(self.api.categories)
            await self.send_message(self.chat_id, self.command.CHOICE_CATEGORY,
                                    reply_markup=InlineKeyboardMarkup(self.keyboard.category))

    async def parser_callback_data(self):
        if self.callback_data.data == self.command.POST:
            await bot.delete_messages(bot.chat_id, bot.message_id)
            await self.send_message(self.chat_id, self.command.POST_MESSAGE,
                                    reply_markup=InlineKeyboardMarkup(self.keyboard.CRUD))
            self.cache.append(self.callback_data.data)

        elif self.callback_data == self.command.CATEGORY:
            await bot.delete_messages(bot.chat_id, bot.message_id)
            await self.send_message(self.chat_id, self.command.CATEGORY_MESSAGE,
                                    reply_markup=InlineKeyboardMarkup(self.keyboard.CRUD))
            self.cache.append(self.callback_data.data)

        elif self.callback_data.data == self.command.CREATE:

            self.command.callback_data = self.callback_data.data
            self.command.location = self.cache.get_last_element()
            self.command.gather_command()
            if self.command.new_command == self.command.CREATE_POST:
                await bot.delete_messages(bot.chat_id, bot.message_id)
                await self.send_message(self.chat_id, self.command.CREATE_POST_TITLE)

                self.cache.append(self.command.CREATE_POST)

        elif self.command.ADD_CATEGORY in self.callback_data.data:

            self.callback_data.parse_category_id()
            self.post.category = self.callback_data.category_id
            self.cache.append(self.command.CREATE_POST_COMPLETED)
            self.create_preview_post(self.post)
            await bot.delete_messages(bot.chat_id, bot.message_id)
            await bot.send_message(self.chat_id, self.preview_post)

            self.cache.append(self.command.CREATE_PREVIEW_POST)

    async def send_start_message(self) -> None:
        await self.send_message(self.chat_id, self.command.START_MESSAGE)

    def create_preview_post(self, post: Post):
        title_category = ''
        for category in self.api.categories:
            if category['id'] == post.category:
                title_category = category['title']

        self.preview_post = (f'Заголовок объявления: {post.title}\nТекст объявления: {post.text}\n'
                             f'Категория:  {title_category}')


bot = Client('my_bot',
             api_id=13542258,
             api_hash='a5fbecad0687312eb8fea06d7a88b399',
             bot_token='5279728090:AAF_0JTxKynunlPiB1KPidXsxloFoIrcvrA'
             )
