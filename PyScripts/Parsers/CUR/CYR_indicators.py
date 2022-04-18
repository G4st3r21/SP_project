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

def format_title(str):
    if '\n' in str and str[-1] != '\n':
        str.replace('\n', ' ')
    elif str[-1] == '\n':
        str.replace('\n', '')

    if str[-1] == '.':
        str.replace('.', '')

    # str[0].capitalize()

    return ' '.join(str.split())

def table_parsing():
    for row in rows:
        if row[0].value is not None:
            gp_id = int(row[1].value)

            cyr = format_title(row[2].value)
            cyr_id = CYR.add(cyr)

            task = format_title(' '.join(row[3].value.split()[1:]))
            task_id = GosprogramTasks.add(cyr_id, task)

            ind_rf = format_title(row[4].value)
            ind_rf_id = IndicationsRF.add(task_id, ind_rf)

            response = format_title(row[7].value)
            response_id = ResponseObj.add(response)

            prog = format_title(row[5].value)
            prog_id = Gosprogram.add_new(prog)

            ind_vo = format_title(row[6].value)
            ind_vo_id = IndicationsVO.add(response_id, ind_vo)

            IndicationsRFVO.add(ind_rf_id, ind_vo_id)

            prog_vo_id = GosprogramVO.add(prog_id, response_id, ind_rf_id, ind_vo_id)

            commit_all()


cols, rows, cur, conn = parser_init("ЦУР и ГП ВО_показатели.xlsx", sheet_number=1, first_str_number=6)
Gosprogram = Gosprogram(cur, conn)

CYR = BasicTableWithoutSerialType('cyr', 'title_cyr', cur, conn)
GosprogramTasks = GosprogramTasks(cur, conn)
IndicationsRF = BasicTable3('indications_rf', 'id_task', 'ind_title_rf', cur, conn)
IndicationsVO = BasicTable3('indications_vo', 'id_task', 'ind_title_vo', cur, conn)
IndicationsRFVO = IndicationsRFVO(cur, conn)
ResponseObj = BasicTableWithoutSerialType('response_obj', 'response_obj', cur, conn)

GosprogramVO = GosprogramVO(cur, conn)

table_parsing()
commit_all()
conn.commit()
