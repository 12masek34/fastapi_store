import re


class Command:
    START = ['/start', 'start']

    START_MESSAGE = 'Это интернет магазин Васи Пупкина.'
    CHOICE_CATEGORY_MESSAGE = 'Выберите категорию.'

    SELECT = 'select'
    ALL = 'all'
    NEXT = 'next'

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

        for post in posts:
            message = (f'{post["title"]}\n'
                       f'{post["text"]}\n'
                       f'{post["created_at"]}'
                       f'\n')
            img = post['img'][0]['img']

            resp = {'message': message,
                    'image': img}

            yield resp

    @staticmethod
    def create_image_posts(posts: list[dict]) -> str:

        for post in posts:
            img = post['img'][0]['img']
            print(img)
            yield img
