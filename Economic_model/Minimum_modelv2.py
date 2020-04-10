"""
    Economic Model for VF
    Created on 30 March 2020
    Author: Francis Baumont De Oliveira
    Contact: sgfbaumo@liv.ac.uk
"""


# ========= IMPORT LIBRARIES ======= #
import numpy as np
import math
import matplotlib.pyplot as plt
import datetime


# ==========  GLOBAL VARIABLES ====== #

#Time parameters
YEARLY_TO_MONTHLY_31 = 11.77
DAYS_IN_MONTH = 31
DAYS_IN_YEAR = 365
WEEKS_IN_YEAR = 52
DAYS_IN_WEEK = 7
DAYS_IN_QUARTER = 112

ROI_THRESHOLD = -5 # Below this Number indicates Bankruptcy

GROWING_AREA_RATIO_TO_TOTAL = 0.5

# =========== CREATION OF TIME SERIES

num_days = 3660   # Days of simulation
days_timeseries = [i for i in range(num_days + 1)]  #  Creation of a timeseries for days
num_years = math.floor(num_days / 365)  #  Years of Simulation

# ====== USER INPUTS ======== #

yield_required = 9000 #Annual yield (kg)
harvest_weight = 0.1 # 100g of lettuce
land_area = 200
crop_price = 10 # £ per kg
crops_per_area = 20 # per sq-m of growbed
no_of_tiers = 15

# Capital Expenditure

def calc_capex(land_area):
    '''
    PP. 51 of Plant Factory
    Initial cost including necessary facilities (15 tiers, 50cm distance between tiers)
    $4000 USD per sq-m x 0.8 for £
    '''
    capex = 4000*0.8*land_area
    return capex

# Annual Productivity
def calc_yield(land_area, GROWING_AREA_RATIO_TO_TOTAL, no_of_tiers, crops_per_area):
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

# =========== OVERALL FIXED COSTS ========== #

# Depreciation of building and facilities

# Tax or Rent of Land/Building

# Insurance

# Basic Salaries

# Basic Charges for Electricity and Municipal Water


# ==========  ACTIVITIES ====== #

'''
    Cost Components from PP.52 Plant Factory
    Labour : 25-30%
    Electricity: 25-30%
    Depreciation: 25-35%
    Logistics: 9.8%
    Consumables: 7.6%
    Seeds: 2.1%
    Other: 11%
'''

# --------- PURCHASING CONSUMABLES ------- #

# CLEANING SUPPLIES - FIXED COST

# SEEDS - VARIABLE COST

def calc_seeds(land_area):
    '''
    Seeds typically account for 2.1% production costs
    PP. 51 of Plant Factory
    3000 lettuce heads per sq-m per year (80-100g fresh weight)
    20 plants per sq-m (culture bed) x 15 tiers x 0.9 ratio salable
    x 0.5 effective floor ratio of tiers to total floor area
    50% of floor area used for operations, walkway, seedlings, production
    equipment.
    12-15 days to harvest
    20-22 days seed to seedling
    '''
    qty_of_seeds = yield_potential/harvest_weight # annual qty of seeds required
    seeds_cost = qty_of_seeds * 0.01
    return seeds_cost

# PACKAGING - VARIABLE COST

"""
    Consumables typically account for 7.5% production costs
"""

# SUBSTRATE - VARIABLE COST

# NUTRIENTS - VARIABLE COST

# CO2 - VARIABLE COST

# PEST MANAGEMENT - VARIABLE COST

# --------- SOWING AND PROPAGATION ------- #

# CLEANING & SYSTEM MAINTENANCE - FIXED COST

# WATER & ENERGY - FIXED COST

# DEPRECIATION - FIXED COST

# LABOUR - VARIABLE COST


# --------- GROWING ------- #

# UTILITIES -
"""
    Electricity typically accounts for 21% of Production costs PP.52 Plant Factory
"""



def calc_utilities(yield_potential):  # Energy and Water
    water_consumption = yield_potential*1
    energy_consumption = yield_potential*1
    utilities_annual = water_consumption * energy_consumption
    return utilities_annual

# LABOUR

def calc_labour(yield_potential):
    """
            Labour Costs Formaula
            Notes
            ------
                Direct farm labour cost = Number of staff working full-time x wages x 30 hours
                Generalisation if statement on farm labour required if unknown
    """

    farm_hours = yield_potential*0.2
    labour_cost = farm_hours * 7 # wage
    return labour_cost

