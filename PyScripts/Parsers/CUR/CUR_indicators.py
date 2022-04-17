from PyScripts.TableClasses.PublicClasses.GosprogramTasks import GosprogramTasks
from PyScripts.TableClasses.PublicClasses.Gosprogram import Gosprogram
from PyScripts.TableClasses.PublicClasses.BasicTables import BasicTableWithoutSerialType, BasicTable
from PyScripts.base.base_functions import *

def commit_all():
    pass

def table_parsing():
    for row in rows:
        if row[0].value is not None:
            gp_id = int(row[1].value)

            cyr = row[2].value.capitalize()
            cyr_id = CYR.add(cyr)

            task = ' '.join(row[3].value.split()[1:])
            task_id = GosprogramTasks.add(cyr_id, task)

            title_rf = row[4].value
            title_rf_id = TitleRF.add(task_id, title_rf)

            response = row[7].value
            response_id = ResponseObj.add(response)

            prog_id = Gosprogram.

            title_vo = row[5].value
            title_vo_id = TitleVO.add(response_id, title_vo)


cols, rows, cur, conn = parser_init("ЦУР и ГП ВО_показатели.xlsx", sheet_number=1, first_str_number=6)
CYR = BasicTableWithoutSerialType('cyr', 'title_cyr', cur, conn)
GosprogramTasks = BasicTableWithoutSerialType('gosprogram_tasks', 'task', cur, conn)
Gosprogram = Gosprogram(cur, conn)
ResponseObj = BasicTableWithoutSerialType('response_obj', 'response_obj', cur, conn)
GosprogramAndTasks = GosprogramTasks(cur, conn)
table_parsing()
commit_all()
