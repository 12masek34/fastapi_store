import datetime
import re
from applications.datacls import Post
from applications.cache import Deque


class Command:
    START = ['/start', 'start']

    START_MESSAGE = 'Это интернет магазин Васи Пупкина.'
    CHOICE_CATEGORY_MESSAGE = 'Выберите категорию.'

    SELECT = 'select'
    ALL = 'all'
    NEXT = 'next'
    BACK = 'back'

    POST = 'post'
    CATEGORY = 'category'

    SELECTED_CATEGORY_PATTERN = 'category_'

    @property
    def all_post(self) -> str:
        return self.ALL + '_' + self.POST

    @staticmethod
    def get_category_id(data: str) -> str:
        _category_pattern = r'category_\d*'
        match = re.fullmatch(_category_pattern, data)
        if match:
            category_id = re.search(r'\d+', data)
            return category_id.group()

    @staticmethod
    def create_message_posts(posts: list[dict]) -> [str, str]:
        queue = Deque()
        for post in posts:
            date = datetime.datetime.fromisoformat(post["created_at"])
            date = date.strftime("%Y-%d-%m %H:%M")

            text = (f'{post["title"]}\n\n'
                    f'{post["text"]}\n\n'
                    f'{date}')
            img = post['img'][0]['img']

            resp = Post(text=text, image=img)

            queue.append(resp)

        return queue

    @staticmethod
    def create_image_posts(posts: list[dict]) -> str:

        for post in posts:
            img = post['img'][0]['img']
            print(img)
            yield img