# DEPRECIATION
'''
    The economic life period for calculating the depreciation differs from country to country. 
    In Japan, it is 15 years for the PFAL building, 10 years for the facilities, and 5 years 
    for the LED lamps.
    
    Typically accounts for 21% of Production costs
'''

# EXPECTED YIELDS

def calc_expected_yield(yield_potential):
    yield_rate = 0.97 # Ratio of marketable plants produced by divided by no. of seeds transplanted
    expected_yield = yield_potential * yield_rate
    return expected_yield

# --------- HARVESTING AND PACKAGING ------- #

# LABOUR - Variable costs

# CLEANING & SYSTEM MAINTENANCE - Variable costs

# WASTE MANAGEMENT

# --------- PACKING AND DELIVERY ------- #

# DELIVERY LABOUR / OUTSOURCING FEES

"""
Packing and Delivery Typically 6-8% of production cost when near City 
12% when outside city PP.52 of Plant Factory
"""

"""
Logistics typically accounts for 9.8% PP.52 of Plant Factory
"""

# VEHICLE MAINTENANCE AND INSURANCE

# COMPLIANCE

# --------- SALES & MARKETING ------- #

# MARKETING COSTS

# OFFICE EXPENSES

# ==================== FINANCES ================ #

# OpEx Time series

'''The component costs for electricity, labor,
   depreciation, and others of the PFAL using fluorescent (FL) lamps
    in Japan accounted for, on average, 25% e 30%, 25% e 30%, 25% e 35%, 
    and 20%, respectively. 
    '''

def calc_cogs(yield_potential):
    '''
    seeds_cost + nutrients_cost + co2_cost + (labour_cost * 50) + packaging costs + media costs
    '''
    cogs_annual = yield_potential*2
    return cogs_annual

def calc_cogs_time_series(days, cogs_annual):
    """
        Cost of Goods Sold Formula
        Notes
        -----
            Can adjust for days/weekly/monthly/annually in the future - ASSUMED: CONSUMABLES PURCHASED MONTHLY
    """
    cogs_time_series = []
    for i in range(days):
        if i % DAYS_IN_MONTH == 0:
            cogs_time_series.append(cogs_annual / YEARLY_TO_MONTHLY_31)
        else:
            cogs_time_series.append(0)
    return cogs_time_series


def calc_opex_time_series(days, labour_cost, utilities):
    """
    Can adjust for days/weekly/monthly/annually in the future - ASSUMED: CONSUMABLES PURCHASED QUARTERLY
    Operations = Bill Growth Lights + Bill Environmental Control + Bill Misc Energy + Water Bill + Salary Cost + Maintenance Cost +
    Distribution cost - Reduction from Renewable Energy

    """
    opex_time_series = []
    for i in range(days):
        opex = 0
        if i % DAYS_IN_MONTH == 0:
            opex += (labour_cost / YEARLY_TO_MONTHLY_31) + (utilities / YEARLY_TO_MONTHLY_31)
        if i % DAYS_IN_YEAR == 0:
            opex += 0
        opex_time_series.append(opex)
    return opex_time_series


# Sales (ANNUALLY)

def calc_sales(expected_yield):  # per year
    sales = expected_yield*15 # £15 per kilo
    return sales


def calc_revenue_time_series(days, sales):
    revenue_time_series = []
    for i in range(days):
        revenue = 0
        if i % DAYS_IN_WEEK == 0:
            revenue += (sales/WEEKS_IN_YEAR)  # sales across 365 days of the year
        revenue_time_series.append(revenue)

    return revenue_time_series

# Profit
def calc_profit_time_series(opex_time_series, cogs_time_series, revenue_time_series):
    opex = np.asarray(opex_time_series)
    cogs = np.asarray(cogs_time_series)
    revenue = np.asarray(revenue_time_series)
    profit_time_series = revenue - cogs - opex
    return profit_time_series

# Loan
def calc_loan_repayment(capex, days):
    # Pay back over 5 years (no interest)
    monthly_loan_repayment = (capex/YEARLY_TO_MONTHLY_31)*5
    loan_time_series = []
    for i in range(days):
        repayment = 0
        if i % DAYS_IN_MONTH == 0:
            repayment = monthly_loan_repayment
        loan_time_series.append(repayment)
    return loan_time_series

