from PyScripts.TableClasses.PublicClasses.SPTable import SPTable
from PyScripts.TableClasses.PublicClasses.SPTableArbitrary import SPTableArbitrary
from PyScripts.base.base_functions import db_conn

cur, conn = db_conn()

# Expected_result = SPTable('expected_result', 'result', cur, conn)
FinancingSource = SPTableArbitrary('financing_source', 'source', cur, conn)
# FinancingSource.find_name_by_id(100)
FinancingSource.add(1, 'anime')
