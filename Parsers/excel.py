from datetime import datetime
from random import randint

from pandas import read_excel

from DB import Session
from DB.models import TestTable, getData


class ParserError(Exception):
    default_detail = 'Ошибка парсера'
    detail = ''

    def __init__(self, detail=None):
        if detail is None:
            detail = self.default_detail

        self.detail = detail

    def __str__(self):
        return str(self.detail)


class Parser:
    def __init__(self, file: str):
        """
        Инициализация объекта

        :param file: путь к файлу для парсинга
        """
        try:
            self._dataFrame = read_excel(file, header=[0, 1, 2])
        except Exception as e:
            raise ParserError(f'Ошибка чтения файла: {e.__class__.__name__}: {str(e)}')

    def do_parsing(self):
        data1 = []
        for _, v in self._dataFrame.loc[:, (['id', 'company'],)].droplevel([1, 2], axis=1).iterrows():
            data1.append(v.to_dict())

        data2 = []
        for k, v in self._dataFrame.loc[:, (['fact', 'forecast'],)].stack([0, 1]).iterrows():
            data2.append(dict(zip(('analytics', 'q_type'), k[1:])) | v.to_dict())

        res = [item[0] | item[1] | item[2] for item in zip(data1, data2, self.__moc_data(len(data1)))]

        self.__save_to_db(res)

    @staticmethod
    def __save_to_db(data):
        with Session() as ses:
            ses.add_all((TestTable(**d, ) for d in data))
            ses.commit()

    @staticmethod
    def __moc_data(length):
        return [{"date": getData(datetime(year=2023, month=4, day=randint(1, 31)))} for _ in range(length)]
