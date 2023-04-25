from typing import List, Dict

from DB import Session
from DB.models import TestTable

from sqlalchemy.sql import functions as func
from sqlalchemy.orm import aliased
from sqlalchemy import String as pgString, and_ as pg_and


class TestCalculations:
    """
    Коллекция аналитических методов
    """

    @staticmethod
    def calculate_total() -> List[Dict[str, str]]:
        """
        Рассчтё тотала Qliq и Qoil сгруппированного по датам
        """
        with Session() as ses:
            view = ses.query(TestTable.q_type,
                             TestTable.date.cast(pgString).label("date"),
                             (func.sum(TestTable.data1) + func.sum(TestTable.data2)).label("total")). \
                group_by(TestTable.date,
                         TestTable.q_type). \
                order_by(TestTable.date).cte()

            view2 = aliased(view)
            view3 = aliased(view)

            data = ses.query(view.c.date,
                             func.coalesce(view2.c.total, 0).label('Qoil_total'),
                             func.coalesce(view3.c.total, 0).label('Qliq_total')). \
                join(view2, pg_and(view2.c.date == view.c.date, view2.c.q_type == 'Qoil'), isouter=True). \
                join(view3, pg_and(view3.c.date == view.c.date, view3.c.q_type == 'Qliq'), isouter=True)

        return [d._asdict() for d in data]
