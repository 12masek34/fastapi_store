import json

import requests
from servece.schemas.schema import PostSchema


class Api:
    URL = 'http://0.0.0.0:8000'
    CATEGORIES = '/categories'
    ADD_POST = '/add/post'
    TOKEN = '/token'
    USERS_ME = '/users/me'

    def __init__(self):
        self.categories = None
        self.token: dict | None = None

    @property
    def url_category(self) -> str:
        return self.URL + self.CATEGORIES

    @property
    def url_add_post(self) -> str:
        return self.URL + self.ADD_POST

    @property
    def url_get_token(self) -> str:
        return self.URL + self.TOKEN

    @property
    def url_ger_users_me(self) -> str:
        return self.URL + self.USERS_ME

    def get_all_category(self) -> None:
        categories = requests.get(self.url_category)
        self.categories = categories.json()

    def add_post(self, data: PostSchema) -> None:
        data = data.dict()
        data = json.dumps(data)
        r = requests.post(self.url_add_post, data=data, headers=self.create_headers_token())
        print(r)

    def get_token(self, user):
        user = user.dict()
        token = requests.post(self.url_get_token, data=user)
        self.token = token.json()

    def get_users_me(self):
        me = requests.get(self.url_ger_users_me, headers=self.create_headers_token())

    def create_headers_token(self):
        bearer = f'Bearer {self.token["access_token"]}'
        headers = {'Authorization': bearer}
        return headers
