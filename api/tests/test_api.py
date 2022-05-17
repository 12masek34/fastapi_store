import os

from dotenv import load_dotenv

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

load_dotenv()


class TestAPI(BaseCase):

    def setup(self):
        self.data = {'username': os.getenv('ADMIN_NAME'),
                     'password': os.getenv('ADMIN_PASS')}
        self.auth_response = self.get_auth_token('token', self.data)
        self.token = self.create_headers_token(self.auth_response.json())

    def test_get_token(self):
        response = self.get_auth_token('token', self.data)
        Assertions.assert_value_by_name(response,
                                        'token_type',
                                        'bearer',
                                        'Wrong token type')
        response_dict = response.json()
        Assertions.assert_status_code(response, 200)
        assert 'access_token' in response_dict, 'There is no field access_token in the response'

    def test_categories(self):
        response = MyRequests.get('categories', headers=self.token)
        response_list = response.json()
        Assertions.assert_status_code(response, 200)
        assert isinstance(response_list, list), 'Response must be list type'
        assert 'id' in response_list[0], f'Response must be field id'
        assert 'title' in response_list[0], f'Response must be field title'
        assert 'created_at' in response_list[0], f'Response must be field created_at'
        assert isinstance(response_list[0]['id'], int), f'Category id field must be int type'
        assert isinstance(response_list[0]['title'], str), f'Delete category response title field must be str type'
        assert isinstance(response_list[0]['created_at'], str), f'Category created_at field must be str type'

    def test_negative_categories(self):
        response = MyRequests.get('categories')
        Assertions.assert_status_code(response, 401)
        Assertions.assert_value_by_name(response,
                                        'detail',
                                        'Not authenticated',
                                        'User must be not authorization')

    def test_categories_count(self):
        response = MyRequests.get('categories/count', headers=self.token)
        response_list = response.json()
        Assertions.assert_status_code(response, 200)
        assert isinstance(response_list, list), f'Response must be list type, or not {type(response)}'

    def test_negative_categories_count(self):
        response = MyRequests.get('categories/count')
        Assertions.assert_status_code(response, 401)
        Assertions.assert_value_by_name(response,
                                        'detail',
                                        'Not authenticated',
                                        'User must be not authorization')
