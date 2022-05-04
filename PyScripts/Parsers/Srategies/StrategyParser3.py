from PyScripts.TableClasses.SPTables.SPTable import SPTable
from PyScripts.TableClasses.SPTables.SPTableArbitrary import SPTableArbitrary
from PyScripts.base.base_functions import parser_init

cols, rows, cur, conn = parser_init('Стратегия.xlsx', 3, 4)

ResearchArea = SPTable('research_area', 'title_area', cur, conn, schema='Strategies')
Ratings = SPTable('ratings', 'title_rating', cur, conn, schema='Strategies')
PlaceOfVORating = SPTableArbitrary('place_of_vo_rating', 'id', cur, conn, schema='Strategies')

Years = SPTable('years', 'year', cur, conn)

for row in rows:
    id2017 = Years.get_id_by_name(2017)
    id_CFO = None  # Взять из RESEARCH_AREA
    id_RF = None  # Взять из RESEARCH_AREA

    place_of_vo_rating_id = int(row[0].value)
    title_rating = row[1].value
    title_rating_id = Ratings.add(title_rating)
    place_CFO = int(row[2].value)
    place_RF = int(row[3].value)

    PlaceOfVORating.add(place_of_vo_rating_id, title_rating_id, id_CFO, id2017, place_CFO)
    PlaceOfVORating.add(place_of_vo_rating_id+6, title_rating_id, id_RF, id2017, place_RF)
