import re
from os import listdir
from os.path import isfile, join
import datetime


def format_title(input_str):
    if '\n' in input_str and input_str[-1] != '\n':
        input_str.replace('\n', ' ')
    elif input_str[-1] == '\n':
        input_str.replace('\n', '')

    if input_str[-1] == '.':
        input_str.replace('.', '')

    return ' '.join(input_str.split())


def get_code(input_str):
    pattern = re.compile("[A-Z][0-9]|[A-Z][A-Z]")
    match = re.search(pattern, input_str)
    return match.group() if match else ""


def get_file_names(path):
    return [f for f in listdir(path) if isfile(join(path, f))]


def format_date(input_str):
    # DB format of DATE - YYYY-MM-DD
    given_format = '%d.%m.%Y'  # our format of DATE from doc - dd.mm.YYYY
    dates = input_str.replace(' ', '').split('-')
    start, end = datetime.datetime.strptime(dates[0], given_format).date(), datetime.datetime.strptime(dates[1],
                                                                                                       given_format).date()
    return start, end


def format_date_single(input_str):
    # DB format of DATE - YYYY-MM-DD
    given_format = '%d.%m.%Y'  # our format of DATE from doc - dd.mm.YYYY
    date_str = input_str.replace(' ', '')
    date = datetime.datetime.strptime(date_str, given_format).date()
    return date
