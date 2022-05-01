from PyScripts.Parsers.Industries.Education.functions import *
from openpyxl import *

table_name = "8. Ответственные и 9. Показатели.xlsx"
sheet_number = read_sheet_number()  # 2
start_row = read_first_str_number()  # 10

cur, conn = db_conn()
cur.execute("SET search_path TO 'Education'")
sheet = load_workbook(table_name).worksheets[sheet_number]
suitable_rows = list(sheet.rows)[start_row:]

id_ = 0
for row in suitable_rows:
    title_indicator = row[3].value
    if title_indicator is not None:
        print(f"{id_} {title_indicator} {row[5].value}")
        cur.execute(f"INSERT INTO NAMES_INDICATORS2017 VALUES ({id_}, '{title_indicator}', '{row[5].value}')")
        id_ = id_ + 1
conn.commit()
cur.execute("SET search_path TO 'Public'")
