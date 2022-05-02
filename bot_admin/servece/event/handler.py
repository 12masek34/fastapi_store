class EventHandler:
    event_handlers: dict[str, list[callable]] = {}

    def register_handler(self, event: str, function: callable) -> None:
        handlers = self.event_handlers.get(event)

        if handlers is None:
            self.event_handlers[event] = [function]
        else:
            handlers.append(function)

    def executor_event(self, event: str, *args, **kwargs):
        handlers = self.event_handlers.get(event)

        if handlers is None:
            raise ValueError(f'Unknown event {event}')
        for handler in handlers:
            return handler(*args, **kwargs)
