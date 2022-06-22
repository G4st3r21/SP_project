from PyScripts.TableClasses.SPTables.SPTableArbitrary import SPTableArbitrary
from PyScripts.TableClasses.SPTables.SPTableManyToMany import SPTableManyToMany
from PyScripts.base.base_functions import parser_init, format_title, partition
from PyScripts.TableClasses.PublicClasses.Gosprogram import Gosprogram
from PyScripts.TableClasses.SPTables.SPTable import SPTable


def commit_all():
    Gosprogram.commit()
    Subprogram.commit()
    MainEvent.commit()
    ResponseObj.commit()
    EventsResponseObj.commit()
    EventsResponseFio.commit()


def format_content(content):
    list_of_content = content.split('\n')
    for i in range(len(list_of_content)):
        list_of_content[i] = format_title(list_of_content[i])

    return list_of_content
                
def part(string):
    # if '-' in string:
    #     if string[string.find('-') + 1] != ' ' and string[string.find('-') - 1] != ' ':
    #         string = string.replace('-', ' ')
    #     else:
    #         string = string.replace('-', '')

    parts = string.replace('\n', ' ').strip().split()
    str_list = list()
    k = 0
    if len(parts) > 1:
        for i in range(len(parts) - 1):
            parts[i] = parts[i].strip()
            if (parts[i + 1].endswith(',') or parts[i + 1].endswith(';')) and \
                    parts[i + 1][0] in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ' and parts[i + 1][1] == '.':
                    # and parts[i + 2][0] in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ' and parts[i + 2][1] != '.':
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
    global prog, subprog, subprog_id, prog_id, main_event_id, code_events
    response_fio_id = 0
    content_id = 1
    for i in range(len(rows)):
        print(i)
        if rows[i][first_column].value is not None and rows[i][first_column + 1].value is not None:
            if 'Государственная программа'.upper() in rows[i][first_column].value:
                prog = rows[i][first_column + 1].value
                prog_id = Gosprogram.add_new(prog)
                AllEvents.add(prog_id, prog)
                code_events = prog_id

            if 'Подпрограмма'.upper() in rows[i][first_column].value:
                subprog = format_title(rows[i][first_column + 1].value)
                subprog_id = format_title(rows[i][first_column].value).split()[1]
                AllEvents.add(subprog_id, subprog)
                Subprogram.add(subprog_id, prog_id, subprog)
                code_events = subprog_id

            if 'Основное мероприятие' in ''.join(rows[i][first_column].value.split('\n')):
                main_event = format_title(rows[i][first_column + 1].value)
                main_event_id = format_title(rows[i][first_column].value).split()[2]
                AllEvents.add(main_event_id, main_event)
                if main_event_id == "10.3":
                    k = 106
                    contents = list()
                    while not rows[k][first_column + 1].value.startswith('Обеспечение'):
                        print(rows[k][first_column + 1].value)
                        contents.append(rows[k][first_column + 1].value)
                        k += 1
                    content = '; '.join(contents)
                else:
                    content = rows[i + 1][first_column + 1].value
                content = " ".join(content.split())
                ContentInResponse.add(content)
                MainEvent.add(main_event_id, subprog_id, ContentInResponse.get_id_by_title(content), main_event)
                code_events = main_event_id
                print(code_events, content)
                # content_id += 1



            response_obj = format_title(rows[i][first_column + 2].value)
            response_obj_id = ResponseObj.add(response_obj)

            fio = part(rows[i][first_column + 3].value)
            for response_fio in fio:
                response_fio_id += 1
                if ResponseFio.add(response_fio_id, response_obj_id, response_fio) is not None \
                        and response_fio_id > int(ResponseFio.add(response_fio_id, response_obj_id, response_fio)):
                    EventsResponseFio.add(code_events,
                                          str(ResponseFio.add(response_fio_id, response_obj_id, response_fio)))
                    print(response_fio)
                    response_fio_id -= 1
                else:
                    EventsResponseFio.add(code_events, response_fio_id)
                    print(response_fio)

            EventsResponseObj.add(code_events, response_obj_id)

        commit_all()


cols, rows, cur, conn = parser_init("2016.xlsx", sheet_number=1, first_str_number=8)
first_column = 2
year = str(2016)

Gosprogram = Gosprogram(cur, conn)
Subprogram = SPTableArbitrary('subprogram' + year, cur, conn, schema='Healthcare')
MainEvent = SPTableArbitrary('main_event' + year, cur, conn, schema='Healthcare')
AllEvents = SPTableManyToMany('all_events' + year, cur, conn, schema='Healthcare')
ResponseObj = SPTable('response_obj', cur, conn)
ResponseFio = SPTableArbitrary('response_fio' + year, cur, conn, schema='Healthcare')
EventsResponseObj = SPTableManyToMany('events_response_obj' + year, cur, conn, schema='Healthcare')
EventsResponseFio = SPTableManyToMany('events_response_fio' + year, cur, conn, schema='Healthcare')
ContentInResponse = SPTable('content_in_response' + year, cur, conn, schema='Healthcare')

first_column -= 1
table_parsing()
