from PyScripts.base.base_functions import parser_init

cols, rows, cur, conn = parser_init("/home/g4st3r/PycharmProjects/SP_project/PyScripts/CUR/ЦУР и ГП ВО_показатели.xlsx", sheet_number=1, first_str_number=6)

for row in rows:
    print(*row)