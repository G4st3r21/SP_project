from PyScripts.TableClasses.PublicClasses.SPTable import SPTable
from PyScripts.TableClasses.PublicClasses.SPTableArbitrary import SPTableArbitrary
from PyScripts.base.base_functions import parser_init

cols, rows, cur, conn = parser_init('11.1. Контрольные события.xlsx', sheet_number=1, first_str_number=12)

ResponseObj = SPTable('response_obj', 'response_obj', cur, conn)
ControlEvent2020 = SPTableArbitrary('control_event2020', 'control_event', cur, conn, schema='Education')
CommentsCE2020 = SPTable('comments_ce2020', 'comment', cur, conn, schema='Education')
DateControlEvent2020 = SPTableArbitrary('date_control_event2020', 'date', cur, conn, schema='Education')

for row in rows:
    if not('Подпрограмма' in row[0].value or 'Основное мероприятие' in row[0].value):
        control_event_id = row[0].value.split()[2]
        control_event_id = control_event_id if control_event_id[-1] != '.' else control_event_id[:-1]
        code_main_event = '.'.join(control_event_id.split('.')[:2])
        control_event = row[1].value
        ControlEvent2020.add(control_event_id, code_main_event, control_event)

        response_obj = row[2].value
        response_obj_id = ResponseObj.add(response_obj)

        planed_date = row[3].value

        if row[4].value:
            event_done = True
            has_violation = False
        elif row[5].value:
            event_done = True
            has_violation = True
        elif row[6].value == '-':
            event_done = False
            has_violation = False

        comment = row[7].value

        DateControlEvent2020.add()