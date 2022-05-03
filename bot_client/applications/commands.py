class Command:
    START = ['/start', 'start']

    START_MESSAGE = 'Это интернет магазин Васи Пупкина.'

    ALL = 'all'
    POST = 'post'
    CATEGORY = 'category'

    @property
    def all_post(self) -> str:
        return self.ALL + '_' + self.POST
