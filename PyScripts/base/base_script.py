from base_functions import *

test_file = "../Plan_meropriatii/План мероприятий.xlsx"
table_names = ["strategy_aim", "gosprogram", "aim_and_gosprogram"]


sheet_number = read_sheet_number()
first_str_number = read_first_str_number()

cur, conn = db_conn()
ws = xlsx_connect(test_file).worksheets[sheet_number]

columns = list(ws.columns)
rows = list(ws.rows)
# print(columns)

aim_id_list = []
for aim_id, cell in enumerate(columns[table_names.index(table_names[0])][first_str_number:], start=1):
    aim = cell.value
    # print(f"{aim_id}: {aim}")
    # cur.execute(f"INSERT INTO {table_names[0]} VALUES ({aim_id}, '{aim}')")
    print(f"INSERT INTO {table_names[0]} values ({aim_id}, '{aim}')")
    aim_id_list.append(aim_id)


print()
gp_id = 0
gosprograms_for_each_rows = []
for cell in columns[table_names.index(table_names[1])][first_str_number:]:
    cell_text = cell.value
    temp_id_list = []

    gosprograms = cell_text.split("\n")
    for gosprogram in gosprograms:
        gp_name = gosprogram.split('.')[1]
        gp_name = gp_name[2:-1]
        # print(f"{gp_id}: {gp_name}")
        cur.execute(f"INSERT INTO {table_names[1]} values ('{char_index_from_number(gp_id)}', '{gp_name}')")
        # print(f"INSERT INTO {table_names[1]} values ({char_index_from_number(gp_id)}, '{gp_name}')")

        temp_id_list.append(char_index_from_number(gp_id))
        gp_id += 1

    gosprograms_for_each_rows.append(temp_id_list)


print()
for i in range(len(aim_id_list)):
    number_id = i * len(aim_id_list) + i
    for j in gosprograms_for_each_rows[i]:
        cur.execute(f"INSERT INTO {table_names[2]} values ({aim_id_list[i]}, '{j}')")
        # print(f"INSERT INTO {table_names[2]} values ({aim_id_list[i]}, {j})")

conn.commit()
print("\nТаблицы успешно заполнены")
