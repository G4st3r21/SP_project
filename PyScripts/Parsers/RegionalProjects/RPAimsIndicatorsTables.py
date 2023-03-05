from base_functions_RP import get_file_names, get_code, format_title

from openpyxl import load_workbook
from PyScripts.base.base_functions import db_conn
from PyScripts.TableClasses.SPTables.SPTable import SPTable
from PyScripts.TableClasses.SPTables.SPTableArbitrary import SPTableArbitrary

cur, conn = db_conn(table_name="All Tables")
RegProject = SPTableArbitrary('reg_project', cur, conn)


def fill_reg_passport_aims(sheet, code_reg_project):
    """Fills reg_passport_aims table"""
    RegPassportAims = SPTableArbitrary('reg_passport_aims', cur, conn)
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
        RegPassportAims.add(code_reg_project, passport_aim)  # serial
        RegPassportAims.commit()


def fill_fed_indicators2019(sheet, code):
    """Fills fed_indicators2019 table"""
    FedIndicators2019 = SPTableArbitrary('fed_indicators2019', cur, conn)
    args_dict = {'code': code}
    id_fed_project = RegProject.get_by_custom_filter_expression(args_dict)[0][1]
    title_indicators = []
    first_aim_and_indicators = False
    for row in sheet.iter_rows():
        if row[0].value is not None:
            if "2. Цель и показатели регионального проекта" in format_title(row[0].value):
                first_aim_and_indicators = True
                continue
            if first_aim_and_indicators:
                first_aim_and_indicators = False
                continue
            if "3. Результаты регионального проекта" in format_title(row[0].value):
                break
            if "№ п/п" not in format_title(row[0].value):
                # todo: define what is fed indicator and what isn't
                title_indicators.append(format_title(row[0].value))
    if title_indicators[0]:
        print(id_fed_project, title_indicators)
        FedIndicators2019.add(id_fed_project, title_indicators[0])  # serial
        FedIndicators2019.commit()


def fill_reg_aims_indicators_names2019():
    """Fills reg_aims_indicators_names2019 table"""
    RegAimsIndicatorsNames2019 = SPTableArbitrary('reg_aims_indicators_names2019', cur, conn)


def fill_types_of_indicators():
    """Fills types_of_indicators table"""
    TypesOfIndicators = SPTable('types_of_indicators', cur, conn)
    # todo: find out if there's another types of indicators
    TypesOfIndicators.add("Дополнительный показатель")
    TypesOfIndicators.commit()
# fill_types_of_indicators()


def fill_dynamics():
    """Fills dynamics table"""


def fill_indicators_comments2019():
    """Fills indicators_comments2019 table for each individual schema"""


def fill_indicators_additional_comments2019():
    """Fills indicators_additional_comments2019 table for each individual schema"""


def fill_reg_aims_indicators2019():
    """Fills reg_aims_indicators2019 table for each individual schema"""


def fills_reg_indicators_passport_values2019():
    """Fills reg_indicators_passport_values2019 for each individual schema"""


path = "D:/КСП/Tables/5_Regionalnye_proekty/5_Региональные проекты/2019 паспорта по состоянию на 23.12.2019"
files = get_file_names(path)

for f in files:
    code = get_code(f)
    if code == 'A2':
        full_path = path + "/" + f
        wb = load_workbook(full_path)

        fill_fed_indicators2019(wb.active, code)
        print(code, "file is loaded to database")
