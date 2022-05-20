from PyScripts.TableClasses.PublicClasses.SPTableArbitrary import SPTableArbitrary
from PyScripts.TableClasses.PublicClasses.SPTableManyToMany import SPTableManyToMany
from PyScripts.base.base_functions import parser_init, format_title, partition
from PyScripts.TableClasses.PublicClasses.Gosprogram import Gosprogram
from PyScripts.TableClasses.PublicClasses.SPTable import SPTable


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

            response_obj = format_title(row[first_column + 2].value)
            response_obj_id = ResponseObj.add(response_obj)

            fio = partition(format_title(row[first_column + 3].value))
            for response_fio in fio:
                response_fio_id += 1
                if response_fio_id > int(ResponseFio.add(response_fio_id, response_obj_id, response_fio)):
                    EventsResponseFio.add(code_events,
                                          str(ResponseFio.add(response_fio_id, response_obj_id, response_fio)))
                    response_fio_id -= 1
                else:
                    EventsResponseFio.add(code_events, response_fio_id)

            EventsResponseObj.add(code_events, response_obj_id)

        commit_all()


cols, rows, cur, conn = parser_init("8. Ответственные.xlsx", sheet_number=1, first_str_number=10)
first_column = 1
first_column -= 1

Gosprogram = Gosprogram(cur, conn)
Subprogram = SPTableArbitrary('subprogram2020', 'title_subprog', cur, conn, schema='Available_Environment')
MainEvent = SPTableArbitrary('main_event2020', 'main_event', cur, conn, schema='Available_Environment')
Event = SPTableArbitrary('event2020', 'event', cur, conn, schema='Available_Environment')
AllEvents = SPTableManyToMany('all_events2020', cur, conn, schema='Available_Environment')
ResponseObj = SPTable('response_obj', 'response_obj', cur, conn)
ResponseFio = SPTableArbitrary('response_fio2020', 'fio', cur, conn, schema='Available_Environment')
EventsResponseObj = SPTableManyToMany('events_response_obj2020', cur, conn, schema='Available_Environment')
EventsResponseFio = SPTableManyToMany('events_response_fio2020', cur, conn, schema='Available_Environment')

table_parsing()
