"""
    FAST BAD WRONG Code for VF Wiz
    Created on 25 Aug 2019
    Author: Francis Baumont De Oliveira
    Contact: 0780 704 6533
"""


# ==================================== IMPORT LIBRARIES ========================================== #

import json
import math
import numpy as np
from random import gauss
from Economic_model.vf_inputs import Scenario

# ==================================== CONSTANTS ========================================== #

PSYCHOMETRIC_CONSTANT = 65.0  # Pa/K

# ==================================== INPUT SCENARIO ========================================== #


def get_scenario(input_file):
    with open(input_file) as f:
        inputs = json.load(f)
    scenario = Scenario()
    scenario.currency = inputs['currency']
    scenario.country = inputs['country']
    scenario.capex = inputs["start_loan"]
    scenario.repayment = inputs["loan_repayment"]
    scenario.interest = inputs['loan_interest']
    scenario.lights = inputs['lights']
    scenario.crop = inputs['crop']
    scenario.area = inputs['grow_area']
    scenario.surface = inputs['surface_area']
    scenario.volume = inputs['farm_volume']
    scenario.building = inputs['building_type']
    scenario.rent = inputs['rental_costs']
    scenario.system = inputs['grow_system']
    scenario.co2 = inputs['co2_enrichment']
    scenario.energy = inputs['energy_price']
    scenario.renewable = inputs['ratio_of_renewable_energy_created_to_sourced']
    scenario.toutdoors = inputs['average_outdoor_temperature']
    scenario.crop_price = inputs['crop_price_per_kilo']
    scenario.farm_staff = inputs['number_of_farm_staff']
    scenario.salaries = inputs['annual_salaries_of_employees']
    scenario.standard_wage = inputs['standard_wage']
    scenario.insurance = inputs['insurance_premium']
    scenario.coverage = inputs['insurance_coverage']
    scenario.days = inputs['days_for_simulation']
    return scenario

# ============================================== SYSTEM AND EXPECTED YIELDS #==================================#


def calc_no_of_racks(grow_system, grow_area):
    if grow_system == 'ziprack_8':
        no_of_racks = math.floor(grow_area/4.62963)  # 54 Zipracks per 250 sq-m (including aisles, work bench & plumbing kit)
    else:
        raise RuntimeError("Unknown grow_system: {}".format(grow_system))
    return no_of_racks

# ------------------------------------ HARVEST WEIGHT ---------------------------------------------- #


def calc_harvest_weight(crop):

    if crop == "lettuce":
        harvest_weight = 0.5  # kg
    else:
        raise RuntimeError("Unknown crop {}".format(crop))
    return harvest_weight


def get_gross_yield(crop):
    if crop == 'lettuce':
        ys = 78.5  # kg / m2 / year
    else:
        raise RuntimeError("Unknown crop {}".format(crop))
    return ys


# ------------------------------------ PLANT CAPACITY ---------------------------------------------- #


def calc_plant_capacity(crop, grow_system, no_of_racks):   # Excluding propagation and only within the VFS
    if crop == "lettuce" and grow_system == 'ziprack_8':
        no_of_towers = no_of_racks*30  # Tight spacing with lettuce (30 towers per rack)
        yield_capacity = no_of_towers*3.3  # 3.3kg of greens per tower
        harvest_weight = calc_harvest_weight(crop)
        farm_plant_capacity = yield_capacity / harvest_weight # Potential yield divided by harvest weight of product
    else:
        raise RuntimeError("Unknown crop {}".format(crop))

    return farm_plant_capacity, yield_capacity


# ------------------------------------ LIGHTING SOLUTION ---------------------------------------------- #

def get_spec(lights):
    if lights == "intraspectra_spectrablade_8":
        light_wattage = 75
        light_efficiency = 0.4
        print("The {} light is {} watts with an efficiency of: {}".format(lights, light_wattage, light_efficiency))
    else:
        raise RuntimeError("Unknown lights {}".format(lights))
    return light_wattage, light_efficiency


def calc_no_of_lights(grow_system, no_of_racks):
    if grow_system == 'ziprack_8':
        no_of_lights = no_of_racks*24  # Assumption that 24 lighting units are require to cover crop area of 1 Ziprack (30 towers)
    else:
        raise RuntimeError("Unknown grow system {}".format(grow_system))
    return no_of_lights