# Tax
def calc_tax(days, profit_time_series):
    """Returns tax as daily series"""
    tax_time_series = []
    for i in range(days):
        if i % 365 == 0:
            tax_time_series.append(profit_time_series[364]*0.2)  # sales across 365 days of the year
        else:
            tax_time_series.append(0)
        tax = np.asarray(tax_time_series)
    return tax


# Post-tax profit
def calc_post_profit(profit_time_series, loan_repayments, tax):
    post_profit_time_series = profit_time_series - loan_repayments - tax
    return post_profit_time_series

def calc_post_profit_annual_series(post_profit_time_series, years):
    post_profit = np.cumsum(post_profit_time_series)
    profit_series = [0]

    for i in range(years):
        profit_series.append(post_profit[years * DAYS_IN_YEAR] - post_profit[(years * DAYS_IN_YEAR) - DAYS_IN_YEAR])

    profit_annual_series = np.asarray(profit_series)
    return profit_annual_series

# Return on Investment - Annually
def calc_roi(profit_annual_series, capex):
    roi = (profit_annual_series/capex) * 100
    return roi

# Probability of Bankruptcy
def calc_probability_of_bankruptcy(roi, ROI_THRESHOLD, years):
    PBS =[0] # Probability of Bankruptcy series

    for i in range(years):
        if ROI_THRESHOLD > roi[i]:
            probability_of_bankruptcy = 1
            PBS.append(probability_of_bankruptcy)
        else:
            PBS.append(0)
    return PBS

#Script for ROI Estimation
# Calculate initial state
capex = calc_capex(land_area)
yield_potential = calc_yield(land_area, GROWING_AREA_RATIO_TO_TOTAL, no_of_tiers, crops_per_area)
# calculate total variable quantities based on initial state
cogs_annual = calc_cogs(yield_potential)
utilities = calc_utilities(yield_potential)
labour = calc_labour(yield_potential)
expected_yield = calc_expected_yield(yield_potential)
sales = calc_sales(expected_yield)
# calculate derived quantities time series based on calculated quantities
cogs_time_series = calc_cogs_time_series(num_days, cogs_annual)
opex_time_series = calc_opex_time_series(num_days, labour, utilities)
revenue_time_series = calc_revenue_time_series(num_days, sales)
loan_time_series = calc_loan_repayment(capex, num_days)
# calculate derived metrics from base quantities
profit_time_series = calc_profit_time_series(opex_time_series, cogs_time_series, revenue_time_series)
tax_time_series = calc_tax(num_days, profit_time_series)
post_profit_time_series = calc_post_profit(profit_time_series, loan_time_series, tax_time_series)
profit_annual_series = calc_post_profit_annual_series(post_profit_time_series, num_years)
# final metrics
roi = calc_roi(profit_annual_series, capex)
PBS = calc_probability_of_bankruptcy(roi, ROI_THRESHOLD, num_years)





def update_cogs(states, step):
    """Calculates cogs at this step

    Notes
    -----
    seeds_cost + nutrients_cost + co2_cost + (labour_cost * 50) + packaging costs + media costs
    
    Can adjust for days/weekly/monthly/annually in the future - ASSUMED: CONSUMABLES PURCHASED MONTHLY
    """
    cogs_annual = states['initial_state']['yield_potential'] * 2
    cogs_monthly = cogs_annual / YEARLY_TO_MONTHLY_31
    if step % DAYS_IN_MONTH == 0:
        states['cogs'][step] = cogs_monthly


def update_labour(states, step):
    """Calculates labour at this step
    
    Notes
    ------
    Direct farm labour cost = Number of staff working full-time x wages x 30 hours
    Generalisation if statement on farm labour required if unknown
    """
    farm_hours = states['initial_state']['yield_potential']  * 0.2
    wage = 7
    labour_annual = farm_hours * wage
    labour_monthly = labour_annual / YEARLY_TO_MONTHLY_31
    if step % DAYS_IN_MONTH == 0:
        states['labour'][step] = labour_monthly


def update_utilities(states, step):
    """Calculates utilities at this step
    """
    water_consumption = states['initial_state']['yield_potential'] 
    energy_consumption = states['initial_state']['yield_potential'] 
    utilities_annual = water_consumption * energy_consumption
    utilties_monthly = utilities_annual / YEARLY_TO_MONTHLY_31
    if step % DAYS_IN_MONTH == 0:
        states['utilities'][step] = utilties_monthly



