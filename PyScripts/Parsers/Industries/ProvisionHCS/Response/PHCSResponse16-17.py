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

def table_parsing():
    global prog, subprog, subprog_id, prog_id, main_event_id, code_events
    response_fio_id = 0
    for row in rows:
        if row[first_column].value is not None:
            if 'Государственная программа' in row[first_column].value:
                prog = row[first_column + 1].value
                prog_id = Gosprogram.add_new(prog)
                AllEvents.add(prog_id, prog)
                code_events = prog_id

            if 'Подпрограмма' in row[first_column].value:
                subprog = format_title(row[first_column + 1].value)
                subprog_id = format_title(row[first_column].value).split()[1]
                AllEvents.add(subprog_id, subprog)
                Subprogram.add(subprog_id, prog_id, subprog)
                code_events = subprog_id

            if 'Основное мероприятие' in ''.join(row[first_column].value.split('\n')):
                main_event = format_title(row[first_column + 1].value)
                main_event_id = format_title(row[first_column].value).split()[2]
                AllEvents.add(main_event_id, main_event)
                MainEvent.add(main_event_id, subprog_id, main_event)
                code_events = main_event_id

            response_obj = format_title(row[first_column + 2].value)
            response_obj_id = ResponseObj.add(response_obj)

            fio = partition(format_title(row[first_column + 3].value))
            for response_fio in fio:
                response_fio_id += 1
                if ResponseFio.add(response_fio_id, response_obj_id, response_fio) is not None:
                    EventsResponseFio.add(code_events,
                                          str(ResponseFio.add(response_fio_id, response_obj_id, response_fio)))
                    print(response_fio)
                    response_fio_id -= 1
                else:
                    EventsResponseFio.add(code_events, response_fio_id)
                    print(response_fio)

            EventsResponseObj.add(code_events, response_obj_id)

        commit_all()


cols, rows, cur, conn = parser_init("8. Ответственные и 9. Показатели.xlsx", sheet_number=1, first_str_number=9)
first_column = 2
year = str(2017)

Gosprogram = Gosprogram(cur, conn)
Subprogram = SPTableArbitrary('subprogram' + year, cur, conn, schema='Provision_HCS')
MainEvent = SPTableArbitrary('main_event' + year, cur, conn, schema='Provision_HCS')
AllEvents = SPTableManyToMany('all_events' + year, cur, conn, schema='Provision_HCS')
ResponseObj = SPTable('response_obj', cur, conn)
ResponseFio = SPTableArbitrary('response_fio' + year, cur, conn, schema='Provision_HCS')
EventsResponseObj = SPTableManyToMany('events_response_obj' + year, cur, conn, schema='Provision_HCS')
EventsResponseFio = SPTableManyToMany('events_response_fio' + year, cur, conn, schema='Provision_HCS')

first_column -= 1
table_parsing()