# ------------------------------------ TEMPERATURE CROP REQUIREMENTS ---------------------------------------------- #


def get_temp_crop_reqs(crop):
    if crop == 'lettuce':
        Tin = 23.9  # Temperature optimal for lettuce growth
    else:
        Tin = 22  # 'general temperature'
    return Tin

# ====================================== FACTORS AND CROP YIELD =============================================#


def calc_crop_ppfd_reqs(crop):
    if crop == 'lettuce':
        crop_ppfd_reqs = 295
    else:
        raise RuntimeError("Unknown crop: {}".format(crop))
    return crop_ppfd_reqs


def calc_PAR_factor(ppfd_lights, crop_ppfd_reqs):
    parf = ppfd_lights/crop_ppfd_reqs
    return parf


def calc_co2_factor(co2_enrichment):
    if co2_enrichment:
        co2f = 1
    else:
        co2f = 0.9
    return co2f


def calc_failure_rate():
    fr = gauss(0.05, 0.02)
    return fr


def calc_standard_yield(crop):  # Standard yield per year
    """ Taken from table from Shao Economic Estimation Tool (2017)"""
    if crop == 'lettuce':
        return 78.5  # kg/m2/year
    else:
        raise RuntimeError("Unknown crop: {}".format(crop))


def calc_plant_area(grow_area, grow_system, no_of_racks):
    """ Plant area calculated using space taken by Racks - formula from Refarmers spreadsheet 2018"""
    if grow_system == 'ziprack_8':
        pa = (no_of_racks*4.300986) + 3.0612
    else:
        pa = grow_area
    return pa


def calc_temperature_factor(hvac_control):
    """
        Temperature Factor Equation
        Notes:
        --------
            The reduction in yield caused by over heating or freezing of the grow area, especially if the farm is uncontrolled by hvac or other systems
            If no hvac control, preliminary value set to 0.85. This should be assessed depending on climate, crop reqs and level of hvac control
            High:
            Med:
            Low:
    """

    if hvac_control == "high":  # If advanced hvac control then temperature factor is 1
        tf = 1
    else:
        tf = 0.85 
    return tf

def calc_system_multiplier(grow_system):
    """
    System Multiplier
    Notes
    -----
        Standard yield isn't 100% accurate and doesn't consider high density vertical farming systems. The estimated yield
        from ZipGrow Ziprack_8 is 66,825 kg/year for 235m2 plant area. Adjusted yield without multiplier is  18447.5 kg/year
        66,825/18447.5 kg = 3.622442065320504
    """
    if grow_system == 'ziprack_8':
        system_multiplier = 3.622442065320504
    else:
        raise RuntimeError("Unknown grow system {}".format(grow_system))
    return system_multiplier

# ---------------------------------------------- ADJUSTED YIELD ---------------------------------------------------- #


def calc_adjusted_yield(ys, pa, parf, co2f, tf, fr, system_multiplier):
    """
        Adjusted Plant Yield Equation
        Notes
        -----
            Ya = Ys x PA x parf x co2f x Tf x (1 - Fr)
            Adjusted Plant Yield = Standard Yield x Plant Area x PAR factor
            parf = ratio of actual PAR delivered to plant canopy compared to theoretical plant requirements. In artificial lighting
            VF the value was 1 as controlled at optimal level. Sun-fed plant level from EcoTect simulation.) x
            co2f = Increment by co2 enrichment
            Tf = Temperature factor (reflects reduction of yield caused by overheating or freezing of the growing area
            if indoor temperature is uncontrolled by hvac or other systems, value can be set for 0.9 for preliminary estimation)
            Fr = Failure rate, by default set at 5%
            Sm = System multiplier (best case scenario x system multiplier)
    """
    ya = ys * pa * parf * co2f * tf * (1 - fr) * system_multiplier
    return ya

# ============================================== SALES ==================================================#


def calc_sales(ya, crop_price, sale_cycle):
    crop_sales = (ya*crop_price)/ sale_cycle
    return crop_sales  # per sales or delivery cycle


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

# ==================================== OPERATIONAL EXPENDITURE ============================== #
# ---------------------------------------------- OPEX: SALARIES ------------------------------------------------------#


