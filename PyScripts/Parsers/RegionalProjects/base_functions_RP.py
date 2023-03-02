import re
from os import listdir
from os.path import isfile, join


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
