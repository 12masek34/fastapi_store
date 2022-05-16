import os

from dotenv import load_dotenv
import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

load_dotenv()

@allure.epic('API cases')
class TestAPI(BaseCase):

    def setup(self):
        self.data = {'username': os.getenv('ADMIN_NAME'),
                     'password': os.getenv('ADMIN_PASS')}
        self.auth_response = self.get_auth_token('token', self.data)
        self.token = self.create_headers_token(self.auth_response.json())

    @allure.description('This test successfully authorize by username and password.')
    def test_get_token(self):
        response = self.get_auth_token('token', self.data)
        Assertions.assert_value_by_name(response,
                                        'token_type',
                                        'bearer',
                                        'Wrong token type')
        response_dict = response.json()
        Assertions.assert_status_code(response, 200)
        assert 'access_token' in response_dict, 'There is no field access_token in the response'

    @allure.description('This positive test check categories route.')
    def test_categories(self):
        response = MyRequests.get('categories', headers=self.token)
        response_list = response.json()
        Assertions.assert_status_code(response, 200)
        assert isinstance(response_list, list), 'Response must be list type'

    @allure.description('This negative test check categories route.')
    def test_negative_categories(self):
        response = MyRequests.get('categories')
        Assertions.assert_status_code(response, 401)
        Assertions.assert_value_by_name(response,
                                        'detail',
                                        'Not authenticated',
                                        'User must be not authorization')

    @allure.description('This positive test check categories/count route.')
    def test_categories_count(self):
        response = MyRequests.get('categories/count', headers=self.token)
        response_list = response.json()
        Assertions.assert_status_code(response, 200)
        assert isinstance(response_list, list), f'Response must be list type, or not {type(response)}'

    @allure.description('This negative test check categories/count route.')
    def test_negative_categories_count(self):
        response = MyRequests.get('categories/count')
        Assertions.assert_status_code(response, 401)
        Assertions.assert_value_by_name(response,
                                        'detail',
                                        'Not authenticated',
                                        'User must be not authorization')