def calc_salary_payments(salaries):
    monthly_salary_payments = salaries/12
    return monthly_salary_payments

# -------------------------------------------- OPEX: WATER CALCULATIONS ---------------------------------------------- #


def calc_water_consumption(grow_system, no_of_racks, grow_area):

    if grow_system == "ziprack_8":
        water_consumption_per_month = no_of_racks * 0.95 * 30.42 # Litres of water per tower per day (0.25 gallons) multiplied by month
        water_buffer = 1900  # Litres of water for buffer per month (500 gallons)
        water_consumption_per_month += water_buffer  # Water consumption could be used here.
        water_consumption_per_day = water_consumption_per_month/30.42
        water_consumption_per_year = water_consumption_per_month*12
        water_consumption_per_week = (water_consumption_per_month*12)/52
        return water_consumption_per_day, water_consumption_per_week, water_consumption_per_month, water_consumption_per_year
    
    else:
        water_consumption_per_year = grow_area * 200  # Average from Agrilyst survey - 4 Gallons per sq ft per year
        water_consumption_per_month = water_consumption_per_year / 12  # consumption per month
        water_consumption_per_week = water_consumption_per_year/52
        water_consumption_per_day = water_consumption_per_year/365
        return water_consumption_per_day, water_consumption_per_week, water_consumption_per_month, water_consumption_per_year


def calc_water_cost(water_consumption_per_day, water_consumption_per_week, water_consumption_per_month, water_consumption_per_year, water_price, water_standing_charge):  # need to include standing charges
    water_cost_per_day = (water_consumption_per_day/1000) * water_price
    water_cost_per_week = (water_consumption_per_week/1000) * water_price
    water_cost_per_month = (water_consumption_per_month/1000) * water_price + water_standing_charge
    water_cost_per_year = (water_consumption_per_year/1000) * water_price
    return water_cost_per_day, water_cost_per_week, water_cost_per_month, water_cost_per_year

# ------------------------------------- OPEX: LIGHT ENERGY CALCULATIONS --------------------------------------------#


def calc_lights_energy(lights, no_of_lights):
    lights_watts, efficiency = get_spec(lights)
    lighting_kw_usage = lights_watts*no_of_lights/1000
    lights_kwh_per_day = lighting_kw_usage*12  # Assuming 12 hours of light for plants
    lights_kwh_per_month = lights_kwh_per_day * 30.417  # 365 days/12 months
    lights_kwh_per_week = lights_kwh_per_day*7
    lights_kwh_per_year = lights_kwh_per_day * 365
    return lights_kwh_per_day, lights_kwh_per_week, lights_kwh_per_month, lights_kwh_per_year

# ---------------------------------- OPEX: hvac ENERGY CALCULATIONS --------------------------------------------------#


def calc_hvac_energy(surface_area, building_type, Tin, Tout):
    """
        Heat Transfer Equation
        Notes
            -----
                Q = U x SA x (Tin - Tout)
                Q - ﻿Heat lost or gained due to outside temperature (kJ·h−1)
                U - Overall heat transfer coefficient (kJ·h−1·m−2·°C−1)
                SA - Surface Area of the space
                Tin - ﻿Inside air set point temperature (°C)
                Tout - ﻿Outside air temperature (°C)
    """

    if building_type == 'basement':
        U = 0.5
    else:
        U = 24 # generic heat transfer coefficient
    Q = U*surface_area*(Tin-Tout)
    hvac_kwh = Q*0.00666667*24  # Conversion factor of kJ/h to kWh x 24 hours

# Rudimentary hvac calculations - general
    hvac_kwh_per_day = hvac_kwh*1
    hvac_kwh_per_month = hvac_kwh_per_day * 30.417  # 365 days/12 months
    hvac_kwh_per_week = hvac_kwh_per_day * 7
    hvac_kwh_per_year = hvac_kwh_per_day * 365
    return hvac_kwh_per_day, hvac_kwh_per_week, hvac_kwh_per_month, hvac_kwh_per_year

# ------------------------------------- OPEX: MISC. ENERGY CALCULATIONS ---------------------------------------------- #


