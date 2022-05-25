import json
import os
import requests
from schemas.schema import PostSchema, CategorySchema, ImageSchema
from pyrogram.errors import Forbidden
from dotenv import load_dotenv

load_dotenv()


class Api:
    URL = os.getenv('URL')
    CATEGORIES = '/categories'
    CATEGORY = '/category'
    ADD = '/add'
    POST = '/post'
    IMAGES = '/images'
    TOKEN = '/token'
    COUNT = '/count'

    def __init__(self):
        self.categories = None
        self.category = None
        self.token: dict | None = None

    @property
    def url_categories(self) -> str:
        return self.URL + self.CATEGORIES

    @property
    def url_add_category(self) -> str:
        return self.URL + self.CATEGORY + self.ADD

    @property
    def url_add_post(self) -> str:
        return self.URL + self.POST + self.ADD

    @property
    def url_get_token(self) -> str:
        return self.URL + self.TOKEN

    @property
    def url_categories_count(self) -> str:
        return self.URL + self.CATEGORIES + self.COUNT

    def get_token(self, user):
        user = user.dict()
        token = requests.post(self.url_get_token, data=user)
        self.token = token.json()

    def create_headers_token(self):
        try:
            bearer = f'Bearer {self.token["access_token"]}'
            headers = {'Authorization': bearer}
            return headers
        except KeyError:
            raise Forbidden

    def get_all_category(self) -> dict | None:
        categories = requests.get(self.url_categories, headers=self.create_headers_token())
        self.categories = categories.json()
        return categories.json()

    def get_category_count(self) -> dict | None:
        categories = requests.get(self.url_categories_count, headers=self.create_headers_token())
        return categories.json()

    def add_post(self, data: PostSchema):
        data = data.dict()
        data = json.dumps(data)
        response = requests.post(self.url_add_post, data=data, headers=self.create_headers_token())
        return response.json()

    def add_category(self, data: CategorySchema):
        data = data.dict()
        data = json.dumps(data)
        response = requests.post(self.url_add_category, data=data, headers=self.create_headers_token())
        return response.status_code

    def delete_category(self, category_id: int) -> str:
        category_id = str(category_id)
        url = self.URL + self.CATEGORIES + '/' + category_id
        response = requests.delete(url, headers=self.create_headers_token())
        return response.json()['title']

    def get_category(self, category_id: int) -> str:
        category_id = str(category_id)
        url = self.URL + self.CATEGORIES + '/' + category_id
        response = requests.get(url, headers=self.create_headers_token())
        self.category = response.json()
        return response.json()['title']

    def add_image(self, data: ImageSchema):
        data = data.dict()
        data = json.dumps(data)
        url = self.URL + self.IMAGES + self.ADD
        requests.post(url, data=data, headers=self.create_headers_token())
