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
    if app.text_message in app.command.START:
        app.query_to_api.get_token(app.user)

        await app.send_message(app.chat_id, app.command.START_MESSAGE,
                               reply_markup=app.keyboard.START)

    elif app.cache.last_element == app.command.ADD_CATEGORY_TO_POST:
        app.post.title = app.to_capitalize(app.text_message)
        await app.send_message(app.chat_id, app.command.CREATE_POST_TEXT_MESSAGE)
        app.cache.append(app.command.add_title)

    elif app.cache.last_element == app.command.add_title:
        app.post.text = app.to_capitalize(app.text_message)
        preview_post = app.create_preview_post()
        await app.send_message(app.chat_id, preview_post,
                               reply_markup=app.keyboard.SAVE_CANCEL)
        app.cache.append(app.command.add_text)
        app.cache.append(app.command.create_post)

    elif app.cache.last_element == app.command.create_category:
        app.category.title = app.to_capitalize(app.text_message)
        preview_category = app.create_preview_category()
        await app.send_message(app.chat_id, preview_category,
                               reply_markup=app.keyboard.SAVE_CANCEL)

        app.cache.append(app.command.add_title_category)
        app.cache.append(app.command.create_category)


@app.on_callback_query()
async def answer(client, callback_query):
    try:
        app.callback_data.data = callback_query.data
        app.chat_id = callback_query.message.chat.id
        app.message_id = callback_query.message.id
    except Forbidden:
        await app.send_message(app.chat_id, app.exception.FORBIDDEN_MESSAGE)
    if app.callback_data.data == app.command.POST:
        await app.event_handler.executor_event(app.command.DELETE_AND_SEND_MESSAGE, chat_id=app.chat_id,
                                               message_id=app.message_id, command=app.command.POST_MESSAGE,
                                               keyboard=app.keyboard.CRUD)
        app.cache.append(app.callback_data.data)

    elif app.callback_data.data == app.command.CATEGORY:
        await app.event_handler.executor_event(app.command.DELETE_AND_SEND_MESSAGE, chat_id=app.chat_id,
                                               message_id=app.message_id, command=app.command.CATEGORY_MESSAGE,
                                               keyboard=app.keyboard.CRUD)
        app.cache.append(app.callback_data.data)

    elif app.callback_data.data == app.command.CREATE and app.cache.last_element == app.command.POST:
        categories = app.query_to_api.get_all_category()
        keyboard = app.keyboard.create_keyboard_add_category(categories)
        await app.event_handler.executor_event(app.command.DELETE_AND_SEND_MESSAGE, chat_id=app.chat_id,
                                               message_id=app.message_id,
                                               command=app.command.CHOICE_CATEGORY_MESSAGE,
                                               keyboard=keyboard)
        app.cache.append(app.command.create_post)

    elif app.command.ADD_CATEGORY_TO_POST in app.callback_data.data:
        category_id = app.callback_data.parse_category_id()
        app.post.category_id = category_id
        await app.event_handler.executor_event(app.command.DELETE_AND_SEND_MESSAGE, chat_id=app.chat_id,
                                               message_id=app.message_id,
                                               command=app.command.CREATE_POST_TITLE_MESSAGE)
        app.cache.append(app.command.ADD_CATEGORY_TO_POST)

    elif app.callback_data.data == app.command.SAVE and app.command.create_post in app.cache.last_element:
        if app.query_to_api.add_post(app.post) == 201:
            await app.event_handler.executor_event(app.command.DELETE_AND_SEND_MESSAGE, chat_id=app.chat_id,
                                                   message_id=app.message_id,
                                                   command=app.command.CREATE_POST_MESSAGE)
        else:
            pass
        app.cache.append(app.command.create_post_completed)
        await app.send_message(app.chat_id, app.command.START_MESSAGE,
                               reply_markup=app.keyboard.START)

    elif app.callback_data.data == app.command.SAVE and app.command.create_category in app.cache.last_element:
        if app.query_to_api.add_category(app.category) == 201:
            await app.event_handler.executor_event(app.command.DELETE_AND_SEND_MESSAGE, chat_id=app.chat_id,
                                                   message_id=app.message_id,
                                                   command=app.command.CREATE_CATEGORY_MESSAGE)
        else:
            pass
        app.cache.append(app.command.create_category_completed)
        await app.send_message(app.chat_id, app.command.START_MESSAGE,
                               reply_markup=app.keyboard.START)

    elif app.callback_data.data == app.command.CREATE and app.cache.last_element == app.command.CATEGORY:
        await app.event_handler.executor_event(app.command.DELETE_AND_SEND_MESSAGE, chat_id=app.chat_id,
                                               message_id=app.message_id,
                                               command=app.command.CREATE_CATEGORY_TITLE_MESSAGE)
        app.cache.append(app.command.create_category)

    elif app.callback_data.data == app.command.DELETE and app.cache.last_element == app.command.CATEGORY:
        categories = app.query_to_api.get_all_category()
        if len(categories) == 0:
            await app.send_message(app.chat_id, app.command.ERROR_CATEGORY,
                                   reply_markup=app.keyboard.START)
        else:
            keyboard = app.keyboard.delete_keyboard_category(categories)
            await app.event_handler.executor_event(app.command.DELETE_AND_SEND_MESSAGE, chat_id=app.chat_id,
                                                   message_id=app.message_id,
                                                   command=app.command.CHOICE_CATEGORY_MESSAGE, keyboard=keyboard)
            app.cache.append(app.command.delete_category)

    elif (app.cache.last_element == app.command.delete_category and app.command.delete_category
          in app.callback_data.data):

        category_id = app.callback_data.parse_category_id()
        app.cache.append(app.command.delete_category_completed)
        app.query_to_api.get_category(category_id)
        category = app.query_to_api.category['title']
        keyboard = app.keyboard.DELETE_CANCEL
        await app.event_handler.executor_event(app.command.DELETE_AND_SEND_MESSAGE, chat_id=app.chat_id,
                                               message_id=app.message_id,
                                               command=f'Удалить {category}?', keyboard=keyboard)
        app.cache.append(app.command.delete_category)

    elif app.cache.last_element == app.command.delete_category and app.callback_data.data == app.command.DELETE:
        category_id = app.query_to_api.category['id']
        app.query_to_api.delete_category(category_id)
        await app.send_message(app.chat_id, f'{app.query_to_api.category["title"]} удалена.')
        await app.send_message(app.chat_id, app.command.START_MESSAGE,
                               reply_markup=app.keyboard.START)
        app.cache.append(app.command.delete_category_completed)

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
