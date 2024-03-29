from PyScripts.TableClasses.PublicClasses.BasicTables import BasicTableWithoutSerialType
from PyScripts.TableClasses.SPTables.SPTable import SPTable
from PyScripts.base.base_functions import *
from PyScripts.TableClasses.PublicClasses.GrowthPoints import GrowthPoint
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
    Gosprogram.commit()
    GrowthPointNames.commit()
    GrowthPoint.commit()


def cell_task_id_parsing(cell):
    value = cell.value if cell.value[-1] != '.' else cell.value[:-1]
    if "3" in value[0]:
        value = 'З' + value[1:]
    if "З" in value:
        sub_aim_id = [i for i in value[1:].split(".")[:-1]]
        sub_aim_id = "СЦ" + '.'.join(sub_aim_id)
        sub_aim_id = sub_aim_id if sub_aim_id[-1] != '.' else sub_aim_id[:-1]
        return sub_aim_id, value
    elif "СЦ" in value:
        sub_aim_id = cell.value if cell.value[-1] != '.' else cell.value[:-1]
        return sub_aim_id, 0


def table_parsing():
    for row in rows:
        if 'Точка роста' in str(row[0].value):
            growth_point = str(row[0].value).split('"')[1]
            growth_point_id = GrowthPointNames.add(growth_point)
        else:
            if row[0].value is not None:
                id_sub_aim, id_task = cell_task_id_parsing(row[0])
            id_event = str(growth_point_id) + '.' + str(row[1].value).split()[0]
            id_event = id_event[:-1] if id_event[-1] == '.' else id_event
            event = " ".join(str(row[1].value).split()[1:])

            period_id = ImplementationPeriod.add(row[2].value)

            result_id = ExpectedResult.add(row[3].value) if row[2].value != 'null' else ExpectedResult.add(
                'Null')

            gp_name, fin_source = cell_gp_fin_parsing(row[4])
            gp_id = Gosprogram.add_new(gp_name) if gp_name != 'null' else Gosprogram.add_new('Null')
            fin_source_id = FinancingSource.add(fin_source) if fin_source != 'null' else FinancingSource.add(
                'Null')

            response_obj = [obj.capitalize() for obj in str(row[5].value).split(';\n')]
            GrowthPoint.add_new(id_event, id_sub_aim, id_task, period_id, result_id, fin_source_id, gp_id, event)

            print('коммит')
            commit_all()
            for r_obj in response_obj:
                r_obj_id = ResponseObj.add(r_obj)
                cur.execute(f"INSERT INTO public.GROWTH_POINT_AND_RESPONSE_OBJ VALUES ('{id_event}', {r_obj_id})")


cols, rows, cur, conn = parser_init("План мероприятий.xlsx", 5, 3)
ResponseObj = BasicTableWithoutSerialType('response_obj', 'response_obj', cur, conn)
ImplementationPeriod = BasicTableWithoutSerialType('implementation_period', 'period', cur, conn)
ExpectedResult = SPTable('expected_result', cur, conn)
FinancingSource = BasicTableWithoutSerialType('financing_source', 'source', cur, conn)
GrowthPointNames = SPTable('growth_point_names', cur, conn)
Gosprogram = Gosprogram(cur, conn)
GrowthPoint = GrowthPoint(cur, conn)
table_parsing()
commit_all()
conn.commit()
