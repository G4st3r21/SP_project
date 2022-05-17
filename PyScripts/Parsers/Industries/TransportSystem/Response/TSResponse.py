from PyScripts.TableClasses.SPTables.SPTableArbitrary import SPTableArbitrary
from PyScripts.TableClasses.SPTables.SPTableManyToMany import SPTableManyToMany
from PyScripts.base.base_functions import parser_init, format_title, partition, parts
from PyScripts.TableClasses.PublicClasses.Gosprogram import Gosprogram
from PyScripts.TableClasses.SPTables.SPTable import SPTable


def commit_all():
    Gosprogram.commit()
    Subprogram.commit()
    MainEvent.commit()
    Event.commit()
    ResponseObj.commit()
    EventsResponseObj.commit()
    EventsResponseFio.commit()


def part(string):
    if '-' in string:
        if string[string.find('-') + 1] != ' ' and string[string.find('-') - 1] != ' ':
            string = string.replace('-', ' ')
        else:
            string = string.replace('-', '')
    parts = string.replace('\n', ' ').split()
    str_list = list()
    k = 0
    if len(parts) > 1:
        for i in range(len(parts) - 1):
            parts[i] = parts[i].strip()
            if (len(parts[i]) >= 4 and parts[i][0] in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ' and parts[i][1] == '.' and\
                    parts[i][2] in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ' and parts[i][3] == '.' and
                    parts[i+1][0] in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'):
                str_list.append(' '.join(parts[k:i + 2]))
                k = i + 2
    str_list.append(' '.join(parts[k:]))
    for j in range(len(str_list)):
        str_list[j] = str_list[j].strip()
        str_list[j] = ' '.join(str_list[j].split())
        # if not (str_list[j] in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'):
        #     str_list[j] = str_list[j].replace(str_list[j].split()[0], str_list[j].split()[0].capitalize())
        if str_list[j].endswith('\n') or str_list[j].endswith(';') or str_list[j].endswith(':') or str_list[j].endswith(','):
            str_list[j] = str_list[j][:-1]
        # if str_list[j].split()[0] == 'Врио' or str_list[j].split()[0] == 'врио':
        #     str_list[j] = str_list[j].replace(str_list[j].split()[0], 'ВРИО')

    return str_list


def table_parsing():
    global prog, subprog, subprog_id, prog_id, main_event_id, code_events
    response_fio_id = 0
    for row in rows:
        if row[first_column].value is not None:
            if 'Государственная программа' in row[first_column].value:
                prog = format_title(row[first_column + 1].value)
                prog_id = Gosprogram.add_new(prog)
                AllEvents.add(prog_id, prog)
                code_events = prog_id

            if 'Подпрограмма'in row[first_column].value:
                subprog = format_title(row[first_column + 1].value)
                subprog_id = format_title(row[first_column].value).split()[1]
                AllEvents.add(subprog_id, subprog)
                Subprogram.add(subprog_id, prog_id, subprog)
                code_events = subprog_id

            if 'Основное мероприятие' in row[first_column].value:
                main_event = format_title(row[first_column + 1].value)
                main_event_id = format_title(row[first_column].value).split()[2]
                AllEvents.add(main_event_id, main_event)
                MainEvent.add(main_event_id, subprog_id, main_event)
                code_events = main_event_id

            if 'Мероприятие' in row[first_column].value:
                event = format_title(row[first_column + 1].value)
                event_id = format_title(row[first_column].value).split()[1]
                AllEvents.add(event_id, event)
                Event.add(event_id, main_event_id, event)
                code_events = event_id

            # if 'Ответственный исполнитель' in row[first_column + 2].value:
            #     response_obj = format_title(' '.join(row[first_column + 2].value.split()[2:]))
            #     response_obj_id = ResponseObj.add(response_obj)
            #     print(response_obj)
            #     ResponseMain.add(response_obj_id)
            # else:
            #     response_obj = format_title(' '.join(row[first_column + 2].value.split()[1:]))
            #     print(response_obj)
            #     response_obj_id = ResponseObj.add(response_obj)

            response_obj = format_title(row[first_column + 2].value)
            response_obj_id = ResponseObj.add(response_obj)

            fio = part(row[first_column + 3].value)
            for response_fio in fio:
                if response_fio is not None and len(response_fio) > 1:
                    response_fio_id += 1
                    if ResponseFio.add(response_fio_id, response_obj_id, response_fio) is not None \
                            and response_fio_id > int(ResponseFio.add(response_fio_id, response_obj_id, response_fio)):
                        EventsResponseFio.add(code_events,
                                              str(ResponseFio.add(response_fio_id, response_obj_id, response_fio)))
                        print(code_events, response_fio)
                        response_fio_id -= 1
                    else:
                        EventsResponseFio.add(code_events, response_fio_id)
                        print(code_events, response_fio)

        EventsResponseObj.add(code_events, response_obj_id)

        commit_all()


cols, rows, cur, conn = parser_init("2020.xlsx",
                                    sheet_number=1, first_str_number=10)
first_column = 1
year = str(2020)

Gosprogram = Gosprogram(cur, conn)
Subprogram = SPTableArbitrary('subprogram' + year, cur, conn, schema='Transport_System')
MainEvent = SPTableArbitrary('main_event' + year, cur, conn, schema='Transport_System')
Event = SPTableArbitrary('event' + year, cur, conn, schema='Transport_System')
AllEvents = SPTableManyToMany('all_events' + year, cur, conn, schema='Transport_System')
ResponseObj = SPTable('response_obj', cur, conn)
ResponseFio = SPTableArbitrary('response_fio' + year, cur, conn, schema='Transport_System')
EventsResponseObj = SPTableManyToMany('events_response_obj' + year, cur, conn, schema='Transport_System')
EventsResponseFio = SPTableManyToMany('events_response_fio' + year, cur, conn, schema='Transport_System')

first_column -= 1
table_parsing()
