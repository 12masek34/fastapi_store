import typing
from applications.application import app
from pyrogram.errors.exceptions.forbidden_403 import Forbidden

if typing.TYPE_CHECKING:
    from applications.application import Client


@app.on_message()
async def message_handler(client: 'Client', message):
    app.user.username = message.from_user.username
    app.user.password = str(message.from_user.id)
    app.text_message = message.text
    app.chat_id = message.chat.id
    app.message_id = message.id
    await app.parse_message_text()


@app.on_callback_query()
async def answer(client, callback_query):
    try:
        app.callback_data.data = callback_query.data
        app.chat_id = callback_query.message.chat.id
        app.message_id = callback_query.message.id
        await app.parser_callback_data()
    except Forbidden:
        await app.send_message(app.chat_id, app.exception.FORBIDDEN_MESSAGE)

    # if bot.cash.get_last_element() == bot.START:
    #     bot.post.title = bot.text_message
    #     bot.cash.append(bot.TITLE)
    #     await bot.send_message(bot.chat_id, 'write title text')
    # elif bot.cash.get_last_element() == bot.TITLE:
    #     bot.post.text = bot.text_message
    #     # await bot.delete_messages(bot.chat_id, bot.message_id)
    #     await bot.send_message(bot.chat_id, 'write text post')
    #     bot.cash.append(bot.TEXT)
    # elif bot.cash.get_last_element() == bot.TEXT:
    #     # await bot.delete_messages(bot.chat_id, bot.message_id)
    #     await bot.send_message(bot.chat_id, 'write category post')
    #     bot.post.category = bot.text_message
