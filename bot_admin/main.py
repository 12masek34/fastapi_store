from _bot import bot

bot.event_handler.register_handler('send_message', bot.send_message)


bot.run()
