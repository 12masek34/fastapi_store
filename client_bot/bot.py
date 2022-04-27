from pyrogram import Client

app = Client('my_bot',
             api_id=13542258,
             api_hash='a5fbecad0687312eb8fea06d7a88b399',
             bot_token='5279728090:AAF_0JTxKynunlPiB1KPidXsxloFoIrcvrA'
             )


@app.on_message()
async def handler(client: Client, message):
    print(message)
