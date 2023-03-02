from base_functions_RP import get_file_names, get_code, format_title

from openpyxl import load_workbook
from PyScripts.base.base_functions import db_conn
from PyScripts.TableClasses.SPTables.SPTableArbitrary import SPTableArbitrary

cur, conn = db_conn(table_name="All Tables")
RegPassportAims = SPTableArbitrary('reg_passport_aims', cur, conn)


def fill_reg_passport_aims(sheet, code):
    passport_aim = ""
    aim_and_indicators = False
    for row in sheet.iter_rows(max_row=22):
        if row[0].value is not None:
            if "2. Цель и показатели регионального проекта" in format_title(row[0].value):
                aim_and_indicators = True
                continue
            if aim_and_indicators:
                passport_aim = format_title(row[0].value)
                break
    if passport_aim:
        RegPassportAims.add(code, passport_aim)
        RegPassportAims.commit()


path = "D:/КСП/Tables/5_Regionalnye_proekty/5_Региональные проекты/2019 паспорта по состоянию на 23.12.2019"
files = get_file_names(path)

for f in files:
    code = get_code(f)

    full_path = path + "/" + f
    wb = load_workbook(full_path)

    fill_reg_passport_aims(wb.active, code)
    print(code, "file is loaded to database")
