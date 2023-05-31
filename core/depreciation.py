def straight_line_depreciation(cost, useful_life):
    depreciation_per_year = cost / useful_life
    return depreciation_per_year


def reducing_balance_depreciation(cost, useful_life, depreciation_rate):
    depreciation_amount = cost * depreciation_rate
    return depreciation_amount


def units_of_production_depreciation(cost, useful_life, units_produced):
    depreciation_per_unit = cost / useful_life
    depreciation_amount = units_produced * depreciation_per_unit
    return depreciation_amount