def setup_simulation(num_timesteps, timestep):
    """Sets up the data structure for the simulation"""
    states = {
        'initial_state' : None,
        'num_timesteps' : num_timesteps,
        'timestep' : timestep,
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
                                           user_inputs['crops_per_area'])
    states['initial_state'] = initial_state

def update_states(states, step):
    """ Updates each quantity that changes with a timestep"""
    update_cogs(states, step)
    update_utilities(states, step)
    update_labour(states, step)


def calculate_opex(metrics, states):
    metrics['opex'] = states['utilities'] = states['labour']


def calculate_metrics(states):
    metrics = {
        'num_timesteps' : states['num_timesteps'],
     }
    calculate_opex(metrics, states)
    return metrics


def plot(metrics):
    x_axis = [i for i in range(metrics['opex'].size)]
    plt.plot(x_axis, metrics['opex'])
    plt.xlabel('Timestep')
    plt.ylabel('Opex')
    plt.show()


user_inputs = {
    'yield_required' : 9000, #Annual yield (kg)
    'harvest_weight' : 0.1, # 100g of lettuce
    'land_area' : 200,
    'crop_price' : 10, # £ per kg
    'crops_per_area' : 20, # per sq-m of growbed
    'no_of_tiers' : 15,
    'growing_area_ratio_to_total' : 0.5,
}

num_years = 5
num_timesteps = DAYS_IN_YEAR * num_years
timestep = datetime.timedelta(days=1)
states = setup_simulation(num_timesteps, timestep)
# Calculate initial parameters
set_initial_state(states, user_inputs)
# Run simulation
for step in range(num_timesteps):
    update_states(states, step)
metrics = calculate_metrics(states)
plot(metrics)





# def plot(num_years, roi, PBS):

#     years_series = [i for i in range(num_years + 1)]  # Creation of time series for years

#     #Plot
#     plt.plot(years_series, roi)
#     plt.xlabel('Years')
#     plt.ylabel('Annual ROI')
#     plt.show()


#     # Setting up Risk Assessment Plot

#     fig, ax = plt.subplots()
#     ax.plot(years_series, PBS, 1, color="g")

#     # Threshold Lines

#     '''
#     - Critical: 50% probability of bankruptcy within 3 years
#     - Substantial risk: 25% probability of bankruptcy within 5 years
#     - Moderate risk: 10% probability of bankruptcy within 10 years 
#     - Safe: Less than 10% probability of bankruptcy within 10 years
#     '''

#     years_thresholds = np.asarray(years_series)
#     safe_threshold = 0.01 * years_thresholds
#     substantial_threshold = 0.05 * years_thresholds
#     critical_threshold = 0.1666 * years_thresholds

#     safe_threshold = safe_threshold.tolist()
#     substantial_threshold = substantial_threshold.tolist()
#     critical_threshold = critical_threshold.tolist()

#     # Risk Assessment Graph Plot

#     #ax.plot([years_thresholds, years_thresholds], [safe_threshold, safe_threshold], "k--")
#     #ax.plot([years_thresholds, years_thresholds], [substantial_threshold, substantial_threshold], "k--")
#     #ax.plot([0., years], [critical_threshold, critical_threshold], "k--")

#     plt.suptitle('Risk Assessment')
#     plt.plot(years_series, PBS)
#     plt.plot(years_series, safe_threshold, "r--", label = "safe/moderate")
#     plt.plot(years_series, substantial_threshold, "r--", label = "moderate/substantial")
#     plt.plot(years_series, critical_threshold, "r--", label = "substantial/critical")

#     plt.ylim(0,1)
#     plt.xlim(0,num_years)
#     plt.grid(True)
#     plt.xlabel('Time (Years)')
#     plt.ylabel('Probability of Bankruptcy')
#     plt.show()






# # Formulas for Produtivity KPIs

# def calc_eletricity_kpi(annual_yield, annual_energy_consumption):
#     elec_kpi = annual_yield / annual_energy_consumption
#     return elec_kpi

# def calc_labour_kpi(annual_yield, annual_labour):
#     labour_kpi = annual_yield / annual_labour
#     return labour_kpi

# def calc_cultivation_area_kpi(annual_yield, land_area, GROWING_AREA_RATIO_TO_TOTAL):
#     cultivation_kpi = annual_yield / (land_area * GROWING_AREA_RATIO_TO_TOTAL)
#     return cultivation_kpi

# def calc_cost_performance(opex, cogs, revenue):
#     CP = revenue/(opex+cogs)
#     return CP



# #Script for Productivity KPIs

