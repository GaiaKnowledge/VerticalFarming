"""
    FAST BAD WRONG Code for VF Wiz
    Created on 25 Aug 2019
    Author: Francis Baumont De Oliveira
    Contact: sgfbaumo@liv.ac.uk
"""


# ==================================== IMPORT LIBRARIES ========================================== #

import json
import math
import numpy as np
from random import gauss

# Scenario
from Economic_model.scenario_module import Scenario

# Crop
from Economic_model.crop_module import Crop

# Equipment
from Economic_model.equipment_module import LightSystem
from Economic_model.equipment_module import GrowSystem
from Economic_model.equipment_module import Calculations
from Economic_model.equipment_module import PumpCalculations

# Utilities
from Economic_model.utilities_module import WaterCalculations

# Yield Factors
from Economic_model.yield_factors import YieldFactors


# ==================================== CONSTANTS ========================================== #

PSYCHOMETRIC_CONSTANT = 65.0  # Pa/K

# ==================================== INPUT SCENARIO ========================================== #

input_file = 'input_file.json'
scenario = Scenario()
scenario.getScenario(input_file)

# ============================ TIME SERIES DEFINED BY USER ================================================= #

days_timeseries =[]

for i in range(scenario.days+1):
    days_timeseries.append(i)

no_of_racks = Calculations.calc_no_of_racks(grow.system)

# opex_time_series: int = 0
# days = 366
# opex_array = []
# sales: int = 0
# sales_array = []
#
# print("days",days-1)
# input_file = 'input_file.json'
# scenario = get_scenario(input_file)

# ============================================== SALES ==================================================#


# ============================================== COST OF GOODS SOLD ==================================================#

# ---------------------------------------------- COGS: SEEDS COSTS ----------------------------------------------------#


# ------------------------------------------------------ COGS: NUTRIENTS COSTS ------------------------------------- #

# --------------------------------- COGS: MEDIA COSTS --------------------------------------------------------#

# ------------------------------------------------- COGS: co2 ENRICHMENT --------------------------------------------- #

# ----------------------------------------------------- COGS: LABOUR COSTS ----------------------------------#

# ------------------------------------------ COGS: PACKAGING COSTS -------------------------------------------------- #

# ---------------------------------------------- COGS: OVERALL COGS ------------------------------------------------- #


# ==================================== OPERATIONAL EXPENDITURE ============================== #
# ---------------------------------------------- OPEX: SALARIES ------------------------------------------------------#


# -------------------------------------------- OPEX: WATER CALCULATIONS ---------------------------------------------- #

# ------------------------------------- OPEX: LIGHT ENERGY CALCULATIONS --------------------------------------------#

# ---------------------------------- OPEX: hvac ENERGY CALCULATIONS --------------------------------------------------#

# ------------------------------------- OPEX: MISC. ENERGY CALCULATIONS ---------------------------------------------- #

# ----------------------------------- OPEX: OVERALL ENERGY CALC (LIGHTS+hvac+MISC) -----------------------#

# -------------------------------- OPEX: MAINTENANCE COST ----------------------------------------------------------#


# ---------------------------------------- OPEX: DISTRIBUTION COST ----------------------------------------------------#

# ---------------------------------- OPEX: RENEWABLE ENERGY REDUCTION ------------------------------------------------#

# ---------------------------------------------- OPEX: OVERALL OPEX --------------------------------------------------#


def calc_opex_time_series(days, monthly_salary_payments, energy_cost_per_month, water_cost_per_month,
              rent, maintenance_cost_per_month, distribution_cost_per_month, renewable_energy_reduction_per_month):
    """
    Can adjust for days/weekly/monthly/annually in the future - ASSUMED: CONSUMABLES PURCHASED QUARTERLY
    Operations = Bill Growth Lights + Bill Environmental Control + Bill Misc Energy + Water Bill + Salary Cost + Maintenance Cost + 
    Distribution cost - Reduction from Renewable Energy

    """
    opex_time_series = []
    for i in range(days):
        if i % 30 == 0:
            opex_time_series_bill += monthly_salary_payments  # Fixed costs
            opex_time_series_bill += energy_cost_per_month  # Lights and hvac energy costs
            opex_time_series_bill += water_cost_per_month
            opex_time_series_bill += misc_energy_cost_per_month
            opex_time_series_bill += maintenance_cost_per_month
            opex_time_series_bill += rent
            opex_time_series_bill += distribution_cost_per_month
            opex_time_series_bill -= renewable_energy_reduction_per_month
            opex_time_series.append(opex_time_series_bill)
        elif i % 365 == 0:
            opex_time_series_annual += 0 # Standing charge
            opex_time_series_annual += insurance_premium # Insurance premium annual charge
            opex_time_series.append(opex_time_series_annual)
        else:
            opex_time_series.append(0.0)
    return opex_time_series

# ========================================== REVENUE TIME SERIES ============================================= #


def calc_revenue_time_series(sales, sale_cycle):

    """
        Revenue Time Series
        Notes:
        -----
            Currently people pay per harvest cycle - consistent customers per delivery
            :param sales: The revenue generated from a sale
            :param sale_cycle: How often sales are made (days)
            :return: A time series for revenue generated for the number of days
    """
    revenue_time_series = []
    for i in range(days):
        if i % sale_cycle == 0:
            revenue_time_series.append(sales)
        else:
            revenue_time_series.append(0.0)
    return revenue_time_series

# ============================================== PROFIT AND MARGINS ===============================================#

# ---------------------------------------------- PROFIT ----------------------------------------------------------#


