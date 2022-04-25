from PyScripts.TableClasses.PublicClasses.GosprogramTasks import GosprogramTasks
from PyScripts.TableClasses.PublicClasses.Gosprogram import Gosprogram
from PyScripts.TableClasses.PublicClasses.GosprogramTarget import GosprogramTarget
from PyScripts.TableClasses.PublicClasses.IndicationsRFTarget import IndicationsRFTarget
from PyScripts.TableClasses.PublicClasses.GosprogramVO import GosprogramVO
from PyScripts.TableClasses.PublicClasses.BasicTables import BasicTableWithoutSerialType, BasicTable, BasicTable3
from PyScripts.base.base_functions import *


def commit_all():
    TargetGosprogramVO.commit()
    GosprogramTarget.commit()
    IndicationsRFTarget.commit()


def table_parsing():
    for row in rows:
        if row[0].value is not None:
            cyr = row[2].value.capitalize()
            cyr_id = CYR.get_id_by_name(cyr)

            task = ' '.join(row[3].value.split()[1:])
            task_id = GosprogramTasks.get_id_by_name(task)

            title_vo = row[4].value
            print(title_vo)
            prog_id = Gosprogram.find_id_by_name(title_vo)

            target = row[5].value
            target_id = TargetGosprogramVO.add(target)

            GosprogramTarget.add(prog_id, target_id)

            # title_rf_id = IndicationsRF.find_id_by_name1(task_id)

            # title_rf_id =

            # IndicationsRFTarget.add(title_rf_id, target_id)
            # print(title_rf_id, target_id)
            commit_all()

            # print(title_prog, response_id, title_rf_id, title_vo_id)


cols, rows, cur, conn = parser_init("ЦУР и ГП ВО_цели.xlsx", sheet_number=1, first_str_number=6)

CYR = BasicTableWithoutSerialType('cyr', 'title_cyr', cur, conn)
GosprogramTasks = GosprogramTasks(cur, conn)
IndicationsRF = BasicTable3('indications_rf', 'id_task', 'ind_title_rf', cur, conn)
Gosprogram = Gosprogram(cur, conn)
IndicationsVO = BasicTable3('indications_vo', 'id_task', 'id_title_vo', cur, conn)
ResponseObj = BasicTableWithoutSerialType('response_obj', 'response_obj', cur, conn)

GosprogramVO = GosprogramVO(cur, conn)

TargetGosprogramVO = BasicTableWithoutSerialType('target_gosprogram_vo', 'target', cur, conn)
GosprogramTarget = GosprogramTarget(cur, conn)

IndicationsRFTarget = IndicationsRFTarget(cur, conn)

table_parsing()
commit_all()
conn.commit()
