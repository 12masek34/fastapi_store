import os

import requests
from dotenv import load_dotenv

from lib.base_case import BaseCase
from lib.assertions import Assertions

load_dotenv()


class TestUserAuth(BaseCase):

    def setup(self):
        self.url = 'http://127.0.0.1:8000/'
        self.data = {'username': os.getenv('ADMIN_NAME'),
                     'password': os.getenv('ADMIN_PASS')}
        self.auth_response = self.get_auth_token(self.url_token, self.data)
        self.token = self.create_headers_token(self.auth_response.json())

    @property
    def url_token(self):
        return self.url + 'token'

    @property
    def url_categories_count(self):
        return self.url + 'categories/count'

    @property
    def url_categories(self):
        return self.url + 'categories'

    def test_get_token(self):
        response = self.get_auth_token(self.url_token, self.data)
        Assertions.assert_value_by_name(response,
                                        'token_type',
                                        'bearer',
                                        'Wrong token type')
        response_dict = response.json()
        Assertions.assert_status_code(response, 200)
        assert 'access_token' in response_dict, 'There is no field access_token in the response'

    def test_categories(self):
        response = requests.get(self.url_categories, headers=self.token)
        response_list = response.json()
        Assertions.assert_status_code(response, 200)
        assert isinstance(response_list, list), 'Response must be list type'

    def test_negative_categories(self):
        response = requests.get(self.url_categories)
        Assertions.assert_status_code(response, 401)
        Assertions.assert_value_by_name(response,
                                        'detail',
                                        'Not authenticated',
                                        'User must be not authorization')

    def test_categories_count(self):
        response = requests.get(self.url_categories_count, headers=self.token)
        response_list = response.json()
        Assertions.assert_status_code(response, 200)
        assert isinstance(response_list, list), f'Response must be list type, or not {type(response)}'

    def test_negative_categories_count(self):
        response = requests.get(self.url_categories_count)
        Assertions.assert_status_code(response, 401)
        Assertions.assert_value_by_name(response,
                                        'detail',
                                        'Not authenticated',
                                        'User must be not authorization')




