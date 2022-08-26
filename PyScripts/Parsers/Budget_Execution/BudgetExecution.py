from PyScripts.TableClasses.SPTables.SPTableArbitrary import SPTableArbitrary
from PyScripts.TableClasses.SPTables.SPTableManyToMany import SPTableManyToMany
from PyScripts.base.base_functions import parser_init


def commit_all():
    GRBS.commit()
    RZ.commit()
    PR.commit()
    SR.commit()
    CSR.commit()
    VR.commit()
    GosprogramSR.commit()
    SubprogramSR.commit()
    MainEventSR.commit()
    SRProg.commit()


def format_code(cd):
    if len(cd) == 1:
        return '0' + cd
    return cd


def format_title(title, com):
    title = str(title)
    title = title.replace('\xa0', ' ')
    title = title.replace('\n', ' ')
    if com == 'prog' and title is not None and title.find('«') != -1:
        title = title[title.index('«') + 1:title.index('»')]
    if com == 'csr' and title is not None:
        for sym in range(1, len(title)):
            if title[sym - 1] == '(' and title[sym] in 'АБВГДЕËЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ' and (title[sym] != 'Е' and title[sym + 1] != 'Г'):
                title = title[:sym - 1]
                break
    if com == 'vr' and title is not None:
        for sym in range(1, len(title)):
            if title[sym - 1] == '(' and title[sym] in 'АБВГДЕËЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ' and (title[sym] != 'Е' and title[sym + 1] != 'Г'):
                title = title[sym:-1]
                break
    return title


def str_to_float(s):
    if s == '' or s is None or s == ' ' or s == '\xa0':
        return float(0)
    s = ''.join(str(s).split())
    s = s.replace(',', '.')
    return float(s)


def create_prog_dict():
    prog_dict = {}
    for row in rows_p:
        if row[first_column].value is not None or row[first_column].value != ' ' and row[first_column + 2].value is not None:
            kbk = ''.join(row[first_column + 2].value.split())[:5]
            id_prog = str(row[first_column].value)
            prog = format_title(row[first_column + 1].value, 'prog')
            if id_prog != '\xa0':
                prog_dict[kbk] = [id_prog, prog]
    return prog_dict


# def prog_parsing():
#     for row in rows_p:
#         if row[first_column].value is not None:
#             sr_kbk = ''.join(row[first_column + 2].value.split())[:5]
#             if sr_kbk[-3] == '0' and sr_kbk[-2] == '0' and sr_kbk[-1] == '0':
#                 gosprogram = format_title(row[first_column + 1].value, 'prog')
#                 code_gosprogram = row[first_column].value
#                 SRProg.add(sr_kbk[-5:], code_gosprogram)
#                 GosprogramSR.add(sr_kbk[-5:], str(code_gosprogram), gosprogram)
#                 prog_kbk = sr_kbk[-5:]
#             elif sr_kbk[-2] == '0' and sr_kbk[-1] == '0':
#                 subprogram = format_title(row[first_column].value, 'prog')
#                 code_subprogram = row[first_column].value
#                 SRProg.add(sr_kbk[-5:], code_subprogram)
#                 SubprogramSR.add(sr_kbk[-5:], code_subprogram, prog_kbk, subprogram)
#                 subprog_kbk = sr_kbk[-5:]
#             else:
#                 main_event = format_title(row[first_column].value, 'prog')
#                 code_main_event = row[first_column].value
#                 SRProg.add(sr_kbk[-5:], code_main_event)
#                 MainEventSR.add(sr_kbk[-5:], code_main_event, subprog_kbk, main_event)
#                 main_event_kbk = sr_kbk[-5:]


