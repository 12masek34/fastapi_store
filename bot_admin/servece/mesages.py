class Message:

    def __init__(self):
        self._text: str | None = None
        self._chat_id: int | None = None
        self._message_id: int | None = None
        self._callback_data: str | None = None

    @property
    def text_message(self) -> str:
        return self._text

    @text_message.setter
    def text_message(self, text: str):
        text = text.lower()
        self._text = text

    @property
    def chat_id(self) -> int:
        return self._chat_id

    @chat_id.setter
    def chat_id(self, chat_id: int) -> None:
        self._chat_id = chat_id

    @property
    def message_id(self) -> int:
        return self._message_id

    @message_id.setter
    def message_id(self, message_id) -> None:
        self._message_id = message_id

    @property
    def callback_data(self) -> str:
        return self._callback_data

    @callback_data.setter
    def callback_data(self, data) -> None:
        self._callback_data = data
