from openpyxl import *
import psycopg2


def db_conn():
    conn = psycopg2.connect(dbname='project-cs', user='cs-main',
                            password='eid4Uepo', host='cs-vm-postgre.cs.vsu.ru')
    cursor = conn.cursor()

    return cursor, conn


def xlsx_connect(path):
    wb = load_workbook(path)

    return wb


def parser_init(file_name, sheet_number):
    first_str_number = read_first_str_number()

    cur, conn = db_conn()
    ws = xlsx_connect(file_name).worksheets[sheet_number - 1]

    columns = list(ws.columns)
    rows = list(ws.rows)

    return columns, rows[first_str_number:], cur, conn


def read_sheet_number():
    return int(input("Номер листа: "))-1


def read_first_str_number():
    return int(input("Номер строки для начала парсинга: "))-1



