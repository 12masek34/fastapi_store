import typing
from applications.application import app

if typing.TYPE_CHECKING:
    from applications.application import Client


@app.on_message()
async def message_handler(client: 'Client', message):
    await app.parse_message_text(message)


@app.on_callback_query()
async def answer(client, callback_query):
    await app.parser_callback_data(callback_query)
