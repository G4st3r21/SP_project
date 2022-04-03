from PyScripts.base.base_functions import *


def cell_gp_fin_parsing(strk):
    if '"' in strk:
        gp_name = strk.split('"')[1]
    else:
        gp_name = 'Null'
    if "," in strk.split('"')[-1] and len(strk.split('"')) > 1:
        fin_source = str(strk.split('"')[-1])[1:].lower()
    else:
        fin_source = strk

    return gp_name, fin_source


def table_parsing():
    id_period, id_result = 0, 0
    periods, results = [], []
    for row in rows:
        if str(row[0].value)[:2] == 'СЦ':
            id_sub_aim = str(row[0].value).split()[0]
        else:
            id_event = str(row[1].value).split()[0]
            event = " ".join(str(row[1].value).split()[1:])

            period = row[2].value
            if period[:50] not in periods:
                id_period += 1
                periods.append(period[:50])
            else:
                temp_id_period = cur.execute(
                    f"SELECT * FROM implementation_period WHERE period LIKE {period}").fetchall()[0]

            result = row[3].value
            if results[:50] not in results:
                id_result += 1
                results.append(result[:50])
            else:
                temp_id_result = cur.execute(
                    f"SELECT * FROM expected_result WHERE result LIKE {result}").fetchall()[0]

            gp_name, fin_source = cell_gp_fin_parsing(row[4].value)
            has_that_gp = cur.execute(
                f"SELECT * FROM gosprogram WHERE gosprogram LIKE {gp_name}").fetchall()
            if has_that_gp:
                gp_id = has_that_gp[0]
            else:
                char_gp_id = cur.execute(
                    f"SELECT * FROM gosprogram").fetchall()[-1][0]
                gp_id = char_index_from_number(char_index_from_number_reversed(char_gp_id) + 1)
                cur.execute(f"INSERT INTO gosprogram VALUES ('{gp_id}', '{gp_name}')")

            response_obj = [obj.capitalize() for obj in str(row[5].value).split(';\n')]


cols, rows, first_str_number, cur, conn = parser_init("План мероприятий.xlsx", 3)
table_parsing()
conn.commit()
