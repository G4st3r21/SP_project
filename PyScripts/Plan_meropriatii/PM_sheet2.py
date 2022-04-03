from PyScripts.base.base_functions import *
from datetime import datetime as dt
from PyScripts.TableClasses.ResponseObjects import rp


def format_ind_title(indicator_title):
    if indicator_title[0].isdigit():
        return ' '.join(indicator_title.split()[1:])
    elif indicator_title[:2].isdigit():
        return indicator_title[5:]
    else:
        return indicator_title


def format_indicator(indicator: str):
    if indicator is None or str(indicator) == "-":
        return [None, False, False]
    elif "не более" in str(indicator).lower() or "<=" in str(indicator).lower() or "<" in str(indicator).lower():
        return [float(str(indicator).split()[-1].replace(',', '.')), True, False]
    elif "не менее" in str(indicator).lower() or "=>" in str(indicator).lower() or ">" in str(indicator).lower():
        return [float(str(indicator).split()[-1].replace(',', '.')), False, True]
    else:
        return [float(''.join(str(indicator).split()).replace(',', '.')), False, False]


def table_parsing():
    indicator_id = 0
    for row in rows:
        if str(row[0].value)[:2] == 'СЦ':
            strategy_sub_aim = str(str(row[0].value).split()[0])[0:-1]
        else:
            indicator_title_id = row[0].value
            indicator_title = format_ind_title(row[1].value)
            indicator_type = indicator_title.split(',')[-1]
            response_obj = [obj.capitalize() for obj in str(row[13].value).split(';\n')]
            indicators = [format_indicator(row[year].value) for year in range(2, 13)]

            # cur.execute(
            #     f"INSERT INTO indicators_names VALUES ({indicator_title_id}, '{indicator_title}',"
            #     f" '{indicator_type}', '{strategy_sub_aim}')")

            indicator_number = 0
            for year in range(2016, 2036):
                if not (year in range(2025, 2030) or year in range(2031, 2035)):
                    # start = dt.now()
                    indicator_id += 1
                    year_id = year - 2015
                    # if indicators[indicator_number][0] is None:
                      # cur.execute(f"INSERT INTO indicators VALUES ({indicator_id}, {indicator_title_id},"
                      #           f" {year_id}, Null, False, False)")
                    # else:
                      # cur.execute(f"INSERT INTO indicators VALUES ({indicator_id}, {indicator_title_id},"
                      #           f" {year_id}, {indicators[indicator_number][0]}, {indicators[indicator_number][1]},"
                      #           f" {indicators[indicator_number][2]})")
                    indicator_number += 1
                    # end = dt.now()
                    # print(end - start)

            for obj in response_obj:
                id_resp_obj = rp.find_id_by_name(obj)
                id_resp_obj = rp.add_new(obj) if not id_resp_obj else id_resp_obj
                cur.execute(f"INSERT INTO INDICATORS_AND_RESPONSE_OBJ VALUES ({indicator_title_id}, {id_resp_obj})")


cols, rows, cur, conn = parser_init("План мероприятий.xlsx", 2)
table_parsing()
conn.commit()
