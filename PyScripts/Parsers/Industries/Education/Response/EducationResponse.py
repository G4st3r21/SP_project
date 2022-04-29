from PyScripts.TableClasses.PublicClasses.SPTableArbitrary import SPTableArbitrary
from PyScripts.base.base_functions import parser_init
from PyScripts.TableClasses.PublicClasses.Gosprogram import Gosprogram
from PyScripts.TableClasses.PublicClasses.SPTable import SPTable


def partition(str):
    parts = str.split()
    str_list = list()
    k = 0
    for i in range(len(parts)):
        if parts[i][0] in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ' and ',' in parts[i]:
            str_list.append(' '.join(parts[k:i + 1]))
            k = i + 1
    str_list.append(' '.join(parts[k:]))
    for j in range(len(str_list)):
        str_list[j] = str_list[j].replace(str_list[j].split()[0], str_list[j].split()[0].capitalize())
        if str_list[j][-1] in '.,\n;:-+=?!':
            str_list[j] = str_list[j][:-1]
    return str_list



def format_title(str):
    if '\n' in str and str[-1] != '\n':
        str.replace('\n', ' ')
    elif str[-1] == '\n':
        str.replace('\n', '')

    if str[-1] == '.':
        str.replace('.', '')

    # str[0].capitalize()

    return ' '.join(str.split())


def table_parsing():
    # global prog_id
    global prog, subprog, subprog_id, prog_id, main_event_id, code_events
    response_fio_id = 0
    for row in rows:
        # if row[2].value is not None:
        if 'Государственная программа' in row[2].value:
            prog = row[3].value
            prog_id = Gosprogram.add_new(prog)
            code_events = AllEvents.add(prog_id, prog)

        if 'Подпрограмма' in row[2].value:
            subprog = format_title(row[3].value)
            subprog_id = row[2].value.split()[1]
            code_events = AllEvents.add(subprog_id, subprog)
            Subprogram.add(subprog_id, prog_id, subprog)

        if 'Основное мероприятие' in row[2].value:
            main_event = format_title(row[3].value)
            main_event_id = row[2].value.split()[2]
            code_events = AllEvents.add(main_event_id, main_event)
            MainEvent.add(main_event_id, subprog_id, main_event)
            # print(subprog, subprog_id, main_event, main_event_id)

        if 'Мероприятие' in row[2].value:
            event = format_title(row[3].value)
            event_id = row[2].value.split()[1]
            code_events = AllEvents.add(event_id, event)
            Event.add(event_id, main_event_id, event)
            # print(main_event, main_event_id, event_id, event)

        response_obj = format_title(row[5].value)
        response_obj_id = ResponseObj.add(response_obj)

        fio = partition(format_title(row[6].value))
        for response_fio in fio:
            response_fio_id += 1
            print(response_fio)
            if response_fio_id > int(ResponseFio.add(response_fio_id, response_obj_id, response_fio)):
                response_fio_id -= 1
        # response_fio_id = ResponseFio.add(response_fio_id, response_obj_id, response_fio)

        EventsResponseObj.add(code_events, response_obj_id)
        EventsResponseFio.add(code_events, response_fio_id)

        if row == rows[74] or row == rows[75]:
            print(*row)


cols, rows, cur, conn = parser_init("ОТЧЕТ_Развитие образования за 2016 год.xlsx", sheet_number=1, first_str_number=6)

Gosprogram = Gosprogram(cur, conn)
Subprogram = SPTableArbitrary('subprogram2016', 'title_subprog', cur, conn, schema='Education')
MainEvent = SPTableArbitrary('main_event2016', 'main_event', cur, conn, schema='Education')
Event = SPTableArbitrary('event2016', 'event', cur, conn, schema='Education')
AllEvents = SPTableArbitrary('all_events2016', 'events', cur, conn, schema='Education')
ResponseObj = SPTable('response_obj', 'response_obj', cur, conn)
ResponseFio = SPTableArbitrary('response_fio2016', 'fio', cur, conn, schema='Education')
EventsResponseObj = SPTableArbitrary('events_response_obj2016', 'code_events', cur, conn, schema='Education')
EventsResponseFio = SPTableArbitrary('events_response_fio2016', 'code_events', cur, conn, schema='Education')

table_parsing()

