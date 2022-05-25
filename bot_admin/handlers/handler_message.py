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
            self._app.user.username = self._message.from_user.username
            self._app.user.password = str(self._message.from_user.id)
            print(self._app.user.password)

            self._app.query_to_api.get_token(self._app.user)

            await self._app.send_message(self._message.chat.id, self._app.command.START_MESSAGE,
                                         reply_markup=self._app.keyboard.START)

    async def create_category(self) -> None:
        """
        Проверяет кеш, если последний элемент в кеше == create_category, предлагает сохранить заголовок категории.
        """
        if self._app.cache.last_element == self._app.command.create_category:
            self._app.category.title = self._app.to_capitalize(self._app.text_message)
            preview_category = self._app.create_preview_category()
            await self._app.send_message(self._app.chat_id, preview_category,
                                         reply_markup=self._app.keyboard.SAVE_CANCEL)
            self._app.cache.append(self._app.command.add_title_category)
            self._app.cache.append(self._app.command.create_category)


