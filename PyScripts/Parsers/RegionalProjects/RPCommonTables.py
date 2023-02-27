import re
from os import listdir
from os.path import isfile, join

from openpyxl import load_workbook
import datetime
from PyScripts.base.base_functions import parser_init, db_conn
from PyScripts.TableClasses.SPTables.SPTable import SPTable
from PyScripts.TableClasses.SPTables.SPTableArbitrary import SPTableArbitrary

cur, conn = db_conn(table_name="All Tables")

FedProject = SPTable('fed_project', cur, conn)
RegProject = SPTableArbitrary('reg_project', cur, conn)
AdditionInRegProject = SPTableArbitrary('addition_in_reg_project', cur, conn)
RegProject2019 = SPTableArbitrary('reg_project2019', cur, conn)
RegProjectsAndGosprogram2019 = SPTableArbitrary('reg_project_and_gosprogram2019', cur, conn)
RegResponseFio2019 = SPTableArbitrary('reg_response_fio2019', cur, conn)
RegProjectsAndResponses2019 = SPTableArbitrary('reg_projects_and_responses2019', cur, conn)

ResponseObj = SPTable('response_obj', cur, conn)


def format_date(input_str):
    # DB format of DATE - YYYY-MM-DD
    given_format = '%d.%m.%Y'  # our format of DATE from doc - dd.mm.YYYY
    dates = input_str.replace(' ', '').split('-')
    start, end = datetime.datetime.strptime(dates[0], given_format).date(), datetime.datetime.strptime(dates[1],
                                                                                                       given_format).date()
    return start, end


def format_title(input_str):
    if '\n' in input_str and input_str[-1] != '\n':
        input_str.replace('\n', ' ')
    elif input_str[-1] == '\n':
        input_str.replace('\n', '')

    if input_str[-1] == '.':
        input_str.replace('.', '')

    return ' '.join(input_str.split())


def get_code(input_str):
    pattern = re.compile("[A-Z][0-9]|[A-Z][A-Z]")  # pardon me but GA ??
    match = re.search(pattern, input_str)
    return match.group() if match else ""


def get_file_names(path):
    return [f for f in listdir(path) if isfile(join(path, f))]


def get_response_obj_id(obj):
    """Returns id of a response object if object exists or adds it and returns id. By i.korn."""
    title_response_obj = ""
    if "департамент" in obj:
        str = obj[obj.find("департамент"):].split(' ')
        str[0] = str[0][:len("департамент")]
        str[0] = str[0][0].upper() + str[0][1:len(str[0])]
        for word in str:
            title_response_obj += (word + " ")
    if "правительств" in obj:
        str = obj[obj.find("правительств"):].split(' ')
        str[0] = str[0][:len("правительств")] + "о"
        str[0] = str[0][0].upper() + str[0][1:len(str[0])]
        for word in str:
            title_response_obj += (word + " ")
    response_obj_id = ResponseObj.get_id_by_title(title_response_obj.strip())
    # ResponseObj.commit()
    if response_obj_id:
        return response_obj_id
    else:
        return None


def get_position(obj):
    """Returns position without object. By i.korn."""
    position = ""
    if "департамент" in obj:
        position = obj[:obj.find("департамент")].strip()
    if "правительств" in obj:
        position = obj[:obj.find("правительств")].strip()
    return position


def fill_fed_project(sheet):
    """Temporary function to fill only FED_PROJECT tables"""
    for row in sheet.iter_rows(min_row=6, max_row=9):
        if row[0].value is not None:
            if 'Наименование федерального проекта' in format_title(row[0].value):
                for j in range(1, len(row)):
                    if row[j].value is not None:
                        title_federal_project = format_title(row[j].value)
                        FedProject.add(title_federal_project)
                        FedProject.commit()


def parse_schemes():
    path = "D:/КСП/Tables/5_Regionalnye_proekty/5_Региональные проекты/Сравнительная таблица региональных проектов.xlsx"
    wb = load_workbook(path)
    sheet = wb.active
    schemes_dict = {}
    scheme_code = ""
    for row in sheet.iter_rows():
        if row[0].value is not None:
            if "Код" in row[0].value:
                scheme_code = row[1].value
            if "Схема" in row[0].value and scheme_code != "":
                schemes_dict[scheme_code] = row[1].value
    return schemes_dict


