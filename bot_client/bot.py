import typing
from applications.application import app

if typing.TYPE_CHECKING:
    from applications.application import Client
    from pyrogram.types.messages_and_media.message import Message
    from pyrogram.types.bots_and_keyboards.callback_query import CallbackQuery


@app.on_message()
async def message_handler(client: 'Client', message: 'Message'):
    app.user.username = message.from_user.username
    app.user.password = str(message.from_user.id)
    if message.text.lower() in app.command.START:
        app.query_to_api.get_token(app.user)
        await app.send_message(message.chat.id, app.command.START_MESSAGE, reply_markup=app.keyboard.START)


@app.on_callback_query()
async def answer(client: 'Client', callback_query: 'CallbackQuery'):
    if callback_query.data == app.command.CATEGORY:
        categories = app.query_to_api.get_all_category()
        keyboard = app.keyboard.create_keyboard_category(categories)
        await app.send_message(callback_query.message.chat.id, app.command.CHOICE_CATEGORY_MESSAGE,
                               reply_markup=keyboard)
        app.cache.append(app.command.CATEGORY)

    elif app.command.SELECTED_CATEGORY_PATTERN in callback_query.data:
        category_id = app.command.get_category_id(callback_query.data)
        posts = app.query_to_api.get_posts_filter_by_category_id(category_id)
        msg = app.command.create_message_posts(posts)
        await app.send_message(callback_query.message.chat.id, msg)
