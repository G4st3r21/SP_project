from PyScripts.Parsers.Industries.Education.functions import *
from openpyxl import *

table_name = "ОТЧЕТ_Развитие образования за 2016 год.xlsx"
sheet_number = read_sheet_number()  # 2
start_row = read_first_str_number()  # 6

cur, conn = db_conn()
sheet = load_workbook(table_name).worksheets[sheet_number]
suitable_rows = list(sheet.rows)[start_row:]
cur.execute("SET search_path TO 'Education'")

id_ = 0
code_events = 0
for row in suitable_rows:
    if row[2].value is not None:
        code_events = (row[2].value.split(" ")[len(row[2].value.split(" ")) - 1])  # todo
        if len(code_events) == 0:
            code_events = "0"
    if row[5].value is not None:
        print(f"{id_} {code_events} {id_} {row[9].value} {row[10].value} {row[11].value}")
        cur.execute(f"INSERT INTO INDICATORS2016 VALUES ({id_}, '{code_events}', {id_}, '{row[9].value}', {row[10].value}, {row[11].value})")
        id_ = id_ + 1

conn.commit()
cur.execute("SET search_path TO 'Public'")
