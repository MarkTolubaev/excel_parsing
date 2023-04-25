from datetime import datetime
from random import randint
from abc import abstractmethod, ABC
from types import MappingProxyType
from typing import Tuple, Dict

from pandas import read_excel

from DB import getData


class ParserError(Exception):
    default_detail = 'Ошибка парсера'
    detail = ''

    def __init__(self, detail=None):
        if detail is None:
            detail = self.default_detail

        self.detail = detail

    def __str__(self):
        return str(self.detail)


class Parser(ABC):
    def __init__(self, file: str):
        try:
            self._dataFrame = read_excel(file, header=[0, 1, 2])
        except Exception as e:
            raise ParserError(f'Ошибка чтения файла: {e.__class__.__name__}: {str(e)}')

        self.__data = None

    @property
    def data(self) -> Tuple[MappingProxyType, ...]:
        """
        Геттер для данных, полученных в ходе разбора файла

        :return: кортеж неизменямых объектов
        """
        return tuple(MappingProxyType(d) for d in self.__data)

    def do_parsing(self) -> None:
        """
        Метод разбора excel файла заданного формата
        """

        df2 = self._dataFrame.\
            loc[:, (['fact', 'forecast'],)].\
            stack([0, 1]).\
            reset_index(names=['index', 'analytics', 'q_type'])

        df1 = self._dataFrame.\
            loc[:, (['id', 'company'],)].\
            droplevel([1, 2], axis=1).\
            reset_index(names='index')

        normalized_table = df2.join(df1, on='index', rsuffix='_right', lsuffix='_left')
        normalized_table = normalized_table.loc[:, ~normalized_table.columns.isin(['index_right', 'index_left'])]

        self.__data = [r[1].to_dict() | self._moc_date() for r in normalized_table.iterrows()]

    @abstractmethod
    def _moc_date(self) -> Dict[str, str]:
        pass


class TestParser(Parser):
    def _moc_date(self):
        """
        Генератция случайцных данных, подмешиваемых к разобранному файлу
        """
        return {"date": getData(datetime(year=2023, month=4, day=randint(1, 30)))}
