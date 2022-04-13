from PyScripts.base.base_functions import *
from PyScripts.TableClasses.PublicClasses.BasicTables import BasicTableWithoutSerialType, BasicTable
from PyScripts.TableClasses.PublicClasses.Events import AllEvents
from PyScripts.TableClasses.PublicClasses.Gosprogram import Gosprogram


def cell_gp_fin_parsing(cell):
    strk = cell.value
    if strk is None:
        return 'Null', 'Null'
    if 'региональный проект' in strk.lower():
        gp_names = 'См. "План мероприятий(т. №3)" ячейка ' + str(
            cell.coordinate)

        return gp_names, 'Null'
    if '"' in strk:
        gp_names = strk.split('"')
        fin_source = 'федеральный бюджет, областной бюджет' if 'федеральный бюджет' in strk.lower() \
                                                               and 'областной бюджет' in strk.lower() else \
            'областной бюджет' if 'областной бюджет' in strk.lower() else \
                'федеральный бюджет' if 'федеральный бюджет' in strk.lower() else 'Null'
        gp_names = '; '.join([gp_name for gp_name in gp_names[1:-1:2] if len(gp_name) > 3]) if len(gp_names) > 3 else \
        gp_names[1]

        return gp_names, fin_source.replace('\n', ' ').lower()
    if 'Государственные программы,' in strk:
        fin_source = 'федеральный бюджет, областной бюджет' if 'федеральный бюджет' in strk.lower() \
                                                               and 'областной бюджет' in strk.lower() else \
            'областной бюджет' if 'областной бюджет' in strk.lower() else \
                'федеральный бюджет' if 'федеральный бюджет' in strk.lower() else 'Null'
        gp_names = strk if 'бюджет' not in strk else ','.join([i for i in strk.split(',') if 'бюджет' not in i])

        return gp_names, fin_source.replace('\n', ' ').lower()

    return 'Null', strk.replace('\n', ' ').lower()


def commit_all():
    ResponseObj.commit()
    ImplementationPeriod.commit()
    ExpectedResult.commit()
    FinancingSource.commit()
    AllEvents.commit()
    Gosprogram.commit()


def table_parsing():
    _ = 0
    for row in rows:
        if str(row[0].value)[:2] == 'СЦ':
            id_sub_aim = str(row[0].value).split()[0]
            id_sub_aim = id_sub_aim[:-1] if id_sub_aim[-1] == '.' else id_sub_aim
        else:
            id_event = str(row[1].value).split()[0]
            id_event = id_event[:-1] if id_event[-1] == '.' else id_event
            event = " ".join(str(row[1].value).split()[1:])

            period_id = ImplementationPeriod.add_new(row[2].value)

            result_id = ExpectedResult.add_new(row[3].value)

            gp_name, fin_source = cell_gp_fin_parsing(row[4])
            gp_id = Gosprogram.add_new(gp_name) if gp_name != 'null' else 'Null'
            fin_source_id = FinancingSource.add_new(fin_source) if fin_source != 'null' else 'Null'

            response_obj = [obj.capitalize() for obj in str(row[5].value).split(';\n')]
            AllEvents.add_new(id_event, id_sub_aim, period_id, result_id, fin_source_id, gp_id, event)

            commit_all()

            for r_obj in response_obj:
                r_obj_id = ResponseObj.add_new(r_obj)
                print(id_event, r_obj_id)
                print(AllEvents.get_all_by_id(id_event))
                # cur.execute(f"INSERT INTO public.events_and_response_obj VALUES ('{id_event}', {r_obj_id})")
                print("отладочный принт")

            print(_)
            _ += 1


cols, rows, cur, conn = parser_init("План мероприятий.xlsx", sheet_number=3, first_str_number=2)
ResponseObj = BasicTableWithoutSerialType('response_obj', 'response_obj', cur, conn)
ImplementationPeriod = BasicTableWithoutSerialType('implementation_period', 'period', cur, conn)
ExpectedResult = BasicTable('expected_result', 'result', cur, conn)
FinancingSource = BasicTableWithoutSerialType('financing_source', 'source', cur, conn)
AllEvents = AllEvents(cur, conn)
Gosprogram = Gosprogram(cur, conn)
table_parsing()
commit_all()
conn.commit()