def calc_pump_energy(grow_system, no_of_racks):
    if grow_system == 'ziprack_8':
        no_of_plumbing_kits = math.ceil(no_of_racks/45) # spec for plumbing kit provided by Refarmers - 45 racks
        plumbing_kit_wattage = 1800  # spec for plumbing kit provided by Refarmers
        pumps_kw_usage = no_of_plumbing_kits * plumbing_kit_wattage / 1000
        pumps_kwh_per_day = pumps_kw_usage * 24  # 24 hours on
        pumps_kwh_per_month = pumps_kwh_per_day * 30.417  # 365 days/12 months
        pumps_kwh_per_week = pumps_kwh_per_day * 7
        pumps_kwh_per_year = pumps_kwh_per_day * 365
        return pumps_kwh_per_day, pumps_kwh_per_week, pumps_kwh_per_month, pumps_kwh_per_year
    else:
        raise RuntimeError("Unknown grow_system: {}".format(grow_system))


def calc_misc_energy(pumps_kwh_per_day):
    """
        Misc Energy Consumption
        Notes
        ------
            Energy consumption for miscellaneous elements such as: Filtration, Sensors, Internet, Office Lighting,
            Automation, Computers, etc.
    """
    misc_kwh_per_day = pumps_kwh_per_day
    return misc_kwh_per_day

# ----------------------------------- OPEX: OVERALL ENERGY CALC (LIGHTS+hvac+MISC) -----------------------#


def calc_energy_consumption(hvac_kwh_per_day, lights_kwh_per_day, misc_kwh_per_day):
    """
        Energy Consumption
        Notes
        ------
            Energy consumption for different time periods
    """
    farm_kwh_per_day = hvac_kwh_per_day + lights_kwh_per_day + misc_kwh_per_day
    farm_kwh_per_week = farm_kwh_per_day * 7  # 7 days in a week
    farm_kwh_per_month = farm_kwh_per_day * 30.417  # 365 days/12 months
    farm_kwh_per_year = farm_kwh_per_day * 365
    return farm_kwh_per_day, farm_kwh_per_week, farm_kwh_per_month, farm_kwh_per_year


def calc_energy_cost(farm_kwh_per_day, farm_kwh_per_week, farm_kwh_per_month, farm_kwh_per_year, energy_price):
    """
        Energy Costs
        Notes
        ------
            Energy cost for different time periods
    """
    energy_cost_per_day = farm_kwh_per_day * energy_price
    energy_cost_per_week = farm_kwh_per_week * energy_price  # 365 days/12 months
    energy_cost_per_month = farm_kwh_per_month * energy_price  # 365 days/12 months
    energy_cost_per_year = farm_kwh_per_year * energy_price
    return energy_cost_per_day, energy_cost_per_week, energy_cost_per_month, energy_cost_per_year

# -------------------------------- OPEX: MAINTENANCE COST ----------------------------------------------------------#


def calc_maintenance_cost(grow_system, no_of_racks):
    if grow_system == 'ziprack_8':
        maintenance_cost_per_month = no_of_racks*2.50  # £2.50 worth of labour per month to maintain
        return maintenance_cost_per_month
    else:
        raise RuntimeError("Unknown grow_system: {}".format(grow_system))

# ---------------------------------------- OPEX: DISTRIBUTION COST ----------------------------------------------------#


def calc_distribution_cost(sales, sale_cycle):   # Distribution cost per delivery
    distribution_cost_per_sale_cycle = sales*0.15
    distribution_cost_per_month = distribution_cost_per_sale_cycle*(30.417/sale_cycle)  # The number of delivery (sale) cycles in a month
    return distribution_cost_per_month

# ---------------------------------- OPEX: RENEWABLE ENERGY REDUCTION ------------------------------------------------#


def calc_renewable_energy_reduction(renewable, energy_cost_per_day):   # Distribution cost per delivery
    renewable_energy_reduction_per_day = energy_cost_per_day*renewable
    renewable_energy_reduction_per_week = energy_cost_per_day*7*renewable
    renewable_energy_reduction_per_month = energy_cost_per_day*30.417*renewable
    renewable_energy_reduction_per_year = energy_cost_per_day*365*renewable
    return renewable_energy_reduction_per_day, renewable_energy_reduction_per_week, renewable_energy_reduction_per_month, renewable_energy_reduction_per_year

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