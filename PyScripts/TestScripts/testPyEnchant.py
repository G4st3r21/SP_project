from PyScripts.base.base_functions import checking_for_typos, parser_init

cols, rows = parser_init('ОТЧЕТ_Развитие образования за 2016 год.xlsx', 1, 6, need_db_conn=False)

checking_for_typos(rows)

for row in rows[3]:
    for cell in row:
        print(cell.value)
