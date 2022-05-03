import re


class Command:
    START = ['/start', 'start']

    START_MESSAGE = 'Это интернет магазин Васи Пупкина.'
    CHOICE_CATEGORY_MESSAGE = 'Выберите категорию.'

    ALL = 'all'
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