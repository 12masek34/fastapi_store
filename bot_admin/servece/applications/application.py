import os
from dotenv import load_dotenv
from pyrogram import Client as Pyrogram_Client
from servece.applications.commands import Command
from servece.applications.mesages import Message
from servece.applications.deques import Deque
from servece.schemas.schema import PostSchema, CategorySchema, TokenUserSchema
from servece.applications.apies import Api
from servece.applications.keyboards import Keyboard
from servece.event.handler import EventHandler
from servece.exceptions.exception import MyException

load_dotenv()


class Client(Pyrogram_Client, Message):

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

    async def parse_message_text(self) -> None:
        """Обработчик текста. Так же проверяет и обрабатывает последний элемент cache."""

        if self.text_message in self.command.START:
            self.query_to_api.get_token(bot.user)

            await self.send_message(self.chat_id, self.command.START_MESSAGE,
                                    reply_markup=self.keyboard.START)

        elif self.cache.last_element == self.command.ADD_CATEGORY_TO_POST:
            self.post.title = self.to_capitalize(self.text_message)
            await self.send_message(self.chat_id, self.command.CREATE_POST_TEXT_MESSAGE)
            self.cache.append(self.command.ADD_TITLE)

        elif self.cache.last_element == self.command.ADD_TITLE:
            self.post.text = self.to_capitalize(self.text_message)
            preview_post = self.create_preview_post()
            await self.send_message(self.chat_id, preview_post,
                                    reply_markup=self.keyboard.SAVE_CANCEL)
            self.cache.append(self.command.ADD_TEXT)
            self.cache.append(self.command.NEW_POST)

        elif self.cache.last_element == self.command.NEW_CATEGORY:
            self.category.title = self.to_capitalize(self.text_message)
            preview_category = self.create_preview_category()
            await self.send_message(self.chat_id, preview_category,
                                    reply_markup=self.keyboard.SAVE_CANCEL)

            self.cache.append(self.command.add_title_category)
            self.cache.append(self.command.NEW_CATEGORY)

    async def parser_callback_data(self) -> None:
        """Обработчик данных от клавиатуры"""

        if self.callback_data.data == self.command.POST:
            await self.event_handler.executor_event(self.command.DELETE_AND_SEND_MESSAGE, chat_id=self.chat_id,
                                                    message_id=self.message_id, command=self.command.POST_MESSAGE,
                                                    keyboard=self.keyboard.CRUD)
            self.cache.append(self.callback_data.data)

        elif self.callback_data.data == self.command.CATEGORY:
            await self.event_handler.executor_event(self.command.DELETE_AND_SEND_MESSAGE, chat_id=self.chat_id,
                                                    message_id=self.message_id, command=self.command.CATEGORY_MESSAGE,
                                                    keyboard=self.keyboard.CRUD)
            self.cache.append(self.callback_data.data)

        elif self.callback_data.data == self.command.CREATE and self.cache.last_element == self.command.POST:
            self.query_to_api.get_all_category()
            self.keyboard.create_keyboard_category(self.query_to_api.categories)
            await self.event_handler.executor_event(self.command.DELETE_AND_SEND_MESSAGE, chat_id=self.chat_id,
                                                    message_id=self.message_id,
                                                    command=self.command.CHOICE_CATEGORY_MESSAGE,
                                                    keyboard=self.keyboard.category)
            self.cache.append(self.command.NEW_POST)

        elif self.command.ADD_CATEGORY_TO_POST in self.callback_data.data:
            self.callback_data.parse_category_id()
            self.post.category_id = self.callback_data.category_id
            await self.event_handler.executor_event(self.command.DELETE_AND_SEND_MESSAGE, chat_id=self.chat_id,
                                                    message_id=self.message_id,
                                                    command=self.command.CREATE_POST_TITLE_MESSAGE)
            self.cache.append(self.command.ADD_CATEGORY_TO_POST)

        elif self.callback_data.data == self.command.SAVE and self.command.create_post in self.cache.last_element:
            if self.query_to_api.add_post(self.post) == 201:
                await self.event_handler.executor_event(self.command.DELETE_AND_SEND_MESSAGE, chat_id=self.chat_id,
                                                        message_id=self.message_id,
                                                        command=self.command.CREATE_POST_MESSAGE)
            else:
                pass
            self.cache.append(self.command.CREATE_POST_COMPLETED)
            await self.send_message(self.chat_id, self.command.START_MESSAGE,
                                    reply_markup=self.keyboard.START)

        elif self.callback_data.data == self.command.SAVE and self.command.create_category in self.cache.last_element:
            if self.query_to_api.add_category(self.category) == 201:
                await self.event_handler.executor_event(self.command.DELETE_AND_SEND_MESSAGE, chat_id=self.chat_id,
                                                        message_id=self.message_id,
                                                        command=self.command.CREATE_CATEGORY_MESSAGE)
            else:
                pass
            self.cache.append(self.command.CREATE_CATEGORY_COMPLETED)
            await self.send_message(self.chat_id, self.command.START_MESSAGE,
                                    reply_markup=self.keyboard.START)

        elif self.callback_data.data == self.command.CREATE and self.cache.last_element == self.command.CATEGORY:
            await self.event_handler.executor_event(self.command.DELETE_AND_SEND_MESSAGE, chat_id=self.chat_id,
                                                    message_id=self.message_id,
                                                    command=self.command.CREATE_CATEGORY_TITLE_MESSAGE)
            self.cache.append(self.command.NEW_CATEGORY)

    async def send_start_message(self) -> None:
        await self.send_message(self.chat_id, self.command.START_MESSAGE)

    def create_preview_post(self) -> str:
        title_category = ''
        for category in self.query_to_api.categories:
            if category['id'] == self.post.category_id:
                title_category = category['title']

        return (f'Категория:  {title_category}\n Заголовок объявления: {self.post.title}'
                f'\nТекст объявления: {self.post.text}\n')

    def create_preview_category(self) -> str:
        return self.category.title


bot = Client('my_bot',
             api_id=int(os.getenv('api_id')),
             api_hash=os.getenv('api_hash'),
             bot_token=os.getenv('bot_token')
             )
