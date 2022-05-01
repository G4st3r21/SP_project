from PyScripts.Parsers.Industries.Education.functions import *
from openpyxl import *

table_name = "ОТЧЕТ_Развитие образования за 2016 год.xlsx"
sheet_number = read_sheet_number()  # 2
start_row = read_first_str_number()  # 6

cur, conn = db_conn()
sheet = load_workbook(table_name).worksheets[sheet_number]
suitable_rows = list(sheet.rows)[start_row:]

id_ = 0
for row in suitable_rows:
    title_indicator = row[5].value
    if title_indicator is not None:
        print(f"{id_} {title_indicator} {row[8].value}")
        cur.execute(f"INSERT INTO NAMES_INDICATORS2016 VALUES ({id_}, '{title_indicator}', '{row[8].value}')")
        id_ = id_ + 1
conn.commit()
