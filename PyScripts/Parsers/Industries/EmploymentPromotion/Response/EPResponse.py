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
    # ResponseMain.commit()


def part(string):
    if '-' in string:
        if string[string.find('-') + 1] != ' ' and string[string.find('-') - 1] != ' ':
            string = string.replace('-', ' ')
        else:
            string = string.replace('-', '')

    # if '\n' in string:
    #     str_list = string.strip().split('\n')
    #     for i in range(len(str_list)):
    #         str_list[i] = format_title(str_list[i])
    #     return str_list

    parts = string.replace('\n', ' ').strip().split()
    str_list = list()
    k = 0
    if len(parts) > 1:
        for i in range(len(parts) - 1):
            parts[i] = parts[i].strip()
            if (len(parts[i]) >= 4 and parts[i][0] in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ' and parts[i][1] == '.' and\
                    parts[i][2] in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ' and parts[i][3] == '.' and
                    parts[i+1][0] in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ') or (parts[i + 1].endswith(',') and parts[i + 1][0] in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'):
                str_list.append(' '.join(parts[k:i + 2]))
                k = i + 2
    str_list.append(' '.join(parts[k:]))
    for j in range(len(str_list)):
        str_list[j] = str_list[j].strip()
        str_list[j] = ' '.join(str_list[j].split())
        if not (str_list[j] in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'):
            str_list[j] = str_list[j].replace(str_list[j].split()[0], str_list[j].split()[0].capitalize())
        if str_list[j].endswith('\n') or str_list[j].endswith(';') or str_list[j].endswith(':') or str_list[j].endswith(','):
            str_list[j] = str_list[j][:-1]
        if str_list[j].startswith('Врио'):
            str_list[j] = str_list[j].replace(str_list[j].split()[0], 'ВРИО')

    return str_list


def table_parsing():
    global prog, subprog, subprog_id, prog_id, main_event_id, code_events, response_obj_id
    response_fio_id = 0
    for row in rows:
        if row[first_column].value is not None:
            if 'государственная программа' in row[first_column].value.lower():
                prog = format_title(row[first_column + 1].value)
                prog_id = Gosprogram.add_new(prog)
                AllEvents.add(prog_id, prog)
                code_events = prog_id
                print(prog)

            if 'подпрограмма' in row[first_column].value.lower():
                subprog = format_title(row[first_column + 1].value)
                subprog_id = format_title(row[first_column].value).split()[1]
                AllEvents.add(subprog_id, subprog)
                Subprogram.add(subprog_id, prog_id, subprog)
                code_events = subprog_id

            if 'основное мероприятие' in row[first_column].value.lower():
                main_event = format_title(row[first_column + 1].value)
                main_event_id = format_title(row[first_column].value).split()[2]
                AllEvents.add(main_event_id, main_event)
                MainEvent.add(main_event_id, subprog_id, main_event)
                code_events = main_event_id
                # print(main_event, main_event_id)
            elif 'мероприятие' in row[first_column].value.lower():
                event = format_title(row[first_column + 1].value)
                event_id = format_title(row[first_column].value).split()[1]
                # subprog_id + '.' +
                AllEvents.add(event_id, event)
                Event.add(event_id, main_event_id, event)
                code_events = event_id

            print(code_events)

            # if 'Ответственный исполнитель' in row[first_column + 2].value:
            #     response_obj = format_title(' '.join(row[first_column + 2].value.split()[3:]))
            #     response_obj_id = ResponseObj.add(response_obj)
            #     print(response_obj)
            #     ResponseMain.add(response_obj_id)
            # else:
            #     response_obj = format_title(' '.join(row[first_column + 2].value.split()[2:]))
            #     # print(response_obj)
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
Subprogram = SPTableArbitrary('subprogram' + year, cur, conn, schema='Employment_Promotion')
MainEvent = SPTableArbitrary('main_event' + year, cur, conn, schema='Employment_Promotion')
Event = SPTableArbitrary('event' + year, cur, conn, schema='Employment_Promotion')
AllEvents = SPTableManyToMany('all_events' + year, cur, conn, schema='Employment_Promotion')
ResponseObj = SPTable('response_obj', cur, conn)
ResponseFio = SPTableArbitrary('response_fio' + year, cur, conn, schema='Employment_Promotion')
EventsResponseObj = SPTableManyToMany('events_response_obj' + year, cur, conn, schema='Employment_Promotion')
EventsResponseFio = SPTableManyToMany('events_response_fio' + year, cur, conn, schema='Employment_Promotion')
# ResponseMain = SPTableArbitrary('response_main' + year, cur, conn, schema='Employment_Promotion')


first_column -= 1
table_parsing()

# 2016 год запарсен без комплекса мероприятий
