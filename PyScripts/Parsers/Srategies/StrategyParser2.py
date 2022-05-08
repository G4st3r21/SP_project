from PyScripts.TableClasses.SPTables.SPTable import SPTable
from PyScripts.TableClasses.SPTables.SPTableArbitrary import SPTableArbitrary
from PyScripts.base.base_functions import parser_init

cols, rows, cur, conn = parser_init('Стратегия.xlsx', 2, 4)

StrategyIndicators = SPTableArbitrary('indicators2', cur, conn, schema='Strategies')
ResearchArea = SPTable('research_area', cur, conn, schema='Strategies')
GrowthRates20162011 = SPTableArbitrary('growth_rates_2016_2011', cur, conn, schema='Strategies')
PlaceOfVOInd = SPTableArbitrary('place_of_vo_ind', cur, conn, schema='Strategies')

IndicatorsNames = SPTableArbitrary('indicators_names', cur, conn)
Years = SPTable('years', cur, conn)


def format_indicator(ind: str):
    return float(ind) if '-' not in ind else -1


ind_name_id = 197
strategy_indicator_id = 1
growth_rates_id = 1
place_of_vo_ind_id = 1
for row in rows:
    id2011 = 21
    id2016 = 1
    id_RF = ResearchArea.add('RF')  # Взять из RESEARCH_AREA
    id_CFO = ResearchArea.add('CFO')  # Взять из RESEARCH_AREA
    id_VO = ResearchArea.add('VO')  # Взять из RESEARCH_AREA

    indicator_title = row[0].value.split(',')[:-1][0]
    indicator_type = row[0].value.split(',')[-1]
    id_ind_name = IndicatorsNames.add(ind_name_id, indicator_title, indicator_type, 'null', conditinon_type='OR')
    ind_name_id += 1 if id_ind_name >= ind_name_id else 0

    indicator_2011 = format_indicator(row[1].value)
    indicator_2016 = format_indicator(row[2].value)
    StrategyIndicators.add(strategy_indicator_id, id_ind_name, id2011, indicator_2011)
    strategy_indicator_id += 1
    StrategyIndicators.add(strategy_indicator_id, id_ind_name, id2016, indicator_2016)
    strategy_indicator_id += 1

    growth_rates_RF = format_indicator(row[3].value)
    growth_rates_CFO = format_indicator(row[4].value)
    growth_rates_VO = format_indicator(row[5].value)
    GrowthRates20162011.add(growth_rates_id, id_ind_name, id_RF, growth_rates_RF)
    growth_rates_id += 1
    GrowthRates20162011.add(growth_rates_id, id_ind_name, id_CFO, growth_rates_CFO)
    growth_rates_id += 1
    GrowthRates20162011.add(growth_rates_id, id_ind_name, id_VO, growth_rates_VO)
    growth_rates_id += 1

    VO_place_2011_CFO = int(row[6].value)
    VO_place_2011_RF = int(row[7].value)
    PlaceOfVOInd.add(place_of_vo_ind_id, id_ind_name, id_CFO, id2011, VO_place_2011_CFO)
    place_of_vo_ind_id += 1
    PlaceOfVOInd.add(place_of_vo_ind_id, id_ind_name, id_RF, id2011, VO_place_2011_RF)
    place_of_vo_ind_id += 1

    VO_place_2016_CFO = int(row[8].value)
    VO_place_2016_RF = int(row[9].value)
    PlaceOfVOInd.add(place_of_vo_ind_id, id_ind_name, id_CFO, id2016, VO_place_2016_CFO)
    place_of_vo_ind_id += 1
    PlaceOfVOInd.add(place_of_vo_ind_id, id_ind_name, id_RF, id2016, VO_place_2016_RF)
    place_of_vo_ind_id += 1
