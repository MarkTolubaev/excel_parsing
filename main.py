from Parsers import ExcelParser
from DB import init_db, Session
from DB.models import TestTable


def main():
    init_db()

    with Session() as ses:
        ses.query(TestTable).delete()
        ses.commit()

    file = r'.\temp\test_file.xlsx'
    parser = ExcelParser(file)
    parser.do_parsing()


if __name__ == '__main__':
    main()
