from PyScripts.base.base_functions import *

test_file = "План мероприятий.xlsx"
table_names = ["strategy_sub_aim", "tasks"]

sheet_number = 1
first_str_number = read_first_str_number()

cur, conn = db_conn()
ws = xlsx_connect(test_file).worksheets[sheet_number-1]

columns = list(ws.columns)
rows = list(ws.rows)
# print(columns)

sub_aim_fullIDs = []
task_titles = []

sub_aim_id = 0
task_id = 0
for row in rows[first_str_number:]:
    sub_aim_was_already = False
    for cell in row:
        if len(cell.value) > 6 and 'A' in cell.coordinate:
            print('len > than 6')
            break

        if 'A' in cell.coordinate:
            sub_aim_id = cell.value
            aim_id = cell.value[2]

            if sub_aim_id not in sub_aim_fullIDs:
                sub_aim_fullIDs.append(sub_aim_id)
                sub_aim_was_already = False
            else:
                sub_aim_was_already = True

        elif 'B' in cell.coordinate:
            if not sub_aim_was_already:
                sub_aim_title = cell.value
                # cur.execute(f"INSERT INTO {table_names[0]} values ('{sub_aim_id}', '{sub_aim_title}', {aim_id})")
                print(f"-- INSERT INTO {table_names[0]} values ({sub_aim_id}, '{sub_aim_title}', {aim_id})")

        elif 'C' in cell.coordinate:
            task_id = cell.value

        elif 'D' in cell.coordinate:
            task_title = cell.value
            if task_title not in task_titles:
                task_titles.append(task_title)

                # cur.execute(f"INSERT INTO {table_names[1]} values ('{task_id}', '{task_title}', '{sub_aim_id}')")
                print(f"-- INSERT INTO {table_names[1]} values ({task_id}, '{task_title}', {sub_aim_id})")

conn.commit()