def table_parsing():
    prog_dict = create_prog_dict()
    cnt = 0
    grbs_kbk = '808'
    # pr_kbk = '821.0909'
    # sr_kbk = '821.0909.019N7'
    # code = '1.9.2'
    for row in rows_v:
        cnt += 1
        print(cnt)
        if cnt >= 1:
            for index in range(1, 6):
                if row[index].value is not None and row[index].value != '\xa0' and row[index].value != ' ':
                    if index == 1 and (row[index + 1].value is None or row[index + 1].value == '\xa0' or row[index + 1].value == ' '):
                        grbs_kbk = str(row[index].value)
                        grbs_title = str(row[first_column].value).replace('\n', '')
                        grbs_title = grbs_title.replace('\xa0', ' ')
                        if GRBS.get_by_tuple(grbs_kbk, grbs_title) is False or GRBS.get_by_tuple(grbs_kbk, grbs_title) is None:
                            GRBS.add(grbs_kbk, grbs_title)
                        print('g')
                    elif index == 2 and (row[index + 1].value is None or row[index + 1].value == '\xa0' or row[index + 1].value == ' '):
                        rz_kbk = grbs_kbk + '.' + format_code(str(row[index].value))
                        rz_title = row[first_column].value
                        RZ.add(rz_kbk, grbs_kbk, rz_title)
                        print('r')
                    elif index == 3 and (row[index + 1].value is None or row[index + 1].value == '\xa0' or row[index + 1].value == ' '):
                        pr_kbk = rz_kbk + format_code(str(row[index].value))
                        pr_title = row[first_column].value
                        PR.add(pr_kbk, rz_kbk, pr_title)
                        print('p')
                    elif index == 4 and (row[index + 1].value is None or row[index + 1].value == '\xa0' or row[index + 1].value == ' '):
                        sr_kbk = pr_kbk + '.' + ''.join(row[index].value.split())[:5]
                        if prog_dict.get(sr_kbk[9:]) is None or prog_dict[sr_kbk[9:]][0] == '' or prog_dict[sr_kbk[9:]][0] == ' ' or prog_dict[sr_kbk[9:]][0] is None:
                            code = 'Null'
                        else:
                            code = prog_dict[sr_kbk[9:]][0]
                        # print(code, prog_dict[sr_kbk[9:]][1])
                        program = format_title(row[first_column].value, 'prog')
                        if sr_kbk[-3] == '0' and sr_kbk[-2] == '0' and sr_kbk[-1] == '0':
                            prog_kbk = sr_kbk[9:]
                            SRProg.add(prog_kbk, code)
                            # print(prog_kbk, code, program)
                            # print(GosprogramSR.get_by_tuple(prog_kbk, code, program))
                            if GosprogramSR.get_by_tuple(prog_kbk, code, program) is False or GosprogramSR.get_by_tuple(prog_kbk, code, program) is None:
                                GosprogramSR.add(prog_kbk, code, program)
                        elif sr_kbk[-2] == '0' and sr_kbk[-1] == '0':
                            subprog_kbk = sr_kbk[9:]
                            SRProg.add(subprog_kbk, code)
                            print(subprog_kbk, code, subprog_kbk[:2] + '000', program)
                            print(SubprogramSR.get_by_tuple(subprog_kbk, code, subprog_kbk[:2] + '000', program))
                            if SubprogramSR.get_by_tuple(subprog_kbk, code, subprog_kbk[:2] + '000', program) is False or SubprogramSR.get_by_tuple(subprog_kbk, code, subprog_kbk[:2] + '000', program) is None:
                                SubprogramSR.add(subprog_kbk, code, subprog_kbk[:2] + '000', program)
                        else:
                            if ''.join(row[index].value.split())[5:] == '00000':
                                main_event_kbk = sr_kbk[9:]
                                SRProg.add(main_event_kbk, code)
                                if MainEventSR.get_by_tuple(main_event_kbk, code, main_event_kbk[:-2] + '00', program) is False:
                                    MainEventSR.add(main_event_kbk, code, main_event_kbk[:-2] + '00', program)
                            else:
                                CSR.add(sr_kbk + ''.join(row[index].value.split())[5:], sr_kbk, format_title(row[first_column].value, 'csr'))
                        SR.add(sr_kbk, pr_kbk, sr_kbk[9:])
                    elif index == 5:
                        csr_title = format_title(row[first_column].value, 'csr')
                        vr_title = format_title(row[first_column].value, 'vr')
                        csr_kbk = pr_kbk + '.' + ''.join(row[index - 1].value.split())
                        vr_kbk = csr_kbk + '.' + str(row[index].value)
                        print(csr_kbk, sr_kbk, csr_title)
                        if CSR.get_by_tuple(csr_kbk, sr_kbk, csr_title) is False or CSR.get_by_tuple(csr_kbk, sr_kbk, csr_title) is None:
                            CSR.add(csr_kbk, sr_kbk, csr_title)
                        code_for_vr = csr_kbk[9:14]
                        if code_for_vr[-2] == '0' and code_for_vr[-1] == '0' and \
                                MainEventSR.get_by_tuple(code_for_vr, code, code_for_vr, 'Null') is False:
                            MainEventSR.add(code_for_vr, code, code_for_vr, 'Null')
                        VR.add(vr_kbk, csr_kbk, code, vr_title, str_to_float(row[index + 1].value),
                           str_to_float(row[index + 2].value), str_to_float(row[index + 3].value))
            commit_all()


year = str(2021)
cols_v, rows_v, cur_v, conn_v = parser_init(year + '/v' + year + '.xlsx',
                                    sheet_number=1, first_str_number=5)
cols_p, rows_p, cur_p, conn_p = parser_init(year + '/p' + year + '.xlsx',
                                    sheet_number=1, first_str_number=5)
first_column = 1

GRBS = SPTableArbitrary('grbs', cur_v, conn_v)
RZ = SPTableArbitrary('rz' + year, cur_v, conn_v, schema='Budget_Execution')
PR = SPTableArbitrary('pr' + year, cur_v, conn_v, schema='Budget_Execution')
SR = SPTableArbitrary('sr' + year, cur_v, conn_v, schema='Budget_Execution')
CSR = SPTableArbitrary('csr' + year, cur_v, conn_v, schema='Budget_Execution')
VR = SPTableArbitrary('vr' + year, cur_v, conn_v, schema='Budget_Execution')
GosprogramSR = SPTableArbitrary('gosprogram_sr' + year, cur_v, conn_v, schema='Budget_Execution')
SubprogramSR = SPTableArbitrary('subprogram_sr' + year, cur_v, conn_v, schema='Budget_Execution')
MainEventSR = SPTableArbitrary('main_event_sr' + year, cur_v, conn_v, schema='Budget_Execution')
SRProg = SPTableManyToMany('sr_prog' + year, cur_v, conn_v, schema='Budget_Execution')

first_column -= 1
table_parsing()
# grbs_kbk = '801'
# grbs_title = 'ГОСУДАРСТВЕННАЯ\nЖИЛИЩНАЯ ИНСПЕКЦИЯ ВОРОНЕЖСКОЙ ОБЛАСТИ'.replace('\n', ' ')
# grbs_title = grbs_title.replace('\xa0', ' ')
# if GRBS.get_by_tuple(grbs_kbk, grbs_title) is False or GRBS.get_by_tuple(grbs_kbk, grbs_title) is None:
#     GRBS.add(grbs_kbk, grbs_title)

# print(CSR.get_by_tuple('865.0801.1110461620', '865.0801.11104', 'Гранты в области науки, культуры, искусства и средств массовой информации '))
print(' ')