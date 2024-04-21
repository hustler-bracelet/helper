# -*- coding: utf-8 -*-

from sqlmodel import create_engine, SQLModel


DATABASE_ENGINE = create_engine('sqlite:///hustler_bracelet.sqlite')


def create_all_tables() -> None:
    return SQLModel.metadata.create_all(DATABASE_ENGINE)
