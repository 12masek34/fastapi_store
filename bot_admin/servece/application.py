from pyrogram import Client as Pyrogram_Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .commands import Command
from .mesages import Message
from .my_deque import Deque
from .schema import Post


class Client(Pyrogram_Client, Message):
    START_KEYBOARD = [
        [InlineKeyboardButton('Объявления', callback_data='post')],
        [InlineKeyboardButton('Категории', callback_data='category')]
    ]

    CRUD_KEYBOARD = [
        [InlineKeyboardButton('создать', callback_data='create')],
        [InlineKeyboardButton('изменить', callback_data='update')],
        [InlineKeyboardButton('удалить', callback_data='delete')]
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cash = Deque()
        self.cash.append('start')
        self.post = Post()
        self.command = Command()

    async def send_start_message(self) -> None:
        await self.send_message(self.chat_id, self.command.START_MESSAGE)

    async def parse_message_text(self) -> None:
        if self.text_message in self.command.START:
            await self.send_message(self.chat_id, self.command.START_MESSAGE,
                                    reply_markup=InlineKeyboardMarkup(self.START_KEYBOARD))
        elif self.cash.get_last_element() == self.command.CREATE_POST:
            self.post.title = self.text_message
            await self.send_message(self.chat_id, self.command.CREATE_POST_TEXT)
            self.cash.append(self.command.TITLE)
        elif self.cash.get_last_element() == self.command.TITLE:
            self.post.text = self.text_message
            await self.send_message(self.chat_id, self.command.CHOICE_CATEGORY)

    async def parser_callback_data(self):
        if self.callback_data == self.command.POST:
            await bot.delete_messages(bot.chat_id, bot.message_id)
            await self.send_message(self.chat_id, self.command.POST_MESSAGE,
                                    reply_markup=InlineKeyboardMarkup(self.CRUD_KEYBOARD))
            self.cash.append(self.callback_data)
        elif self.callback_data == self.command.CATEGORY:
            await bot.delete_messages(bot.chat_id, bot.message_id)
            await self.send_message(self.chat_id, self.command.CATEGORY_MESSAGE,
                                    reply_markup=InlineKeyboardMarkup(self.CRUD_KEYBOARD))
            self.cash.append(self.callback_data)
        elif self.callback_data == self.command.CREATE:
            self.command.callback_data = self.callback_data
            self.command.location = self.cash[-1]
            self.command.gather_command()
            if self.command.new_command == self.command.CREATE_POST:
                await bot.delete_messages(bot.chat_id, bot.message_id)
                await self.send_message(self.chat_id, self.command.CREATE_POST_TITLE)
                self.cash.append(self.command.new_command)


bot = Client('my_bot',
             api_id=13542258,
             api_hash='a5fbecad0687312eb8fea06d7a88b399',
             bot_token='5279728090:AAF_0JTxKynunlPiB1KPidXsxloFoIrcvrA'
             )
