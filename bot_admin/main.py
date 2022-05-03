from bot import app

app.event_handler.register_handler('delete_and_send_message', app.delete_messages)
app.event_handler.register_handler('delete_and_send_message', app.send_message)

app.run()
