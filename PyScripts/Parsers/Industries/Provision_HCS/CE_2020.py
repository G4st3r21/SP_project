from PyScripts.TableClasses.SPTables.SPTable import SPTable
from PyScripts.TableClasses.SPTables.SPTableArbitrary import SPTableArbitrary
from PyScripts.TableClasses.SPTables.SPTableManyToMany import SPTableManyToMany
from PyScripts.base.base_functions import parser_init


def commit_all():
    ResponseObj.commit()
    ControlEvent2020.commit()
    CommentsCE2020.commit()
    DateControlEvent2020.commit()


def table_parsing():
    for row in rows:
        # if ('Подпрограмма' in row[0].value or 'Основное мероприятие' in row[0].value):
        #     code = row[0].value.split()[1]
        #     code = code if code[-1] != '.' else code[:-1]
        #     code_main_event = '.'.join(code.split('.')[:2])
        #     control_event = row[1].value if row[1].value != None else control_event
        #     print(code, code_main_event, control_event)
        #     ControlEvent2020.add(code, code_main_event, control_event)

        if row[0].value != "" and not ('Подпрограмма' in row[0].value or 'Основное мероприятие' in row[0].value):
            code = row[0].value.split()[2]
            code = code if code[-1] != '.' else code[:-1]
            code_main_event = '.'.join(code.split('.')[:2])
            control_event = row[1].value if row[1].value != None else control_event
            print(code, code_main_event, control_event)
            code = ControlEvent2020.add(code, code_main_event, control_event)

            response_obj = row[2].value
            id_response = ResponseObj.add(response_obj)
            commit_all()

            id_pf = 0
            id_done = 0
            id_viol = 0
            date_ce = row[3].value
            DateControlEvent2020.add(code, id_response, id_pf, id_done, id_viol, date_ce)

            if row[4].value:
                # event_done = True
                # has_violation = False
                id_pf = 1
                id_done = 1
                id_viol = 0
                date_ce = row[4].value

            elif row[5].value:
                # event_done = True
                # has_violation = True
                id_pf = 1
                id_done = 1
                id_viol = 1
                date_ce = row[5].value

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

cols, rows, cur, conn = parser_init('11.1. Контрольные события.xlsx', sheet_number=1, first_str_number=12)
ResponseObj = SPTable('response_obj', cur, conn)
ControlEvent2020 = SPTableArbitrary('control_event2020', cur, conn, schema='Provision_HCS')
CommentsCE2020 = SPTableArbitrary('comments_ce2020',  cur, conn, schema='Provision_HCS')
DateControlEvent2020 = SPTableArbitrary('date_control_event2020', cur, conn, schema='Provision_HCS')
table_parsing()

