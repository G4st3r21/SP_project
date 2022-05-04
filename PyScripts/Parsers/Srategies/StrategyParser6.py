from PyScripts.TableClasses.SPTables.SPTable import SPTable
from PyScripts.TableClasses.SPTables.SPTableArbitrary import SPTableArbitrary
from PyScripts.base.base_functions import parser_init

cols, rows, cur, conn = parser_init('Стратегия.xlsx', 6, 4)

RegionsCFO = SPTable('regions_cfo', 'region', cur, conn, schema='Strategies')
IndustrialIndices = SPTableArbitrary('industrial_indices', 'id', cur, conn, schema='Strategies')
Years = SPTable('years', 'year', cur, conn)

industrial_indices_id = 1
for row in rows:
    id_years = [Years.get_id_by_name(i) for i in range(2010, 2017)]

    region_CFO = row[0].value
    region_CFO_id = RegionsCFO.add(region_CFO)

    indexes = [float(row[i].value) for i in range(1, 8)]

    for i in range(7):
        IndustrialIndices.add(industrial_indices_id, region_CFO_id, id_years[i], indexes[i])
        industrial_indices_id += 1
