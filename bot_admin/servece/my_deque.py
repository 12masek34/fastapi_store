from collections import deque as CollectionDeque


class Deque(CollectionDeque):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_last_element(self):
        return self[-1]
