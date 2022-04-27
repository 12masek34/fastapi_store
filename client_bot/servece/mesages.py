class Message:
    START = ['/start', 'start']

    def __init__(self):
        self._text: str | None = None
        self._chat_id: int | None = None

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
