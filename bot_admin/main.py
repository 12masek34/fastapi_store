from _bot import bot

bot.event_handler.register_handler('delete_and_send_message', bot.delete_messages)
bot.event_handler.register_handler('delete_and_send_message', bot.send_message)

bot.run()
