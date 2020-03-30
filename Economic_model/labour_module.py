
# Labour Module

# Labour CLASS

from Economic_model.scenario_module import Scenario
from Economic_model.equipment_module import GrowSystem


class LabourCalculations(Scenario, GrowSystem):
    def __init__(self):
        super().__init__()


def calc_salary_payments(salaries):
    monthly_salary_payments = salaries/12
    return monthly_salary_payments

# ----------------------------------------------------- COGS: LABOUR COSTS ----------------------------------#


def calc_labour_cost(farm_staff, standard_wage):
    """
        Labour Costs Formaula
        Notes
        ------
            Direct farm labour cost = Number of staff working full-time x wages x 30 hours
            Generalisation if statement on farm labour required if unknown
    """
    labour_cost = farm_staff * standard_wage * 35
    return labour_cost
