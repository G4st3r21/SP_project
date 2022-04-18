from PyScripts.Parsers.CUR.CYR_indicators import format_title
from PyScripts.TableClasses.PublicClasses.GosprogramTasks import GosprogramTasks
from PyScripts.TableClasses.PublicClasses.Gosprogram import Gosprogram
from PyScripts.TableClasses.PublicClasses.GosprogramTarget import GosprogramTarget
from PyScripts.TableClasses.PublicClasses.IndicationsRFTarget import IndicationsRFTarget
from PyScripts.TableClasses.PublicClasses.GosprogramVO import GosprogramVO
from PyScripts.TableClasses.PublicClasses.BasicTables import BasicTableWithoutSerialType, BasicTable, BasicTable3
from PyScripts.base.base_functions import *


def commit_all():
    CYR.commit()
    GosprogramTasks.commit()
    IndicationsRF.commit()
    Gosprogram.commit()
    GosprogramVO.commit()
    TargetGosprogramVO.commit()
    GosprogramTarget.commit()
    IndicationsRFTarget.commit()

def table_parsing():
    for row in rows:
        if row[0].value is not None:
            cyr = format_title(row[2].value)
            cyr_id = CYR.add(cyr)

            task = format_title(' '.join(row[3].value.split()[1:]))
            task_id = GosprogramTasks.add(cyr_id, task)

            prog = format_title(row[4].value)
            prog_id = Gosprogram.add_new(prog)

            target = row[5].value
            commit_all()
            if target[0] == '1':
                for value_part in target.split('\n'):
                    target_id = TargetGosprogramVO.add(' '.join(value_part.split()[1:]))

                    GosprogramTarget.add(prog_id, target_id)

                    ind_rf_id = IndicationsRF.find_all_by_task_id(task_id)

                    if ind_rf_id:
                        for obj in ind_rf_id:
                            IndicationsRFTarget.add(obj[0], target_id)
            else:
                target_id = TargetGosprogramVO.add(target)
                GosprogramTarget.add(prog_id, target_id)

                ind_rf_id = IndicationsRF.find_all_by_task_id(task_id)
                if ind_rf_id:
                    for obj in ind_rf_id:
                        temp_id = IndicationsRFTarget.add(obj[0], target_id)

cols, rows, cur, conn = parser_init("ЦУР и ГП ВО_цели.xlsx", sheet_number=1, first_str_number=6)

CYR = BasicTableWithoutSerialType('cyr', 'title_cyr', cur, conn)
GosprogramTasks = GosprogramTasks(cur, conn)
IndicationsRF = BasicTable3('indications_rf', 'id_task', 'ind_title_rf', cur, conn)
Gosprogram = Gosprogram(cur, conn)

GosprogramVO = GosprogramVO(cur, conn)

TargetGosprogramVO = BasicTableWithoutSerialType('target_gosprogram_vo', 'target', cur, conn)
GosprogramTarget = GosprogramTarget(cur, conn)

IndicationsRFTarget = IndicationsRFTarget(cur, conn)

table_parsing()
commit_all()
conn.commit()