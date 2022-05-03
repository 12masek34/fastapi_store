import re


class CallbackData:
    def __init__(self):
        self.data: str | None = None
        self.category_id: int | None = None

    def parse_category_id(self) -> None:
        category_id = re.search(r'\d+', self.data).group()
        self.category_id = int(category_id)


class Message:

    def __init__(self):
        self._text: str | None = None
        self._chat_id: int | None = None
        self._message_id: int | None = None
        self.preview_post: str | None = None
        self.callback_data = CallbackData()

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

    @staticmethod
    def to_capitalize(text: str) -> str:
        return text.capitalize()
