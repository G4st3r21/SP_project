from PyScripts.TableClasses.SPTables.SPTable import SPTable
from PyScripts.TableClasses.SPTables.SPTableArbitrary import SPTableArbitrary
from PyScripts.base.base_functions import parser_init

cols, rows, cur, conn = parser_init('Стратегия.xlsx', 8, 4) # Прогнать для 8 и 9

DevelopmentOPPSVO = SPTable('development_opps_vo', 'opportunity', cur, conn, schema='Strategies')
EvaluationOfOPPS = SPTable('evaluation_of_opps', 'evaluation_criteria', cur, conn, schema='Strategies')

EvaluationValue = SPTableArbitrary('evaluation_value', 'id', cur, conn, schema='Strategies')

for row in rows:
    pass
