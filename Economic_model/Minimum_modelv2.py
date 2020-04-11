# ========= IMPORT LIBRARIES ======= #
import numpy as np
import math
import matplotlib.pyplot as plt
import datetime


class TimeStepper():
    """Class to track where the simulation is in progress and time"""

    DAYS_IN_MONTH = 31
    DAYS_IN_YEAR = 365
    YEARLY_TO_MONTHLY_31 = 11.77

    def __init__(self,
                num_steps=None,
                timestep=None,
                start_date=None):
        self.step = None
        self.num_steps = num_steps
        self.timestep = timestep
        # Use the current date if one isn't passed in
        self.start_date = start_date or datetime.date.today()

    def is_month_end(self):
        if self.timestep.days == 1:
            return self.step % self.DAYS_IN_MONTH == 0
        raise NotImplementedError("Only implemented for day timestep")


def calc_capex(land_area):
    '''
    PP. 51 of Plant Factory
    Initial cost including necessary facilities (15 tiers, 50cm distance between tiers)
    $4000 USD per sq-m x 0.8 for £
    '''
    capex = 4000*0.8*land_area
    return capex


def calc_yield(land_area, GROWING_AREA_RATIO_TO_TOTAL, no_of_tiers, crops_per_area, harvest_weight):
    '''
    PP. 51 of Plant Factory
    3000 lettuce heads per sq-m per year (80-100g fresh weight)
    20 plants per sq-m (culture bed) x 15 tiers x 0.9 ratio salable
    x 0.5 effective floor ratio of tiers to total floor area
    50% of floor area used for operations, walkway, seedlings, production
    equipment.
    12-15 days to harvest
    20-22 days seed to seedling
    '''
    yield_potential = land_area * GROWING_AREA_RATIO_TO_TOTAL\
                      * crops_per_area * no_of_tiers * harvest_weight
    return yield_potential


def update_cogs(states, timestepper):
    """Calculates cogs at this step

    Notes
    -----
    seeds_cost + nutrients_cost + co2_cost + (labour_cost * 50) + packaging costs + media costs
    
    Can adjust for days/weekly/monthly/annually in the future - ASSUMED: CONSUMABLES PURCHASED MONTHLY
    """
    cogs_annual = states['initial_state']['yield_potential'] * 2
    cogs_monthly = cogs_annual / timestepper.YEARLY_TO_MONTHLY_31
    if timestepper.is_month_end():
        states['cogs'][step] = cogs_monthly


def update_labour(states, timestepper):
    """Calculates labour at this step
    
    Notes
    ------
    Direct farm labour cost = Number of staff working full-time x wages x 30 hours
    Generalisation if statement on farm labour required if unknown
    """
    farm_hours = states['initial_state']['yield_potential']  * 0.2
    wage = 7
    labour_annual = farm_hours * wage
    labour_monthly = labour_annual / timestepper.YEARLY_TO_MONTHLY_31
    if timestepper.is_month_end():
        states['labour'][step] = labour_monthly


def update_utilities(states, timestepper):
    """Calculates utilities at this step
    """
    water_consumption = states['initial_state']['yield_potential'] 
    energy_consumption = states['initial_state']['yield_potential'] 
    utilities_annual = water_consumption * energy_consumption
    utilties_monthly = utilities_annual / timestepper.YEARLY_TO_MONTHLY_31
    if timestepper.is_month_end():
        states['utilities'][step] = utilties_monthly


def setup_simulation(num_timesteps):
    """Sets up the data structure for the simulation"""
    states = {
        'initial_state' : None,
        'cogs' : np.zeros(num_timesteps, dtype=float),
        'labour' : np.zeros(num_timesteps, dtype=float),
        'utilities' : np.zeros(num_timesteps, dtype=float),
        'opex' : np.zeros(num_timesteps, dtype=float),
        'revenue' : np.zeros(num_timesteps, dtype=float),
        'loan_repayments' : np.zeros(num_timesteps, dtype=float),
        'tax_payments' : np.zeros(num_timesteps, dtype=float),
        'yield' : np.zeros(num_timesteps, dtype=float),
        'sales' : np.zeros(num_timesteps, dtype=float),
    }
    return states


def set_initial_state(states, user_inputs):
    """Calculates initial parameters that won't change during the simulation"""
    initial_state = {}
    initial_state['capex']  = calc_capex(user_inputs['land_area'])
    initial_state['yield_potential'] = calc_yield(user_inputs['land_area'],
                                                  user_inputs['growing_area_ratio_to_total'],
                                                  user_inputs['no_of_tiers'],
                                                  user_inputs['crops_per_area'],
                                                  user_inputs['harvest_weight'])
    states['initial_state'] = initial_state

def update_states(states, timestepper):
    """ Updates each quantity that changes with a timestep"""
    update_cogs(states, timestepper)
    update_utilities(states, timestepper)
    update_labour(states, timestepper)


def calculate_metrics(states, timestepper):
    """This is where we take what we've simulated and calculate any derived properties"""
    metrics = {
        'timestepper' : timestepper,
     }
    calculate_opex(metrics, states)
    return metrics


def calculate_opex(metrics, states):
    """Calculate the Operational Expenditure"""
    metrics['opex'] = states['utilities'] - states['labour']


def plot(metrics):
    """Draw the graphs we have calculated"""
    x_axis = [i for i in range(metrics['timestepper'].num_steps)]
    plt.plot(x_axis, metrics['opex'])
    plt.xlabel('Timestep')
    plt.ylabel('Opex')
    plt.show()

#
# Input starts here
#
user_inputs = {
    'yield_required' : 9000, #Annual yield (kg)
    'harvest_weight' : 0.1, # 100g of lettuce
    'land_area' : 200,
    'crop_price' : 10, # £ per kg
    'crops_per_area' : 20, # per sq-m of growbed
    'no_of_tiers' : 15,
    'growing_area_ratio_to_total' : 0.5,
}
#
# Parameters for this simulation
#
num_years = 5
num_steps = TimeStepper.DAYS_IN_YEAR * num_years
timestep = datetime.timedelta(days=1)
timestepper = TimeStepper(num_steps=num_steps,
                          timestep=timestep)
#
# Script starts here
#
# Create the data structures
states = setup_simulation(timestepper.num_steps)
# Calculate initial parameters
set_initial_state(states, user_inputs)
# Loop to run simulation
for step in range(timestepper.num_steps):
    timestepper.step = step
    update_states(states, timestepper)
metrics = calculate_metrics(states, timestepper)
plot(metrics)
