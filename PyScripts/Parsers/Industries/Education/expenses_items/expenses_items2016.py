from PyScripts.Parsers.Industries.Education.functions import *
from openpyxl import *

table_name = "ОТЧЕТ_Развитие образования за 2016 год.xlsx"
sheet_number = read_sheet_number()  # 4
start_row = read_first_str_number()  # 12

# cur, conn = db_conn()
sheet = load_workbook(table_name).worksheets[sheet_number]
suitable_rows = list(sheet.rows)[start_row:]

id_ = 0
for category in categories:
    print(f"{id_} {categories[id_]} тыс.рублей")
    id_ = id_ + 1
    # cur.execute()

id_ = 0
for item in expense_items:
    print(f"{id_} {expense_items[id_]}")
    id_ = id_ + 1
    # cur.execute()

# cur.execute("SET search_path TO 'Education'")
print(list(sheet.rows)[0][0].value)
code_events = 0
id_ = 0
for row in suitable_rows:
    if row[0].value is not None:
        code_events = (row[0].value.split(" ")[len(row[0].value.split(" ")) - 1])  # todo
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
        ex_item = "twetwetwewte"

    print(f"{id_} {code_events} {expense_items[ex_item]} {0} {row[6].value} {row[7].value}")
    # cur.execute()
    id_ = id_ + 1
    print(f"{id_} {code_events} {expense_items[ex_item]} {1} {row[10].value} {row[11].value}")
    # cur.execute()
    id_ = id_ + 1
    print(f"{id_} {code_events} {expense_items[ex_item]} {2} {row[13].value} {row[14].value}")
    # cur.execute()
    id_ = id_ + 1
    print(f"{id_} {code_events} {expense_items[ex_item]} {3} {row[16].value} {row[17].value}")
    # cur.execute()
    id_ = id_ + 1
# conn.commit()
# cur.execute("SET search_path TO 'Public'")