def fill_reg_project(sheet, code, schema):
    """Fills REG_PROJECT and FED_PROJECT tables"""
    title = format_title(sheet['A6'].value)
    for row in sheet.iter_rows(max_row=14):
        if row[0].value is not None:
            if 'Наименование федерального проекта' in format_title(row[0].value):
                for j in range(1, len(row)):
                    if row[j].value is not None:
                        title_federal_project = format_title(row[j].value)
                        id_fed_project = FedProject.add(title_federal_project)
                        FedProject.commit()
            if 'Краткое наименование регионального проекта' in format_title(row[0].value):
                for j in range(1, len(row)):
                    if row[j].value is not None:
                        if 'Срок начала и окончания проекта' in format_title(row[j].value):
                            for k in range(j + 1, len(row)):
                                if row[k].value is not None:
                                    dates = format_date(row[k].value)
                                    start_date, end_date = dates[0], dates[1]
                            break
                        else:
                            print(row[j].value)
                            short_title = row[j].value

    RegProject.add(code, id_fed_project, title, short_title, start_date, end_date, schema)
    RegProject.commit()


def fill_addition_in_reg_project(sheet, code_project):
    """Fills ADDITION_IN_REG_PROJECT table"""
    additional_info_title = False
    addition = ""
    for row in sheet.iter_rows():
        if row[0].value is not None:
            if "6. Дополнительная информация" in format_title(row[0].value):
                additional_info_title = True
                continue
            if "ПЛАН" in format_title(row[0].value) \
                    or "МЕТОДИКА" in format_title(row[0].value):
                additional_info_title = False
                break
            if additional_info_title:
                to_add = format_title(row[0].value)
                if not to_add.isnumeric():
                    if addition != "":
                        addition += " " + to_add
                    else:
                        addition += to_add
    if addition != "":
        AdditionInRegProject.add(code_project, addition)
        AdditionInRegProject.commit()


def fill_reg_response_fio2019(sheet):
    """Fills REG_RESPONSE_FIO2019 table. By i.korn."""
    for row in sheet.iter_rows(min_row=8, max_row=13):
        if "Куратор регионального проекта" in format_title(row[0].value) \
                or "Руководитель регионального проекта" in format_title(row[0].value) \
                or "Администратор регионального проекта" in format_title(row[0].value):
            for j in range(1, len(row)):
                if row[j].value is not None:
                    response_obj_id = get_response_obj_id(row[j].value.split(", ")[1])
                    reg_response_fio = row[j].value.split(", ")[0]
                    position = get_position(row[j].value.split(", ")[1])
                    if response_obj_id and position:
                        RegResponseFio2019.add(response_obj_id, reg_response_fio, position)
                        RegResponseFio2019.commit()
                    break


def fill_reg_project2019(sheet, code):
    """Fills REG_PROJECT2019 table"""
    # if 'Куратор регионального проекта' in format_title(row[0].value):
    #     kur = format_response(row[8].value)
    #     kurator_fio, kurator_position = kur[0], kur[1]
    # if 'Руководитель регионального проекта' in format_title(row[0].value):
    #     man = format_response(row[8].value)
    #     manager_fio, manager_position = man[0], man[1]
    # if 'Администратор регионального проекта' in format_title(row[0].value):
    #     adm = format_response(row[8].value)
    #     administrator_fio, administrator_position = adm[0], adm[1]
    curator_id = RegResponseFio2019.get_id_by_title(sheet['I10'].value.split(', ')[0])
    manager_id = RegResponseFio2019.get_id_by_title(sheet['I11'].value.split(', ')[0])
    administrator_id = RegResponseFio2019.get_id_by_title(sheet['I12'].value.split(', ')[0])
    RegResponseFio2019.add(code, curator_id, manager_id, administrator_id)
    RegResponseFio2019.commit()


def fill_reg_projects_and_responses2019(sheet):
    """Fills REG_PROJECTS_AND_RESPONSES2019 table"""
    for row in sheet.iter_rows():
        if "Участники регионального проекта" in row[0].value:
            while row[0].value is not None:
                code_reg_project = 1
                id_response_fio = 1
                role_in_reg_project = ""
                direct_supervisor_id = 1
                employment_percents = 0.50
                RegProjectsAndResponses2019.add(code_reg_project, id_response_fio, role_in_reg_project,
                                                direct_supervisor_id, employment_percents)
                RegProjectsAndResponses2019.commit()


def fill_reg_project_and_gosprogram2019(sheet):
    """Fills REG_PROJECT_AND_GOSPROGRAM2019 table"""


path = "D:/КСП/Tables/5_Regionalnye_proekty/5_Региональные проекты/2019 паспорта по состоянию на 23.12.2019"
files = get_file_names(path)

for f in files:
    code = get_code(f)
    full_path = path + "/" + f
    wb = load_workbook(full_path)

    fill_reg_response_fio2019(wb.active)
    print(code, "file is loaded to database")
