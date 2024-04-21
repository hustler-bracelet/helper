# -*- coding: utf-8 -*-

class DatabaseException(BaseException):
    pass


class CategoryAlreadyExists(DatabaseException):
    def __init__(self):
        super().__init__('Категория с таким именем уже существует')
