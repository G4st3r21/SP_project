import time
import pymorphy2
from PyScripts.base.base_functions import parser_init

cols, rows, cur, conn = parser_init("План мероприятий.xlsx", sheet_number=3, first_str_number=2)
morph = pymorphy2.MorphAnalyzer()


for row in rows:
    for word in row[4].value.split():
        w = morph.parse(word=word)[0].tag.case
        if word == 'бюджет' and w == 'nomn':
            print(*[wrd for wrd in row[4].value.split()[row[4].value.split().index(word):]], sep=' ')
