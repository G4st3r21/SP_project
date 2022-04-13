from datetime import datetime as dt
from PyScripts.base.base_functions import *


def sql_work(task_id):
    cur, conn = db_conn()
    cur.execute(f"select title, sub_aim_id from tasks where id = 'З2.2.10'")
    task_name, sub_aim_id = cur.fetchall()[0]
    cur.execute(f"select * from strategy_aim where id = (select aim_id from strategy_sub_aim where id = '{sub_aim_id}')")
    aim_id, aim = cur.fetchall()[0]

    return [task_name, aim_id, aim]


def xlsx_work(task_id):
    wb = xlsx_connect("../Plan_meropriatii/План мероприятий.xlsx")
    all_ws = wb.worksheets
    ws_1 = all_ws[0]
    ws_4 = all_ws[3]

    for i in range(len(list(ws_1.columns)[2])):
        if list(ws_1.columns)[2][i].value is not None and list(ws_1.columns)[2][i].value == task_id:
            task_name = list(ws_1.columns)[3][i].value
            sub_aim_id = list(ws_1.columns)[0][i].value
            aim_id = int(sub_aim_id[2])
            break

    for i in range(len(list(ws_4.columns)[0])):
        if i-2 == aim_id:
            aim = list(ws_4.columns)[1][i].value
            break

    return [task_name, aim_id, aim]


start_sql = dt.now()
answer_sql = sql_work('З2.2.10')
end_sql = dt.now()
print('SQL-запросы из БД:', end_sql-start_sql)

start_xlsx = dt.now()
answer_xlsx = xlsx_work('З2.2.10')
end_xlsx = dt.now()
print('Поиск по Excel таблицам:', end_xlsx-start_xlsx)

