from handlers.ABCHandler import MyHandlerText


class HandlerMessageText(MyHandlerText):
    """
    Класс обработки текста сообщений.
    """

    async def start(self) -> None:
        """
        Обработка стартового сообщения. Получает токен и отправляет стартовое сообщение.
        """
        if self._message.text in self._app.command.START:
            self._app.query_to_api.get_token(self._app.user)

            await self._app.send_message(self._message.chat.id, self._app.command.START_MESSAGE,
                                         reply_markup=self._app.keyboard.START)
