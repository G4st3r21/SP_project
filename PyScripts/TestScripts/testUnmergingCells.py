from PyScripts.base.base_functions import parser_init

cols, rows, cur, conn = parser_init("ОТЧЕТ_Развитие образования за 2016 год.xlsx", sheet_number=1, first_str_number=5)

for row in rows:
    print(row[2].value, row[3].value, row[5].value, row[6].value, sep='\t')