from PyScripts.TableClasses.PublicClasses.SPTableManyToMany import SPTableManyToMany
from PyScripts.TableClasses.PublicClasses.SPTable import SPTable
from PyScripts.TableClasses.PublicClasses.SPTableArbitrary import SPTableArbitrary
from PyScripts.base.base_functions import db_conn

cur, conn = db_conn()

AimAndGosprogram = SPTableManyToMany('aim_and_gosprogram', cur, conn)
print(AimAndGosprogram.table_name, AimAndGosprogram.schema)
print(AimAndGosprogram.columns)
print(AimAndGosprogram.find_tuple(1, 'A'))
AimAndGosprogram.add(1, 'A')
print(AimAndGosprogram.get_first_columns_by_second('A'))
print(AimAndGosprogram.get_second_columns_by_first(1))

