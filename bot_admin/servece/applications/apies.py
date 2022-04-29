import json

import requests
from servece.schemas.schema import PostSchema


class Api:
    URL = 'http://0.0.0.0:8000'
    CATEGORIES = '/categories'
    ADD_POST = '/add/post'

    def __init__(self):
        self.categories = None

    @property
    def url_category(self) -> str:
        return self.URL + self.CATEGORIES

    @property
    def url_add_post(self) -> str:
        return self.URL + self.ADD_POST

    def get_all_category(self) -> None:
        categories = requests.get(self.url_category)
        self.categories = categories.json()

    def add_post(self, data: PostSchema):
        data = data.dict()
        data = json.dumps(data)
        requests.post(self.url_add_post, data=data)
