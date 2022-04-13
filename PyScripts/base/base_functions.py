from openpyxl import *
import psycopg2
from os import system


def db_conn(db_name='project-cs', table_name='other'):
    print(f"Подключение к базе данных '{db_name}'. Таблица - '{table_name}'")
    conn = psycopg2.connect(dbname=db_name, user='cs-main',
                            password='eid4Uepo', host='cs-vm-postgre.cs.vsu.ru')
    cursor = conn.cursor()

    return cursor, conn


def clear_console():
    system('clear')


def xlsx_connect(path):
    wb = load_workbook(path)

    return wb


def parser_init(file_name, sheet_number, first_str_number):
    cur, conn = db_conn(table_name="All Tables")
    ws = xlsx_connect(file_name).worksheets[sheet_number - 1]

    columns = list(ws.columns)
    rows = list(ws.rows)

    return columns, rows[first_str_number-1:], cur, conn


def read_sheet_number():
    return int(input("Номер листа: "))-1


def read_first_str_number():
    return int(input("Номер строки для начала парсинга: "))-1



