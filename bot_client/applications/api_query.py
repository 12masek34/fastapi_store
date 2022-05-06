import json
import os
import requests
from pyrogram.errors import Forbidden
from dotenv import load_dotenv

load_dotenv()


class Api:

    def __init__(self):
        self.token: dict | None = None

    URL = os.getenv('URL')

    TOKEN = '/token'
    CATEGORIES = '/categories'
    CATEGORY = '/category'
    POSTS = '/posts'
    COUNT = '/count'

    @property
    def url_get_token(self) -> str:
        return self.URL + self.TOKEN

    @property
    def url_categories(self) -> str:
        return self.URL + self.CATEGORIES

    @property
    def url_categories_count(self) -> str:
        return self.URL + self.CATEGORIES + self.COUNT

    @property
    def url_posts(self) -> str:
        return self.URL + self.POSTS

    def get_token(self, user):
        user = user.dict()
        token = requests.post(self.url_get_token, data=user)
        self.token = token.json()

    def create_headers_token(self):
        try:
            bearer = f'Bearer {self.token["access_token"]}'
            headers = {'Authorization': bearer}
            return headers
        except TypeError:
            raise Forbidden

    def get_all_category(self) -> dict:

        categories = requests.get(self.url_categories, headers=self.create_headers_token())
        return categories.json()

    def get_category_count(self) -> dict:

        categories = requests.get(self.url_categories_count, headers=self.create_headers_token())
        return categories.json()

    def get_posts_filter_by_category_id(self, category_id: str) -> dict:

        url = self.url_posts + self.CATEGORY + '/' + category_id
        posts = requests.get(url, headers=self.create_headers_token())
        return posts.json()

    def get_all_posts(self):
        url = self.url_posts
        posts = requests.get(url, headers=self.create_headers_token())
        return posts.json()
