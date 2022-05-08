from PyScripts.TableClasses.SPTables.SPTable import SPTable
from PyScripts.TableClasses.SPTables.SPTableArbitrary import SPTableArbitrary
from PyScripts.base.base_functions import parser_init

cols, rows, cur, conn = parser_init('Стратегия.xlsx', 1, 4)

StrategyIndicators = SPTableArbitrary('indicators1', cur, conn, schema='Strategies')
IndicatorNames = SPTableArbitrary('indicators_names', cur, conn)
Years = SPTable('years', cur, conn)


def format_indicator(ind: str):
    print(ind)
    if type(ind) not in [float, int] and '<*>' in ind:
        ind = float(ind.replace(' <*>', '').replace(',', '.'))
        estimated_actual = 0
    else:
        estimated_actual = 1
        if type(ind) not in [float, int] and 'н/д' in ind:
            ind = -1
        elif type(ind) is str:
            ind = float(''.join(ind.split()))
    print(ind)

    return ind, estimated_actual


for row in rows:
    strategy_indicator_id = row[0].value
    indicator_title = ','.join(row[1].value.split(',')[:-1])
    indicator_type = row[1].value.split(',')[-1]
    indicator2009_plan = format_indicator(row[2].value)[0]
    indicator2017_plan = format_indicator(row[3].value)[0]
    indicator2017_fact, estimated_actual = format_indicator(row[4].value)

    ind_title_id = IndicatorNames.get_by_column('indicator_title', indicator_title)
    if not ind_title_id:
        ind_title_id = IndicatorNames.add(indicator_title, indicator_type, 'null')
    else:
        ind_title_id = ind_title_id[0]
    id2017 = Years.add(2017)
    id2009 = Years.add(2009)
    StrategyIndicators.add(strategy_indicator_id, ind_title_id, id2009, indicator2009_plan, -1, 1)
    StrategyIndicators.add(strategy_indicator_id + 23, ind_title_id, id2017, indicator2017_plan, indicator2017_fact,
                           estimated_actual)


StrategyIndicators.commit()
IndicatorNames.commit()
Years.commit()
