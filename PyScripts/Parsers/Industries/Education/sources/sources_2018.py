from PyScripts.Parsers.Industries.Education.functions import *
from openpyxl import *

table_name = "Отчет за 2018 год_финансирование.xlsx"
sheet_number = read_sheet_number()  # 3
start_row = read_first_str_number()  # 8

# cur, conn = db_conn()
sheet = load_workbook(table_name).worksheets[sheet_number]
suitable_rows = list(sheet.rows)[start_row:]

sources = [
    "федеральный бюджет (бюджетные ассигнования, не предусмотренные законом Воронежской области об областном бюджете)",
    "областной бюджет (бюджетные ассигнования, предусмотренные законом Воронежской области об областном бюджете, всего)",
    "федеральный бюджет",
    "областной бюджет",
    "местный бюджет",
    "территориальные государственные внебюджетные фонды",
    "юридические лица",
    "физические лица"
]

id_ = 0
code_events = "0"
for row in suitable_rows:
    # zero index
    if row[1].value is not None:
        code_events = (row[1].value.split(" ")[len(row[1].value.split(" ")) - 1])  # todo
        if len(code_events) == 0 or code_events == "программа":
            code_events = "0"

    # source_name prepare
    source_name = row[3].value
    while source_name[0] == " " or source_name[0] == "-":
        source_name = source_name[1:]

    # find suitable row
    if source_name in sources and row[4].value != 0:
        print(f"{id_} {code_events} {sources.index(source_name)} {row[4].value} {row[5].value} {row[6].value}")
        id_ = id_ + 1
    # cur.execute()
# conn.commit()
