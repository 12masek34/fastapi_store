import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from models.database import Base, get_db
from main import app
from tests.test_api import TestAPI
from lib.assertions import Assertions

load_dotenv()

URL_TEST_DB = os.getenv('URL_TEST_DB')
engine = create_engine(URL_TEST_DB)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class TestSql(TestAPI):
    category_id = None

    def setup(self):
        super().setup()

    def test_create_category(self):
        response = client.post(
            '/category/add',
            json={'title': 'Test category'},
            headers=self.token
        )
        Assertions.assert_status_code(response, 201)
        response_dict = response.json()
        assert isinstance(response_dict, dict), f'Response must be dict type, or not {type(response_dict)}'
        assert 'id' in response_dict, f'Response must be field id'
        assert 'title' in response_dict, f'Response must be field title'
        Assertions.assert_value_by_name(response,
                                        'title',
                                        'Test category',
                                        'Wrong title')
        assert 'created_at' in response_dict, f'Response must be field created_at'
        assert isinstance(response_dict['id'], int), f'Category id field must be int type'
        assert isinstance(response_dict['title'], str), f'Delete category response title field must be str type'
        assert isinstance(response_dict['created_at'], str), f'Category created_at field must be str type'
        return response_dict

    def test_create_category_negative(self):
        response = client.post(
            '/category/add',
            json={'title': 'Test category'}
        )

        Assertions.assert_status_code(response, 401)
        Assertions.assert_value_by_name(response,
                                        'detail',
                                        'Not authenticated',
                                        'User must be not authorization')

    def test_delete_category(self):
        category = self.test_create_category()
        response = client.delete(
            f'/categories/{category["id"]}',
            json={'title': 'Test category'},
            headers=self.token
        )
        Assertions.assert_status_code(response, 200)
        response_dict = response.json()
        assert isinstance(response_dict, dict), f'Response must be dict type, or not {type(response_dict)}'
        assert 'id' in response_dict, f'Response must be field id'
        assert 'title' in response_dict, f'Response must be field title'
        assert 'created_at' in response_dict, f'Response must be field created_at'
        assert isinstance(response_dict['id'], int), f'Category id field must be int type'
        assert isinstance(response_dict['title'], str), f'Delete category response title field must be str type'
        assert isinstance(response_dict['created_at'], str), f'Category created_at field must be str type'
