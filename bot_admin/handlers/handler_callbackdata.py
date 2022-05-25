from handlers.ABCHandler import MyHandlerCallbackData


class HandlerCallbackData(MyHandlerCallbackData):
    """
    Обработчик callback data.
    """

    async def category(self) -> None:
        """
        Обрабатывает  нажатие кнопки "категории"  callbackdata == category.
        """
        if self._app.callback_data.data == self._app.command.CATEGORY:
            await self._app.event_handler.executor_event(self._app.command.DELETE_AND_SEND_MESSAGE,
                                                         chat_id=self._app.chat_id,
                                                         message_id=self._app.message_id,
                                                         command=self._app.command.CATEGORY_MESSAGE,
                                                         keyboard=self._app.keyboard.CRUD)
            self._app.cache.append(self._app.callback_data.data)

    async def create_category(self):
        """
        Обрабатывает нажатие кнопки "создать" если в кеше последний элемент == category.
        """

        if (self._app.callback_data.data == self._app.command.CREATE and
                self._app.cache.last_element == self._app.command.CATEGORY):
            await self._app.event_handler.executor_event(self._app.command.DELETE_AND_SEND_MESSAGE,
                                                         chat_id=self._app.chat_id,
                                                         message_id=self._app.message_id,
                                                         command=self._app.command.CREATE_CATEGORY_TITLE_MESSAGE)
            self._app.cache.append(self._app.command.create_category)

    async def save_category(self) -> None:
        """
        Сохраняет категорию.
        """
        if (self._app.callback_data.data == self._app.command.SAVE and
                self._app.cache.last_element == self._app.command.create_category):

            response_status_code = self._app.query_to_api.add_category(self._app.category)
            if response_status_code == 201:
                await self._app.event_handler.executor_event(self._app.command.DELETE_AND_SEND_MESSAGE,
                                                             chat_id=self._app.chat_id,
                                                             message_id=self._app.message_id,
                                                             command=self._app.command.CREATE_CATEGORY_MESSAGE)
            else:
                pass
            self._app.cache.append(self._app.command.create_category_completed)
            await self._app.send_message(self._app.chat_id, self._app.command.START_MESSAGE,
                                         reply_markup=self._app.keyboard.START)
