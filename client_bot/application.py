from pyrogram import Client as Pyrogram_Client
from servece.mesages import Message


class Client(Pyrogram_Client, Message):
    START_MESSAGE = 'HELLO'

    async def send_start_message(self) -> None:
        await self.send_message(self.chat_id, self.START_MESSAGE)


app = Client('my_bot',
             api_id=13542258,
             api_hash='a5fbecad0687312eb8fea06d7a88b399',
             bot_token='5279728090:AAF_0JTxKynunlPiB1KPidXsxloFoIrcvrA'
             )
