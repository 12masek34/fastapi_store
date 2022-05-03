import typing
from applications.application import bot
from pyrogram.errors.exceptions.forbidden_403 import Forbidden

if typing.TYPE_CHECKING:
    from applications.application import Client


@bot.on_message()
async def message_handler(client: 'Client', message):
    bot.user.username = message.from_user.username
    bot.user.password = str(message.from_user.id)
    bot.text_message = message.text
    bot.chat_id = message.chat.id
    bot.message_id = message.id
    await bot.parse_message_text()


@bot.on_callback_query()
async def answer(client, callback_query):
    try:
        bot.callback_data.data = callback_query.data
        bot.chat_id = callback_query.message.chat.id
        bot.message_id = callback_query.message.id
        await bot.parser_callback_data()
    except Forbidden:
        await bot.send_message(bot.chat_id, bot.exception.FORBIDDEN_MESSAGE)

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
