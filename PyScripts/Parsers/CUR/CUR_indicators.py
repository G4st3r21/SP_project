from PyScripts.TableClasses.PublicClasses.GosprogramTasks import GosprogramTasks
from PyScripts.TableClasses.PublicClasses.Gosprogram import Gosprogram
from PyScripts.TableClasses.PublicClasses.GosprogramTarget import GosprogramTarget
from PyScripts.TableClasses.PublicClasses.IndicationsRFTarget import IndicationsRFTarget
from PyScripts.TableClasses.PublicClasses.IndicationsRFVO import IndicationsRFVO
from PyScripts.TableClasses.PublicClasses.GosprogramVO import GosprogramVO
from PyScripts.TableClasses.PublicClasses.BasicTables import BasicTableWithoutSerialType, BasicTable, BasicTable3
from PyScripts.base.base_functions import *


def commit_all():
    CYR.commit()
    GosprogramTasks.commit()
    IndicationsRF.commit()
    Gosprogram.commit()
    IndicationsVO.commit()
    ResponseObj.commit()
    GosprogramVO.commit()


def table_parsing():
    for row in rows:
        if row[0].value is not None:
            gp_id = int(row[1].value)

            cyr = row[2].value.capitalize()
            cyr_id = CYR.add(cyr)

            task = ' '.join(row[3].value.split()[1:])
            task_id = GosprogramTasks.add(cyr_id, task)

            title_rf = row[4].value
            title_rf_id = IndicationsRF.add(task_id, title_rf)

            response = row[7].value
            response_id = ResponseObj.add(response)
            print(response_id)

            title_vo = row[5].value.capitalize()
            prog_id = Gosprogram.add_new(title_vo)
            title_vo_id = IndicationsVO.add(response_id, prog_id)

            IndicationsRFVO.add(title_rf_id, title_vo_id)

            prog_vo_id = GosprogramVO.add(prog_id, response_id, title_rf_id, title_vo_id)
            #
            # target = row[6].value
            # target_id = TargetGosprogramVO.add(target)
            #
            # GosprogramTarget.add(prog_id, target_id)
            #
            # IndicationsRFTarget.add(title_rf_id, target_id)

            commit_all()

            # print(title_prog, response_id, title_rf_id, title_vo_id)


cols, rows, cur, conn = parser_init("ЦУР и ГП ВО_показатели.xlsx", sheet_number=1, first_str_number=6)

CYR = BasicTableWithoutSerialType('cyr', 'title_cyr', cur, conn)
GosprogramTasks = GosprogramTasks(cur, conn)
IndicationsRF = BasicTable3('indications_rf', 'id_task', 'ind_title_rf', cur, conn)
Gosprogram = Gosprogram(cur, conn)
IndicationsVO = BasicTable3('indications_vo', 'id_task', 'id_title_vo', cur, conn)
IndicationsRFVO = IndicationsRFVO(cur, conn)
ResponseObj = BasicTableWithoutSerialType('response_obj', 'response_obj', cur, conn)

GosprogramVO = GosprogramVO(cur, conn)

TargetGosprogramVO = BasicTableWithoutSerialType('target_gosprogram_vo', 'target', cur, conn)
GosprogramTarget = GosprogramTarget(cur, conn)

IndicationsRFTarget = IndicationsRFTarget(cur, conn)

table_parsing()
commit_all()
conn.commit()