def calc_profit(revenue_time_series, opex_time_series, cogs_time_series):
    """
        Profit Formula
        Notes
        ------------
            Profit = revenue from sales - running costs (OpEx and COGS)
    """
    profit_time_series = revenue_time_series - opex_time_series - cogs_time_series 
    return profit_time_series

# ----------------------------------- GROSS PROFIT MARGIN ----------------------------------------------------------#


def calc_gross_profit_margin(revenue_time_series, cogs_time_series):  # Profit and Cost of Goods Sold - i.e. cost of materials and director labour costs
    """
        Gross Profit Margins Formula
        Notes
        ------------
            Profit Margins =  Total revenue - Cost of goods sold (COGS) / revenue
            = Profit / Revenue = Cost of Materials and Direct Labour Costs
    """
    gross_profit_margin = (revenue_time_series - cogs_time_series) / revenue_time_series 
    return gross_profit_margin

# -------------------------------------- LOAN & REPAYMENT INTEREST --------------------------------------------------#


def calc_loan_balance(capex, interest, days, repayment):
    """
        Loan Balance Equation
        Notes
        ----
            The formula for the remaining balance on a loan can be used to calculate the remaining balance at a given time(time n),
            whether at a future date or at present. The remaining balance on a loan formula shown is only used for a loan that is amortized,
            meaning that the portion of interest and principal applied to each payment is predetermined.
            FV / loan_balance = Future value - remaining balance
            PV = Present value - original balance
            P = Payment
            r = rate per payment
            n = number of payments
    """
    loan_balance: int(capex)
    monthly_interest = interest/12
    loan_balance_time_series = []
    for i in range(days):
        if i % 30 == 0:
            loan_balance = loan_balance * (1 + monthly_interest)**(i/30) - repayment * (((1+monthly_interest)**(i/30) - 1) / monthly_interest)
            loan_balance_time_series.append(loan_balance)
        else:
            loan_balance_time_series.append(0.0)

    return loan_balance_time_series

# ------------------------------------- TAX TIME SERIES ------------------------------------------------------------#


def calc_tax_rate(country):
    if country == uk:
        tax_rate = 0.2
        tax_deadline = "6th April"
        return tax_rate, tax_deadline
    else:
        raise RuntimeError("Unknown country: {}".format(country))


def calc_tax_time_series(tax_rate, days, profit_time_series):
    tax_time_series = []
    for i in range(days):
        if i % 365 == 0:
            tax_time_series.append((profit_time_series[i]-profit_time_series[i-365])*tax_rate)
        else:
            tax_time_series.append(0.0)
    return tax_time_series

# ---------------------------------------- RETURN ON INVESTMENT  ---------------------------------------#


def calc_roi(revenue_time_series, opex_time_series, cogs_time_series, interest, tax_time_series, capex):
    """
        Return on Investment Equation
        Notes
        -----
            Calculates ROI by calculating profit divided by total investment, and then multiplying by 100 for a percentage.
            The profit is calculated as the revenue computed from Eqn. 5, subtracting OpEx (Eqn. 1), COGS (Eqn. 2), the interest from the loan or investment,
            and taxes associated with the specified operation. The user has two options, to calculate ROI for a tax-year with annual revenue, or to calculate
            by using the computed monthly revenue with risk and uncertainty analysis applied on yield and sales. The ROI is calculated per month,
            which is then used for risk assessment
    """
    r = revenue_time_series - opex_time_series - cogs_time_series - interest - tax_time_series
    roi_array = (r / capex) * 100
    return roi_array

# ====================================================================================================================#
# ============================================== SCRIPT ==============================================================#
# ====================================================================================================================#


# OPEX

# opex_time_series: int = 0
# days = 366
# opex_array = []
# sales: int = 0
# sales_array = []
#
# print("days",days-1)
# input_file = 'input_file.json'
# scenario = get_scenario(input_file)
#
# no_of_racks = calc_no_of_racks(scenario.system, scenario.area)
# no_of_lights = calc_no_of_lights(scenario.system, no_of_racks)
# lights_daily_energy = calc_lights_energy(scenario.lights, no_of_lights)
#
# hvac_daily_energy = calc_hvac_energy(surface_area=scenario.surface, building_type=scenario.building,
#                                 Tin=get_temp_crop_reqs(scenario.crop), Tout=scenario.toutdoors)
# daily_energy_consumption_farm, monthly_energy_consumption_farm = calc_energy_consumption(hvac_daily_energy, lights_daily_energy)
# farm_plant_capacity, standard_yield = calc_plant_capacity(scenario.crop, scenario.system, no_of_racks)
# ys = standard_yield
# crop_ppfd_reqs = calc_crop_ppfd_reqs(scenario.crop)
# ppfd_lights = 295  # placeholder
#
# tf = 1
# opex_array.append(opex_time_series)
# # ARRAY conversion
# sales_array.append(sales)
# sales_array = np.asarray(sales_array) # Sales as an array
# opex_array = np.asarray(opex_array)  # OpEx as an array
# profit_array = profit(sales_array, opex_array)


# gross_profit_margin(sales_array, cogs)

# print("Profit £:", profit_array[-1])

# plt.plot(profit_array)
# plt.xlabel('Days')
# plt.ylabel('Gross Profit')
# plt.show()

# plt.figure()
# plt.plot(gross_profit_margin)
# plt.xlabel('Days')
# plt.ylabel('Gross Profit Margin')
# plt.show()
#
# print("Gross Profit Margin:",gross_profit_margin[-1])

# print("GOT costs ", costs)