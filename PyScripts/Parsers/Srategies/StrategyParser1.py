from PyScripts.TableClasses.SPTables.SPTable import SPTable
from PyScripts.TableClasses.SPTables.SPTableArbitrary import SPTableArbitrary
from PyScripts.base.base_functions import parser_init

cols, rows, cur, conn = parser_init('Стратегия.xlsx', 1, 4)

StrategyIndicators = SPTableArbitrary('strategy_indicators', 'id', cur, conn, schema='Strategies')
IndicatorNames = SPTableArbitrary('indicator_names', 'indicator_title', cur, conn)
Years = SPTable('years', 'year', cur, conn)


def format_indicator(ind: str):
    if '<*>' in ind:
        ind = float(ind.replace('<*>', ''))
        estimated_actual = 0
    else:
        estimated_actual = 1
        if 'н/д' in ind:
            ind = -1

    return ind, estimated_actual


for row in rows:
    strategy_indicator_id = row[0].value
    indicator_title = row[1].value.split(',')[:-1]
    indicator_type = row[1].value.split(',')[-1]
    indicator2009_plan = row[2].value
    indicator2017_plan = row[3].value
    indicator2017_fact, estimated_actual = format_indicator(row[4].value)

    ind_title_id = IndicatorNames.get_id_by_name(indicator_title)
    id2017 = Years.get_id_by_name(2017)
    id2009 = Years.get_id_by_name(2009)
    StrategyIndicators.add(strategy_indicator_id, ind_title_id, id2009, indicator2009_plan, -1, 1)
    StrategyIndicators.add(strategy_indicator_id + 23, ind_title_id, id2017, indicator2017_plan, indicator2017_fact,
                           estimated_actual)


StrategyIndicators.commit()
