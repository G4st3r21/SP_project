from PyScripts.Parsers.Industries.Education.functions import *
from openpyxl import *

table_name = "8. Ответственные и 9. Показатели.xlsx"
sheet_number = read_sheet_number()  # 0
start_row = read_first_str_number()  # 10

# cur, conn = db_conn()
sheet = load_workbook(table_name).worksheets[sheet_number]
suitable_rows = list(sheet.rows)[start_row:]

id_ = 0
code_events = 0
for row in suitable_rows:
    if row[1].value is not None:
        code_events = (row[1].value.split(" ")[len(row[1].value.split(" ")) - 1])  # todo
        if len(code_events) == 0 or code_events == "программа":
            code_events = "0"

    title_indicator = row[3].value
    if title_indicator is not None:
        print(f"{id_} {code_events} {id_} {row[6].value} {row[7].value} {row[8].value}")
        # cur.execute(f"INSERT INTO INDICATORS2017 VALUES ({id_}, '{code_events}', {id_}, '{row[6].value}', {row[7].value}, {row[8].value})")
        print(f"  {id_} {title_indicator} {row[5].value}")
        # cur.execute(f"INSERT INTO NAMES_INDICATORS2017 VALUES ({id_}, '{title_indicator}', '{row[5].value}')")
        if (row[9].value != "") and (row[9].value is not None):
            print(f"     {id_} {row[9].value}")
            # cur.execute(f"INSERT INTO ??? VALUES({id_},{row[9].value}")

        id_ = id_ + 1
# conn.commit()
