import datetime

from PyScripts.TableClasses.SPTables.SPTable import SPTable
from PyScripts.TableClasses.SPTables.SPTableArbitrary import SPTableArbitrary
from PyScripts.base.base_functions import parser_init


def commit_all():
    ResponseObj.commit()
    ControlEvent2020.commit()
    CommentsCE2020.commit()
    DateControlEvent2020.commit()


def table_parsing():
    for row in rows:

        if ('Контрольное событие' in row[1].value):
            # my_list = list()
            # my_list.append(row[1].value)
            # print(my_list[1])
            my_list = row[1].value.split('\n')
            my_list_1 = list()
            my_list_1.append(my_list[0])

            code = my_list_1[0].split()[2]
            code = code if code[-1] != '.' else code[:-1]
            code_main_event = '.'.join(code.split('.')[:2])
            control_event = my_list[1]
            print(code, code_main_event, control_event)
            code = ControlEvent2020.add(code, code_main_event, control_event)

            if row[2].value:
                response_obj = row[2].value
                id_response = ResponseObj.add(response_obj)
            commit_all()

            id_pf = 0
            id_done = 0
            id_viol = 0
            date_ce = datetime.datetime.date(row[3].value).strftime("%Y.%m.%d")
            DateControlEvent2020.add(code, id_response, id_pf, id_done, id_viol, date_ce)
            # row[3].value.split('\n')
            # my_list_d = row[3].value.split('\n')
            # if len(my_list_d) > 1:
            #     print(my_list_d)
            #     for i in range(0, len(my_list_d)):
            #         date_ce = my_list_d[i]
            #         DateControlEvent2020.add(code, id_response, id_pf, id_done, id_viol, date_ce)
            # elif len(my_list_d) == 1:
            #     date_ce = datetime.datetime.date(row[3].value).strftime("%Y.%m.%d")
            #     DateControlEvent2020.add(code, id_response, id_pf, id_done, id_viol, date_ce)

            if row[4].value:
                # event_done = True
                # has_violation = False
                id_pf = 1
                id_done = 1
                id_viol = 0
                date_ce = datetime.datetime.date(row[4].value).strftime("%Y.%m.%d")
                DateControlEvent2020.add(code, id_response, id_pf, id_done, id_viol, date_ce)
                # row[4].value.split('\n')
                # my_list_d = row[4].value.split('\n')
                # if len(my_list_d) > 1:
                #     print(my_list_d)
                #     for i in range(0, len(my_list_d)):
                #         date_ce = my_list_d[i]
                #         DateControlEvent2020.add(code, id_response, id_pf, id_done, id_viol, date_ce)
                #
                # elif len(my_list_d) == 1:
                #     date_ce = datetime.datetime.date(row[4].value).strftime("%Y.%m.%d")
                #     DateControlEvent2020.add(code, id_response, id_pf, id_done, id_viol, date_ce)

            elif row[5].value:
                # event_done = True
                # has_violation = True
                id_pf = 1
                id_done = 1
                id_viol = 1
                date_ce = datetime.datetime.date(row[5].value).strftime("%Y.%m.%d")
                DateControlEvent2020.add(code, id_response, id_pf, id_done, id_viol, date_ce)
                # row[5].value.split('\n')
                # my_list_d = row[5].value.split('\n')
                # if len(my_list_d) > 1:
                #     print(my_list_d)
                #     for i in range(0, len(my_list_d)):
                #         date_ce = my_list_d[i]
                #         DateControlEvent2020.add(code, id_response, id_pf, id_done, id_viol, date_ce)
                # elif len(my_list_d) == 1:
                #     date_ce = datetime.datetime.date(row[5].value).strftime("%Y.%m.%d")
                #     DateControlEvent2020.add(code, id_response, id_pf, id_done, id_viol, date_ce)

            elif row[6].value == '-':
                # event_done = False
                # has_violation = False
                id_pf = 1
                id_done = 0
                id_viol = 0
                date_ce = "11.11.1111"

            id = DateControlEvent2020.add(code, id_response, id_pf, id_done, id_viol, date_ce)
            print(code, id_response, id_pf, id_done, id_viol, date_ce)
            print(id)

            if row[7].value:
                comment = row[7].value
                CommentsCE2020.add(id, comment)

        commit_all()

cols, rows, cur, conn = parser_init('Социальная поддержка_граждан_2020.xlsx', sheet_number=5, first_str_number=83)
ResponseObj = SPTable('response_obj', cur, conn)
ControlEvent2020 = SPTableArbitrary('control_event2020', cur, conn, schema='Social_Support')
CommentsCE2020 = SPTableArbitrary('comments_ce2020', cur, conn, schema='Social_Support')
DateControlEvent2020 = SPTableArbitrary('date_control_event2020', cur, conn, schema='Social_Support')
table_parsing()