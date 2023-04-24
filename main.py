from Parsers import ExcelParser
from DB import init_db


def main():
    init_db()
    file = r'.\temp\test_file.xlsx'
    parser = ExcelParser(file)
    parser.do_parsing()


if __name__ == '__main__':
    main()
