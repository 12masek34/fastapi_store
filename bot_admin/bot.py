import typing

from pyrogram.errors.exceptions.forbidden_403 import Forbidden

from applications.application import app, CHANNEL, NAME_CHANNEL
from handlers.my_handler import Handler

if typing.TYPE_CHECKING:
    from applications.application import Client
    from pyrogram.types.messages_and_media.message import Message
    from pyrogram.types.bots_and_keyboards.callback_query import CallbackQuery


@app.on_message()
async def message_handler(client: 'Client', message: 'Message'):
    handler = Handler(app, message)
    await handler.message_text.start()

    if message.chat.title == NAME_CHANNEL:
        app.image.img = message.text
        preview_message = app.create_preview_post()
        await app.send_message(app.chat_id, preview_message)
        await app.send_message(app.chat_id, app.command.SAVE_MESSAGE, reply_markup=app.keyboard.SAVE_CANCEL)
        app.cache.append(app.command.add_photo)

    elif message.text:
        app.user.username = message.from_user.username
        app.user.password = str(message.from_user.id)
        app.text_message = message.text
        app.chat_id = message.chat.id
        app.message_id = message.id

        # if app.text_message in app.command.START:
        #     app.query_to_api.get_token(app.user)
        #
        #     await app.send_message(app.chat_id, app.command.START_MESSAGE,
        #                            reply_markup=app.keyboard.START)

        if app.cache.last_element == app.command.ADD_CATEGORY_TO_POST:
            app.post.title = app.to_capitalize(app.text_message)
            await app.send_message(app.chat_id, app.command.CREATE_POST_TEXT_MESSAGE)
            app.cache.append(app.command.add_title)

        elif app.cache.last_element == app.command.add_title:
            app.post.text = app.to_capitalize(app.text_message)
            await app.send_message(app.chat_id, app.command.CREATE_IMAGE_POST_MESSAGE)
            app.cache.append(app.command.add_text_post)

        await handler.message_text.create_category()
        # elif app.cache.last_element == app.command.create_category:
        #     app.category.title = app.to_capitalize(app.text_message)
        #     preview_category = app.create_preview_category()
        #     await app.send_message(app.chat_id, preview_category,
        #                            reply_markup=app.keyboard.SAVE_CANCEL)

        # app.cache.append(app.command.add_title_category)
        # app.cache.append(app.command.create_category)

    elif message.photo is not None and app.cache.last_element == app.command.add_text_post:

        # todo ???????????????? ?????????????????? ???????????????????? ????????

        await app.send_photo(CHANNEL, message.photo.file_id)
        await app.delete_messages(message.chat.id, message.id)
        await app.send_photo(app.chat_id, message.photo.file_id)
        app.chat_id = message.chat.id
        app.cache.append(app.command.send_photo)


@app.on_callback_query()
async def answer(client: 'Client', callback_query: 'CallbackQuery'):
    handler = Handler(app, callback_query)
    try:
        app.callback_data.data = callback_query.data
        app.chat_id = callback_query.message.chat.id
        app.message_id = callback_query.message.id
    except Forbidden:
        await app.send_message(app.chat_id, app.exception.FORBIDDEN_MESSAGE)

    await handler.callback_data.post_choice()
    # if app.callback_data.data == app.command.POST:
    #     await app.event_handler.executor_event(app.command.DELETE_AND_SEND_MESSAGE, chat_id=app.chat_id,
    #                                            message_id=app.message_id, command=app.command.POST_MESSAGE,
    #                                            keyboard=app.keyboard.CRUD)
    #     app.cache.append(app.callback_data.data)

    await handler.callback_data.category_choice()
    # elif app.callback_data.data == app.command.CATEGORY:
    #     await app.event_handler.executor_event(app.command.DELETE_AND_SEND_MESSAGE, chat_id=app.chat_id,
    #                                            message_id=app.message_id, command=app.command.CATEGORY_MESSAGE,
    #                                            keyboard=app.keyboard.CRUD)
    #     app.cache.append(app.callback_data.data)

    if app.callback_data.data == app.command.CREATE and app.cache.last_element == app.command.POST:

        categories = app.query_to_api.get_all_category()
        count = app.query_to_api.get_category_count()
        if len(categories) == 0:
            await app.send_message(callback_query.message.chat.id, app.command.EMPTY_CATEGORY_MESSAGE)
        else:
            keyboard = app.keyboard.create_keyboard_count_category(categories, count)
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

    elif app.callback_data.data == app.command.SAVE and app.cache.last_element == app.command.add_photo:
        post_id = app.query_to_api.add_post(app.post)
        app.image.post_id = post_id
        app.query_to_api.add_image(app.image)
        await app.event_handler.executor_event(app.command.DELETE_AND_SEND_MESSAGE, chat_id=app.chat_id,
                                               message_id=app.message_id,
                                               command=app.command.CREATE_POST_MESSAGE)
        app.cache.append(app.command.create_post_completed)
        await app.send_message(app.chat_id, app.command.START_MESSAGE,
                               reply_markup=app.keyboard.START)

    await handler.callback_data.save_category()
    # elif app.callback_data.data == app.command.SAVE and app.cache.last_element == app.command.create_category:
    #     response_status_code = app.query_to_api.add_category(app.category)
    #     if response_status_code == 201:
    #         await app.event_handler.executor_event(app.command.DELETE_AND_SEND_MESSAGE, chat_id=app.chat_id,
    #                                                message_id=app.message_id,
    #                                                command=app.command.CREATE_CATEGORY_MESSAGE)
    #     else:
    #         pass
    #     app.cache.append(app.command.create_category_completed)
    #     await app.send_message(app.chat_id, app.command.START_MESSAGE,
    #                            reply_markup=app.keyboard.START)

    await handler.callback_data.create_category()
    # elif app.callback_data.data == app.command.CREATE and app.cache.last_element == app.command.CATEGORY:
    #     await app.event_handler.executor_event(app.command.DELETE_AND_SEND_MESSAGE, chat_id=app.chat_id,
    #                                            message_id=app.message_id,
    #                                            command=app.command.CREATE_CATEGORY_TITLE_MESSAGE)
    #     app.cache.append(app.command.create_category)

    if app.callback_data.data == app.command.DELETE and app.cache.last_element == app.command.CATEGORY:
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
                                               command=f'?????????????? {category}?', keyboard=keyboard)
        app.cache.append(app.command.delete_category)

    elif app.cache.last_element == app.command.delete_category and app.callback_data.data == app.command.DELETE:
        category_id = app.query_to_api.category['id']
        app.query_to_api.delete_category(category_id)
        await app.send_message(app.chat_id, f'{app.query_to_api.category["title"]} ??????????????.')
        await app.send_message(app.chat_id, app.command.START_MESSAGE,
                               reply_markup=app.keyboard.START)
        app.cache.append(app.command.delete_category_completed)
