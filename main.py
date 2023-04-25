from json import dumps

from Utils import ExcelParser, TestCalculations
from DB import init_db, Session
from DB.models import TestTable


def main():
    print("Init db")
    init_db()

    file = r'.\temp\test_file.xlsx'  # replace on your file location
    parser = ExcelParser(file)
    print("Parsing data")
    parser.do_parsing()

    with Session() as ses:
        print("Clear table")
        ses.query(TestTable).delete()
        ses.flush()
        print("Inserting data to db")
        ses.add_all((TestTable(**d, ) for d in parser.data))
        ses.commit()

    calculations = TestCalculations()
    print("Calculate analytics:")
    totals = calculations.calculate_total()
    print(dumps(totals, indent=2))


if __name__ == '__main__':
    main()
