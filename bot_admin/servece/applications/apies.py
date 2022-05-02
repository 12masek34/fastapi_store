import json

import requests
from servece.schemas.schema import PostSchema, CategorySchema
from pyrogram.errors import Forbidden


class Api:
    URL = 'http://0.0.0.0:8000'
    CATEGORIES = '/categories'
    CATEGORY = '/category'
    ADD = '/add'
    POST = '/post'
    TOKEN = '/token'
    USERS_ME = '/users/me'

    def __init__(self):
        self.categories = None
        self.token: dict | None = None

    @property
    def url_category(self) -> str:
        return self.URL + self.CATEGORIES

    @property
    def url_add_category(self) -> str:
        return self.URL + self.ADD + self.CATEGORY

    @property
    def url_add_post(self) -> str:
        return self.URL + self.ADD + self.POST

    @property
    def url_get_token(self) -> str:
        return self.URL + self.TOKEN

    @property
    def url_ger_users_me(self) -> str:
        return self.URL + self.USERS_ME

    def get_all_category(self) -> None:
        try:
            categories = requests.get(self.url_category, headers=self.create_headers_token())
            self.categories = categories.json()
        except requests.exceptions.JSONDecodeError:
            pass

    def add_post(self, data: PostSchema):
        data = data.dict()
        data = json.dumps(data)
        response = requests.post(self.url_add_post, data=data, headers=self.create_headers_token())
        return response.status_code

    def add_category(self, data: CategorySchema):
        data = data.dict()
        data = json.dumps(data)
        response = requests.post(self.url_add_category, data=data, headers=self.create_headers_token())
        return response.status_code


    def get_token(self, user):
        user = user.dict()
        token = requests.post(self.url_get_token, data=user)
        self.token = token.json()

    def get_users_me(self):
        me = requests.get(self.url_ger_users_me, headers=self.create_headers_token())

    def create_headers_token(self):
        try:
            bearer = f'Bearer {self.token["access_token"]}'
            headers = {'Authorization': bearer}
            return headers
        except TypeError:
            raise Forbidden
