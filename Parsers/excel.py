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
        try:
            self._dataFrame = read_excel(file, header=[0, 1, 2])
        except Exception as e:
            raise ParserError(f'Ошибка чтения файла: {e.__class__.__name__}: {str(e)}')

    def do_parsing(self):
        df2 = self._dataFrame.loc[:, (['fact', 'forecast'],)].stack([0, 1]).reset_index(names=['index', 'analytics', 'q_type'])
        df1 = self._dataFrame.loc[:, (['id', 'company'],)].droplevel([1, 2], axis=1).reset_index(names='index')
        normalized_table = df2.join(df1, on='index', rsuffix='_right', lsuffix='_left')
        normalized_table = normalized_table.loc[:, ~normalized_table.columns.isin(['index_right', 'index_left'])]
        [r[1].to_dict() for r in normalized_table.iterrows()]
        res = [r[1].to_dict() | {"date": self.__moc_date()} for r in normalized_table.iterrows()]

        self.__save_to_db(res)

    @staticmethod
    def __save_to_db(data):
        with Session() as ses:
            ses.add_all((TestTable(**d, ) for d in data))
            ses.commit()

    @staticmethod
    def __moc_date():
        return getData(datetime(year=2023, month=4, day=randint(1, 30)))
