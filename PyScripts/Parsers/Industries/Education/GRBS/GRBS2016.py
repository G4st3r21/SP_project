from functions import *
from openpyxl import *

table_name = "ОТЧЕТ_Развитие образования за 2016 год.xlsx"
sheet_number = read_sheet_number()  # 3
start_row = read_first_str_number()  # 12

# cur, conn = db_conn()
wb = load_workbook(table_name)
sheet = wb.worksheets[sheet_number]
unmerge_all_cells(sheet)
suitable_rows = list(sheet.rows)[start_row:]

# cur.execute("SET search_path TO 'Education'")
code_events = 0
id_ = 0
response_index = ""

kbk = [] #public kbk
for row in suitable_rows:
    if (row[4].value is not None) and (row[4].value not in kbk):
        print(row[4].value)
        kbk.append(row[4].value)

# response = [] #
# for row in suitable_rows:
#     if (row[3].value is not None) and (row[3].value not in kbk):
#         print(row[3].value)
#         response.append(row[3].value)

for row in suitable_rows:
    if row[0].value is not None:
        code_events = (row[0].value.split(" ")[len(row[0].value.split(" ")) - 1])  # todo
        if len(code_events) == 0 or code_events == "программа":
            code_events = "0"

    if row[3].value is not None:
        response_index = response.index(row[3].value)

    if row[4].value is not None:
        print(f"{id_} {code_events} {response_index} {kbk.index(row[4].value)} {0} {roundOrNone(row[6].value)} {roundOrNone(row[7].value)}")
        id_ = id_ + 1
        print(f"{id_} {code_events} {response_index} {kbk.index(row[4].value)} {1} {roundOrNone(row[9].value)} {roundOrNone(row[10].value)}")
        id_ = id_ + 1
        print(f"{id_} {code_events} {response_index} {kbk.index(row[4].value)} {2} {roundOrNone(row[12].value)} {roundOrNone(row[13].value)}")
        id_ = id_ + 1
        print(f"{id_} {code_events} {response_index} {kbk.index(row[4].value)} {4} {roundOrNone(row[15].value)} {roundOrNone(row[16].value)}")
        id_ = id_ + 1
        print(f"{id_} {code_events} {response_index} {kbk.index(row[4].value)} {6} {roundOrNone(row[18].value)} {roundOrNone(row[19].value)}")
        id_ = id_ + 1

# conn.commit()
# cur.execute("SET search_path TO 'Public'")
