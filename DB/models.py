import sqlalchemy as db

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def getData(dt: datetime = None) -> str:
    """
    дата в формате Postgres TIMESTAMP

    :param dt: дата для преобразования в строку
    """

    if not dt:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


class TestTable(Base):
    """
    Модель тестовой таблицы
    """
    __tablename__ = 'test_table'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(8), primary_key=True)
    analytics = db.Column(db.String(8), primary_key=True)
    q_type = db.Column(db.String(4), primary_key=True)
    data1 = db.Column(db.Integer)
    data2 = db.Column(db.Integer)
    date = db.Column(db.TIMESTAMP)
