import requests


class Api:
    def __init__(self):
        self.categories = None

    def get_all_category(self):
        categories = requests.get('http://0.0.0.0:8000/categories')
        self.categories = categories.json()
