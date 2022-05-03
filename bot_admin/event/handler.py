class EventHandler:
    event_handlers: dict[str, list[callable]] = {}

    def register_handler(self, event: str, function: callable) -> None:

        handlers = self.event_handlers.get(event)
        if handlers is None:
            self.event_handlers[event] = [function]
        else:
            handlers.append(function)

    async def executor_event(self, event: str, chat_id: int, message_id: int, command: str,
                             keyboard: callable = None) -> None:

        handlers = self.event_handlers.get(event)
        if handlers is None:
            raise ValueError(f'Unknown event {event}')
        for handler in handlers:
            if handler.__name__ == 'delete_messages':
                await handler(chat_id=chat_id, message_ids=message_id)
            elif handler.__name__ == 'send_message':
                await handler(chat_id=chat_id, text=command, reply_markup=keyboard)
