import os
import requests
from dotenv import load_dotenv

load_dotenv()


class Api:

    def __init__(self):
        self.token: dict | None = None

    URL = os.getenv('URL')
    TOKEN = '/token'

    @property
    def url_get_token(self) -> str:
        return self.URL + self.TOKEN

    def get_token(self, user):
        user = user.dict()
        token = requests.post(self.url_get_token, data=user)
        self.token = token.json()
