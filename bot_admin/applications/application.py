import os
from dotenv import load_dotenv
from pyrogram import Client as PyrogramClient
from applications.commands import Command
from applications.mesages import MessageMixin
from applications.cache import Deque
from schemas.schema import PostSchema, CategorySchema, TokenUserSchema
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

    async def parse_message_text(self) -> None:
        """Обработчик текста. Так же проверяет и обрабатывает последний элемент cache."""

        if self.text_message in self.command.START:
            self.query_to_api.get_token(self.user)

            await self.send_message(self.chat_id, self.command.START_MESSAGE,
                                    reply_markup=self.keyboard.START)

        elif self.cache.last_element == self.command.ADD_CATEGORY_TO_POST:
            self.post.title = self.to_capitalize(self.text_message)
            await self.send_message(self.chat_id, self.command.CREATE_POST_TEXT_MESSAGE)
            self.cache.append(self.command.add_title)

        elif self.cache.last_element == self.command.add_title:
            self.post.text = self.to_capitalize(self.text_message)
            preview_post = self.create_preview_post()
            await self.send_message(self.chat_id, preview_post,
                                    reply_markup=self.keyboard.SAVE_CANCEL)
            self.cache.append(self.command.add_text)
            self.cache.append(self.command.create_post)

        elif self.cache.last_element == self.command.create_category:
            self.category.title = self.to_capitalize(self.text_message)
            preview_category = self.create_preview_category()
            await self.send_message(self.chat_id, preview_category,
                                    reply_markup=self.keyboard.SAVE_CANCEL)

            self.cache.append(self.command.add_title_category)
            self.cache.append(self.command.create_category)

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
            categories = self.query_to_api.get_all_category()
            keyboard = self.keyboard.create_keyboard_add_category(categories)
            await self.event_handler.executor_event(self.command.DELETE_AND_SEND_MESSAGE, chat_id=self.chat_id,
                                                    message_id=self.message_id,
                                                    command=self.command.CHOICE_CATEGORY_MESSAGE,
                                                    keyboard=keyboard)
            self.cache.append(self.command.create_post)

        elif self.command.ADD_CATEGORY_TO_POST in self.callback_data.data:
            category_id = self.callback_data.parse_category_id()
            self.post.category_id = category_id
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
            self.cache.append(self.command.create_post_completed)
            await self.send_message(self.chat_id, self.command.START_MESSAGE,
                                    reply_markup=self.keyboard.START)

        elif self.callback_data.data == self.command.SAVE and self.command.create_category in self.cache.last_element:
            if self.query_to_api.add_category(self.category) == 201:
                await self.event_handler.executor_event(self.command.DELETE_AND_SEND_MESSAGE, chat_id=self.chat_id,
                                                        message_id=self.message_id,
                                                        command=self.command.CREATE_CATEGORY_MESSAGE)
            else:
                pass
            self.cache.append(self.command.create_category_completed)
            await self.send_message(self.chat_id, self.command.START_MESSAGE,
                                    reply_markup=self.keyboard.START)

        elif self.callback_data.data == self.command.CREATE and self.cache.last_element == self.command.CATEGORY:
            await self.event_handler.executor_event(self.command.DELETE_AND_SEND_MESSAGE, chat_id=self.chat_id,
                                                    message_id=self.message_id,
                                                    command=self.command.CREATE_CATEGORY_TITLE_MESSAGE)
            self.cache.append(self.command.create_category)

        elif self.callback_data.data == self.command.DELETE and self.cache.last_element == self.command.CATEGORY:
            categories = self.query_to_api.get_all_category()
            if len(categories) == 0:
                await self.send_message(self.chat_id, self.command.ERROR_CATEGORY,
                                        reply_markup=self.keyboard.START)
            keyboard = self.keyboard.delete_keyboard_category(categories)
            await self.event_handler.executor_event(self.command.DELETE_AND_SEND_MESSAGE, chat_id=self.chat_id,
                                                    message_id=self.message_id,
                                                    command=self.command.CHOICE_CATEGORY_MESSAGE, keyboard=keyboard)
            self.cache.append(self.command.delete_category)

        elif (self.cache.last_element == self.command.delete_category and self.command.delete_category
              in self.callback_data.data):

            category_id = self.callback_data.parse_category_id()
            self.cache.append(self.command.delete_category_completed)
            self.query_to_api.get_category(category_id)
            category = self.query_to_api.category["title"]
            keyboard = self.keyboard.DELETE_CANCEL
            await self.event_handler.executor_event(self.command.DELETE_AND_SEND_MESSAGE, chat_id=self.chat_id,
                                                    message_id=self.message_id,
                                                    command=f'Удалить {category}?', keyboard=keyboard)
            self.cache.append(self.command.delete_category)

        elif self.cache.last_element == self.command.delete_category and self.callback_data.data == self.command.DELETE:
            category_id = self.query_to_api.category['id']
            self.query_to_api.delete_category(category_id)
            await self.send_message(self.chat_id, f'{self.query_to_api.category["title"]} удалена.')
            await self.send_message(self.chat_id, self.command.START_MESSAGE,
                                    reply_markup=self.keyboard.START)
            self.cache.append(self.command.delete_category_completed)

    # async def send_start_message(self) -> None:
    #     await self.send_message(self.chat_id, self.command.START_MESSAGE)

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
