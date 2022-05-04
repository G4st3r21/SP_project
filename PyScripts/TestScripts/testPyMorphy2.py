import time
import pymorphy2
from PyScripts.base.base_functions import parser_init

morph = pymorphy2.MorphAnalyzer()

# cols, rows = parser_init('ОТЧЕТ_Развитие образования за 2016 год.xlsx', 1, 6, need_db_conn=False)
#
# for row in rows:
#     for cell in row[2:]:
#         text = cell.value
#         if type(text) is str:
#             print(text)
#             print(morph.parse(text)[0])
#             time.sleep(3)

for parse in morph.parse('государство'):
    print(parse.tag.cyr_repr)
    print(parse.word, parse.normal_form)

print('-----------------------------------------')
for parse in morph.parse('государсво'):
    print(parse.tag.cyr_repr)
    print(parse.word, parse.normal_form)

print('-----------------------------------------')
for parse in morph.parse('государсо'):
    print(parse.tag.cyr_repr)
    print(parse.word, parse.normal_form)