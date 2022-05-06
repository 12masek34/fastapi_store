import typing
from pprint import pprint

from applications.application import app, CHANNEL, NAME_CHANNEL

if typing.TYPE_CHECKING:
    from applications.application import Client
    from pyrogram.types.messages_and_media.message import Message
    from pyrogram.types.bots_and_keyboards.callback_query import CallbackQuery


@app.on_message()
async def message_handler(client: 'Client', message: 'Message'):
    if message.chat.title == NAME_CHANNEL:
        if message.photo:
            await app.send_message(CHANNEL, message.photo.file_id)

    elif message.text in app.command.START:
        app.user.username = message.from_user.username
        app.user.password = str(message.from_user.id)
        if message.text.lower() in app.command.START:
            app.query_to_api.get_token(app.user)
            categories = app.query_to_api.get_category_count()
            keyboard = app.keyboard.create_keyboard_category(categories)
            await app.send_message(message.chat.id, app.command.CHOICE_CATEGORY_MESSAGE,
                                   reply_markup=keyboard)
            app.cache.command.append(app.command.CATEGORY)


@app.on_callback_query()
async def answer(client: 'Client', callback_query: 'CallbackQuery'):
    if callback_query.data == app.command.all_post:
        posts = app.query_to_api.get_all_posts()
        msg = app.command.create_message_posts(posts)
        await app.send_message(callback_query.message.chat.id, msg)
        app.cache.command.append(app.command.all_post)

    elif app.command.SELECTED_CATEGORY_PATTERN in callback_query.data:
        category_id = app.command.get_category_id(callback_query.data)
        posts = app.query_to_api.get_posts_filter_by_category_id(category_id)
        app.posts = app.command.create_message_posts(posts)
        data = app.posts.pop()
        await app.send_photo(callback_query.message.chat.id, data.image)
        await app.send_message(callback_query.message.chat.id, data.text, reply_markup=app.keyboard.BACK_NEXT)
        app.cache.posts.append(data)
        app.cache.command.append(app.command.SELECT + '_' + app.command.SELECTED_CATEGORY_PATTERN + category_id)

    elif callback_query.data == app.command.NEXT:
        try:
            last_element = app.posts.last_element
            if last_element.text == callback_query.message.text:
                data = app.posts.pop()
                app.cache.posts.append(data)

            data = app.posts.pop()
            await app.send_photo(callback_query.message.chat.id, data.image)
            await app.send_message(callback_query.message.chat.id, data.text, reply_markup=app.keyboard.BACK_NEXT)
            app.cache.posts.append(data)
        except IndexError:
            app.query_to_api.get_token(app.user)
            categories = app.query_to_api.get_category_count()
            keyboard = app.keyboard.create_keyboard_category(categories)
            await app.send_message(callback_query.message.chat.id, app.command.CHOICE_CATEGORY_MESSAGE,
                                   reply_markup=keyboard)
            app.cache.command.append(app.command.CATEGORY)
            # todo обработать стоп итератор
    elif callback_query.data == app.command.BACK:
        try:
            last_element = app.cache.posts.last_element
            if last_element.text == callback_query.message.text:
                data = app.cache.posts.pop()
                app.posts.append(data)
            data = app.cache.posts.pop()
        except IndexError:
            app.query_to_api.get_token(app.user)
            categories = app.query_to_api.get_category_count()
            keyboard = app.keyboard.create_keyboard_category(categories)
            await app.send_message(callback_query.message.chat.id, app.command.CHOICE_CATEGORY_MESSAGE,
                                   reply_markup=keyboard)
            app.cache.command.append(app.command.CATEGORY)


        await app.send_photo(callback_query.message.chat.id, data.image)
        await app.send_message(callback_query.message.chat.id, data.text, reply_markup=app.keyboard.BACK_NEXT)
        app.cache.command.append(app.command.BACK)
        app.posts.append(data)