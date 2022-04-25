from PyScripts.Parsers.Industries.Education.functions import *
from openpyxl import *

table_name = "11. Статьи расходов.xlsx"
sheet_number = read_sheet_number()  # 0
start_row = read_first_str_number()  # 12

# cur, conn = db_conn()
sheet = load_workbook(table_name).worksheets[sheet_number]
suitable_rows = list(sheet.rows)[start_row:255]

# cur.execute("SET search_path TO 'Education'")
print(list(sheet.rows)[0][0].value)
code_events = 0
id_ = 0
for row in suitable_rows:
    if row[0].value is not None:
        code_events = (row[0].value.split(" ")[len(row[0].value.split(" ")) - 1])  # todo
        if len(code_events) == 0 or code_events == "программа":
            code_events = "0"

    print(row[2].value.split(" "))
    if row[2].value.split(" ")[0] == "Всего,":
        ex_item = 0
    elif row[2].value.split(" ")[0] == "Государственные":
        ex_item = 8
    elif row[2].value.split(" ")[0] == "Прочие":
        ex_item = 5
    else:
        print("NOT FOUND")
        ex_item = "wertwetew"

    print(f"{id_} {code_events} {expense_items[ex_item]} {0} {row[4].value} {row[5].value}")
    # cur.execute()
    id_ = id_ + 1
    print(f"{id_} {code_events} {expense_items[ex_item]} {1} {row[7].value} {row[8].value}")
    # cur.execute()
    id_ = id_ + 1
    print(f"{id_} {code_events} {expense_items[ex_item]} {4} {row[10].value} {row[11].value}")
    # cur.execute()
    id_ = id_ + 1
    print(f"{id_} {code_events} {expense_items[ex_item]} {3} {row[13].value} {row[14].value}")
    # cur.execute()
    id_ = id_ + 1
# conn.commit()
# cur.execute("SET search_path TO 'Public'")
