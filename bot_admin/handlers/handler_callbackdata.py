from handlers.ABCHandler import MyHandlerCallbackData


class HandlerCallbackData(MyHandlerCallbackData):
    """
    Обработчик callbackdata.
    """

    async def category(self):
        """
        Обрабатывает  callbackdata == category.
        """
        if self._app.callback_data.data == self._app.command.CATEGORY:
            await self._app.event_handler.executor_event(self._app.command.DELETE_AND_SEND_MESSAGE,
                                                         chat_id=self._app.chat_id,
                                                         message_id=self._app.message_id,
                                                         command=self._app.command.CATEGORY_MESSAGE,
                                                         keyboard=self._app.keyboard.CRUD)
            self._app.cache.append(self._app.callback_data.data)
