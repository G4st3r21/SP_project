from PyScripts.Parsers.Industries.Education.functions import *
from openpyxl import *

table_name = "ОТЧЕТ_Развитие образования за 2016 год.xlsx"
sheet_number = read_sheet_number()  # 6
start_row = read_first_str_number()  # 5

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
    if row[0].value is not None:
        code_events = (row[0].value.split(" ")[len(row[0].value.split(" ")) - 1])  # todo
        if len(code_events) == 0 or code_events == "программа":
            code_events = "0"

    # source_name prepare
    source_name = row[5].value
    while source_name[0] == " " or source_name[0] == "-":
        source_name = source_name[1:]
    if source_name.split(" ")[0] == "областной" and (len(source_name.split(" ")) > 2):
        source_name = sources[1]

    # find suitable row
    if source_name in sources and row[10].value != 0:
        print(f"{id_} {code_events} {sources.index(source_name)} {row[10].value} {row[11].value} {row[12].value}")
        id_ = id_ + 1
    # cur.execute()


for source in sources:
    print(f"{sources.index(source)} {source}")
    # cur.execute()
# conn.commit()
