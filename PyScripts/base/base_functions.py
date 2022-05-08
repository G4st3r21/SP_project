from openpyxl import *
import psycopg2
from os import system

from openpyxl.utils import range_boundaries


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


def parser_init(file_name, sheet_number, first_str_number, need_db_conn=True):
    cur, conn = db_conn(table_name="All Tables") if need_db_conn else (None, None)
    wb = xlsx_connect(file_name)
    ws = wb.worksheets[sheet_number - 1]
    unmerge_all_cells(ws)

    columns = list(ws.columns)
    rows = list(ws.rows)
    return (columns, rows[first_str_number - 1:], cur, conn) if need_db_conn else (columns, rows[first_str_number - 1:])


def read_sheet_number():
    return int(input("Номер листа: ")) - 1


def read_first_str_number():
    return int(input("Номер строки для начала парсинга: ")) - 1


def unmerge_all_cells(ws):
    try:
        while len(ws.merged_cells.ranges) > 0:
            min_col, min_row, max_col, max_row = range_boundaries(str(ws.merged_cells.ranges[0]))
            top_left_cell_value = ws.cell(row=min_row, column=min_col).value
            ws.unmerge_cells(str(ws.merged_cells.ranges[0]))
            for row in ws.iter_rows(min_col=min_col, min_row=min_row, max_col=max_col, max_row=max_row):
                for cell in row:
                    cell.value = top_left_cell_value
    except Exception:
        pass


def input_answer_and_replace(word, suggest):
    print('Верно ли предположение?(y/n/dr): ')
    yn = input().lower()
    if yn == 'y':
        return suggest
    elif yn == 'n':
        print('Введите верное слово: ')
        suggest = input()
        return suggest
    elif yn == 'dr':
        return False
    else:
        print('Неправильный ответ, попробуйте еще раз')
        return input_answer_and_replace(word, suggest)


def checking_for_typos(rows):
    from enchant import Dict
    import string
    from natasha import NamesExtractor, Doc
    dictionary = Dict('ru_RU')

    for row in rows:
        for cell in row:
            text = cell.value
            if type(text) is str:
                for word in text.split():
                    temp_word = word.translate(str.maketrans('', '', string.punctuation))
                    if not dictionary.check(temp_word):
                        suggest = dictionary.suggest(temp_word)[0]
                        print('Предположительная опечатка в слове', f"'{temp_word}' (Ячейка {cell.coordinate})")
                        print('Предположительно подходящее слово:', f"'{suggest}'")
                        suggest = input_answer_and_replace(temp_word, suggest)
                        if suggest:
                            text.replace(temp_word, suggest)
                cell.value = text
