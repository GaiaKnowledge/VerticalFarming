

from Economic_model.scenario_module import Scenario


class Consumables(object):
    def __init__(self, towers_per_rack, grow_system_area, no_of_lights_req, no_of_plumbing_kit):
        self.towers_per_rack = towers_per_rack
        self.grow_system_area = grow_system_area
        self.no_of_lights_req = no_of_lights_req
        self.no_of_plumbing_kit = no_of_plumbing_kit


# ============================================== COST OF GOODS SOLD ==================================================#

# ---------------------------------------------- COGS: SEEDS COSTS ----------------------------------------------------#


def calc_seeds_cost(crop, ya, harvest_weight):
    """
        Seeds Calculator
        Notes
        ------
            :param crop: The crop that is selected to be grown on the farm
            :param ya: The expected yield for that crop
            :param harvest_weight: The harvest weight selected for that crop
            The seeds required are 40% more than the plants harvested. This is to account for error, unsuccessful
            propagation or thinning.
            :return: The cost per seed, and the number of seeds required to calculate the overall seed cost per year
    """
    if crop == 'lettuce':
        cost_per_seed = 0.10
    else:
        raise RuntimeError("Unknown crop: {}".format(crop))
    seeds_required = (ya/harvest_weight)*1.4
    seeds_cost = seeds_required * cost_per_seed  # costs of seeds
    return seeds_cost

# ------------------------------------------------------ COGS: NUTRIENTS COSTS ------------------------------------- #


def calc_nutrients_cost(ya):
    nutrients_cost = ya*0.20  # £0.20 worth of nutrients per kg of crop produced
    return nutrients_cost

# --------------------------------- COGS: MEDIA COSTS --------------------------------------------------------#


def calc_media_cost(ya):
    media_cost = ya*0.75  # £0.30 worth of media per kg of crop produced
    return media_cost

# ------------------------------------------------- COGS: co2 ENRICHMENT --------------------------------------------- #


def calc_co2_cost(co2_enrichment):
    if co2_enrichment:
        co2_cost = ya*0.1
    else:
        co2_cost = 0
    return co2_cost

# ----------------------------------------------------- COGS: LABOUR COSTS ----------------------------------#

# ------------------------------------------ COGS: PACKAGING COSTS -------------------------------------------------- #


def calc_packaging_cost(ya):
    packaging_cost = 0.5*ya  # 0.5 is cost per kilo of produce (User specified)
    return packaging_cost

# ---------------------------------------------- COGS: OVERALL COGS ------------------------------------------------- #


def calc_cogs(seeds_cost, nutrients_cost, media_cost, co2_cost, labour_cost, packaging_cost):
    cogs_annual = seeds_cost + nutrients_cost + co2_cost + (labour_cost * 50) + packaging_cost + media_cost # Annual cost of goods sold
    cogs_quarterly = cogs_annual / 4
    cogs_monthly = cogs_annual / 12
    cogs_weekly = cogs_annual / 50
    cogs_daily = cogs_annual / 365
    return cogs_annual, cogs_quarterly, cogs_monthly, cogs_weekly, cogs_daily


def calc_cogs_time_series(days, cogs_quarterly):
    """
        Cost of Goods Sold Formaula
        Notes
        -----
            Can adjust for days/weekly/monthly/annually in the future - ASSUMED: CONSUMABLES PURCHASED QUARTERLY
    """
    cogs_time_series = []
    for i in range(days):
        if i % 365/4 == 0:
            cogs_time_series.append(cogs_quarterly)
        else:
            cogs_time_series.append(0.0)
    return cogs_time_series