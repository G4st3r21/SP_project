from PyScripts.Parsers.Industries.Education.functions import *
from openpyxl import *

table_name = "10. По ГРБС, 11. По статьям, 12. Источники и 13. Субсидии.xlsx"
sheet_number = read_sheet_number()  # 2
start_row = read_first_str_number()  # 12

# cur, conn = db_conn()
sheet = load_workbook(table_name).worksheets[sheet_number]
suitable_rows = list(sheet.rows)[start_row:277]

# cur.execute("SET search_path TO 'Education'")
print(list(sheet.rows)[0][0].value)
code_events = 0
id_ = 0
for row in suitable_rows:
    if row[1].value is not None:
        code_events = (row[1].value.split(" ")[len(row[1].value.split(" ")) - 1])  # todo
        if len(code_events) == 0 or code_events == "программа":
            code_events = "0"

    print(row[3].value.split(" "))
    if row[3].value.split(" ")[0] == "НИОКР":
        ex_item = 4
    elif row[3].value.split(" ")[0] == "ПРОЧИЕ":
        ex_item = 5
    elif row[3].value.split(" ")[3] == "числе:":
        ex_item = 0
    elif row[3].value.split(" ")[3] == "всего":
        ex_item = 1
    elif row[3].value.split(" ")[0] == "субсидии":
        ex_item = 3
    elif row[3].value.split(" ")[0] == "бюджетные":
        ex_item = 6
    elif row[3].value.split(" ")[3] == "(за":
        ex_item = 7
    elif row[3].value.split(" ")[3] == "(объекты":
        ex_item = 2
    else:
        print("NOT FOUND")
        ex_item = "wettetee"

    print(f"{id_} {code_events} {expense_items[ex_item]} {0} {row[5].value} {row[6].value}")
    # cur.execute()
    id_ = id_ + 1
    print(f"{id_} {code_events} {expense_items[ex_item]} {1} {row[8].value} {row[9].value}")
    # cur.execute()
    id_ = id_ + 1
    print(f"{id_} {code_events} {expense_items[ex_item]} {2} {row[11].value} {row[12].value}")
    # cur.execute()
    id_ = id_ + 1
    print(f"{id_} {code_events} {expense_items[ex_item]} {3} {row[14].value} {row[15].value}")
    # cur.execute()
    id_ = id_ + 1
# conn.commit()
# cur.execute("SET search_path TO 'Public'")
