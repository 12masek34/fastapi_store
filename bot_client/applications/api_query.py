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
    POSTS = '/posts'

    @property
    def url_get_token(self) -> str:
        return self.URL + self.TOKEN

    @property
    def url_categories(self) -> str:
        return self.URL + self.CATEGORIES

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
        try:
            categories = requests.get(self.url_categories, headers=self.create_headers_token())
            return categories.json()
        except requests.exceptions.JSONDecodeError:
            pass

    def get_posts_filter_by_category_id(self, category_id: str) -> dict:
        try:
            url = self.url_posts + '/' + category_id
            posts = requests.get(url, headers=self.create_headers_token())
            return posts.json()
        except requests.exceptions.JSONDecodeError:
            pass
