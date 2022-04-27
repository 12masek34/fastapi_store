import typing

from application import app

if typing.TYPE_CHECKING:
    from application import Client


@app.on_message()
async def handler(client: 'Client', message):
    app.text_message = message.text
    app.chat_id = message.chat.id
    if app.text_message in app.START:
        await app.send_start_message()
