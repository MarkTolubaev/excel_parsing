from sqlalchemy import create_engine
from contextlib import contextmanager

from urllib.parse import quote
from sqlalchemy.orm import sessionmaker

from Config import configs


def makeEngine():
    settings = configs.get('postgres')

    password = quote(settings.get('password'))
    user = settings.get('username')
    host = settings.get('host')
    port = settings.get('port')
    db = settings.get('db')

    hostname = f'{host}:{port}' if port else host

    engineString = f'postgresql://{user}:{password}@{hostname}/{db}'

    return create_engine(engineString)


def makeSession():
    return sessionmaker(bind=makeEngine())()


@contextmanager
def Session():
    """
    Декоратор, предоставляющий объект сессии для работы с базой данных
    """
    ses = makeSession()
    try:
        yield ses
    finally:
        ses.close()
