# -*- coding: utf-8 -*-

class DatabaseException(BaseException):
    pass


class CategoryAlreadyExistsError(DatabaseException):
    def __init__(self):
        super().__init__('Категория с таким именем уже существует')
