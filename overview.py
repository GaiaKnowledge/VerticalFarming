# coding=utf-8
from datetime import datetime
from datetime import timedelta
from inputs import Scenario
from inputs import Growthplan
from inputs import Staff
from equipment import Lights
from equipment import System
from crops import Crops
import pandas as pd
import numpy as np
from dateutil.relativedelta import *
import random
import matplotlib.pyplot as plt
import os
from math import pi
import math
#import pba

from openpyxl import Workbook

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory

years = 15 # Time series length !!UP TO 20!!
days_in_year = 365.25
months_in_a_year = 12
simulations = 20

#Crops
basil_lemon = Crops('Basil - Lemon', 'n/a',	'n/a',	14,	42,	'n/a', 'n/a', 'n/a', 13.067,	'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 0.03, 0.97, 'herbs')
lettuce_fu_mix = Crops('Lettuce (Farm Urban Mix)',	0,	0,	16,	35,	0,	0,	0,	33,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0.03, 0.97, 'leafy greens')
none = Crops('none',	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 1, 'n/a')
basil_genovese = Crops('Basil - Genovese',	0,	0,	14,	42,	0,	0,	34.33833756,	9.802857143,	35.67186965,	33.33830224,	33.33830224, 0,	0,	16.66892363,	0,	0,	0,	0,	0,	0,	0,	0,	0.03, 0.97, 'herbs')

#Equipment
Spectra_Blade_Single_Sided_J = Lights('Intravision Spectra Blade Single Sided - J', 'LED', 'Spectra J', 160,
                                      '32-37.5 (Vdc)', 120, 100, '1.6-3.4', 1.6, 0, '152 degree coverage',
                                      'Passive Air Cooling', 0, 0, 0, 60000, '2.39m x 112mm x 36mm', 5.5,
                                      '3m +-0.2m', 0, '3-year std', 0,
                                      'https://www.intravisiongroup.com/spectra-blades', False)

# Input File
def get_scenario():
    """Get Scenario
        Notes: Scenario is extracted from /Users/Francis/PycharmProjects/VerticalFarming/Current_Financial_Model.xlsx
        This should be edited according to the file path and name of the saved excel model.

    Returns:
        scenario (object): The farm scenario that provided the basis of the analysis

    To Do:
    """

    input_filepath = '/Users/Francis/PycharmProjects/VerticalFarming/Current_Financial_Model.xlsx' # Make a copy and call spreadsheet this name
    inputs = pd.read_excel(input_filepath, index_col=0).to_dict()
    inputs = inputs['Inputs']

    scenario = Scenario()
    scenario.start_date = inputs['start_date']
    scenario.facility_size_pilot = inputs["facility_size_pilot"]
    scenario.percent_production_area_pilot = inputs['percent_production_area_pilot']
    scenario.growing_levels_pilot = inputs['growing_levels_pilot']
    scenario.weight_unit = inputs['weight_unit']
    scenario.growing_area_mulitplier = inputs['growing_area_mulitplier']
    scenario.no_lights_pilot = inputs['no_lights_pilot']
    scenario.packaging_cost_pilot = inputs['packaging_cost_pilot']
    scenario.packaging_cost_full = inputs['packaging_cost_full']
    scenario.other_costs_pilot = inputs['other_costs_pilot']

    scenario.farm_type = inputs['farm_type']
    scenario.business_model = inputs['business_model']
    scenario.grower_exp = inputs['grower_exp']
    scenario.automation_level = inputs['automation_level']
    scenario.climate_control = inputs['climate_control']
    scenario.lighting_control = inputs['lighting_control']
    scenario.nutrient_control = inputs['nutrient_control']
    scenario.system_type = inputs['system_type']
    scenario.system_quantity = inputs['system_quantity']
    scenario.light_system = inputs['light_system']
    scenario.growing_media = inputs['growing_media']
    scenario.ceiling_height = inputs['ceiling_height']
    scenario.insultation_level = inputs['insultation_level']
    scenario.roof_type = inputs['roof_type']
    scenario.co2_enrichment = inputs['co2_enrichment']
    scenario.structure_type = inputs['structure_type']
    scenario.water_price = inputs['water_price']
    scenario.electricity_price = inputs['electricity_price']
    scenario.labour_improvement = inputs['labour_improvement']
    scenario.percentage_renewable_energy = inputs['percentage_renewable_energy']
    scenario.biosecurity_level = inputs['biosecurity_level']

    scenario.loan_amount = inputs['loan_amount']
    scenario.tax_rate = inputs['tax_rate']
    scenario.loan_interest = inputs['loan_interest']
    scenario.loan_tenure = inputs['loan_tenure']
    scenario.loan_type = inputs['loan_type']

    # crop 1
    scenario.crop_typ1 = inputs['crop_typ1']
    scenario.crop1_percent = inputs['crop1_percent']
    scenario.crop1_system = inputs['crop1_system']
    scenario.crop1_harvest_weight = inputs['crop1_harvest_weight']
    scenario.crop1_product_weight = inputs['crop1_product_weight']
    scenario.crop1_customer_percent = inputs['crop1_customer_percent']
    scenario.crop1_price1 = inputs['crop1_price1']
    scenario.crop1_price2 = inputs['crop1_price2']

    # crop 2
    scenario.crop_typ2 = inputs['crop_typ2']
    scenario.crop2_percent = inputs['crop2_percent']
    scenario.crop2_system = inputs['crop2_system']
    scenario.crop2_harvest_weight = inputs['crop2_harvest_weight']
    scenario.crop2_product_weight = inputs['crop2_product_weight']
    scenario.crop2_customer_percent = inputs['crop2_customer_percent']
    scenario.crop2_price1 = inputs['crop2_price1']
    scenario.crop2_price2 = inputs['crop2_price2']

    # crop 3
    scenario.crop_typ3 = inputs['crop_typ3']
    scenario.crop3_percent = inputs['crop3_percent']
    scenario.crop3_system = inputs['crop3_system']
    scenario.crop3_harvest_weight = inputs['crop3_harvest_weight']
    scenario.crop3_product_weight = inputs['crop3_product_weight']
    scenario.crop3_customer_percent = inputs['crop3_customer_percent']
    scenario.crop3_price1 = inputs['crop3_price1']
    scenario.crop3_price2 = inputs['crop3_price2']

    # crop 4
    scenario.crop_typ4 = inputs['crop_typ4']
    scenario.crop4_percent = inputs['crop4_percent']
    scenario.crop4_system = inputs['crop4_system']
    scenario.crop4_harvest_weight = inputs['crop4_harvest_weight']
    scenario.crop4_product_weight = inputs['crop4_product_weight']
    scenario.crop4_customer_percent = inputs['crop4_customer_percent']
    scenario.crop4_price1 = inputs['crop4_price1']
    scenario.crop4_price2 = inputs['crop4_price2']

    # Growth multiplier
    scenario.vadded_products_multiplier = inputs['vadded_products_multiplier']
    scenario.education_multiplier = inputs['education_multiplier']
    scenario.tourism_multiplier = inputs['tourism_multiplier']
    scenario.hospitality_multiplier = inputs['hospitality_multiplier']

    # Estimated revenue
    scenario.vadded_avg_revenue_y1 = inputs['vadded_avg_revenue_y1']
    scenario.education_avg_revenue_y1 = inputs['education_avg_revenue_y1']
    scenario.tourism_avg_revenue_y1 = inputs['tourism_avg_revenue_y1']
    scenario.hospitality_avg_revenue_y1 = inputs['hospitality_avg_revenue_y1']

    # Estimated Opex
    scenario.monthly_rent_y1 = inputs['monthly_rent_y1']
    scenario.monthly_distribution_y1 = inputs['monthly_distribution_y1']
    scenario.monthly_rent_y2 = inputs['monthly_rent_y2']
    scenario.monthly_distribution_y2 = inputs['monthly_distribution_y2']

    # Staff
    scenario.delivery_msalary = inputs['delivery_msalary']
    scenario.farmhand_msalary = inputs['farmhand_msalary']
    scenario.parttime_wage = inputs['parttime_wage']

    scenario.ceo_msalary = inputs['ceo_msalary']
    scenario.hgrower_msalary = inputs['hgrower_msalary']
    scenario.marketer_msalary = inputs['marketer_msalary']
    scenario.scientist_msalary = inputs['scientist_msalary']
    scenario.salesperson_msalary = inputs['salesperson_msalary']
    scenario.manager_msalary = inputs['manager_msalary']
    scenario.admin_msalary = inputs['admin_msalary']

    # Staff Headcount - Pilot
    scenario.ceo_count_y1 = inputs['ceo_count_y1']
    scenario.hgrower_count_y1 = inputs['hgrower_count_y1']
    scenario.marketer_count_y1 = inputs['marketer_count_y1']

    scenario.scientist_count_y1 = inputs['scientist_count_y1']
    scenario.salesperson_count_y1 = inputs['salesperson_count_y1']
    scenario.manager_count_y1 = inputs['manager_count_y1']
    scenario.delivery_count_y1 = inputs['delivery_count_y1']
    scenario.farmhand_count_y1 = inputs['farmhand_count_y1']
    scenario.admin_count_y1 = inputs['admin_count_y1']
    scenario.parttime_count_y1 = inputs['parttime_count_y1']

    # Staff Headcount - Full-Scale
    scenario.ceo_count_y2 = inputs['ceo_count_y2']
    scenario.hgrower_count_y2 = inputs['hgrower_count_y2']
    scenario.marketer_count_y2 = inputs['marketer_count_y2']

    scenario.scientist_count_y2 = inputs['scientist_count_y2']
    scenario.salesperson_count_y2 = inputs['salesperson_count_y2']
    scenario.manager_count_y2 = inputs['manager_count_y2']
    scenario.delivery_count_y2 = inputs['delivery_count_y2']
    scenario.farmhand_count_y2 = inputs['farmhand_count_y2']
    scenario.admin_count_y2 = inputs['admin_count_y2']
    scenario.parttime_count_y2 = inputs['parttime_count_y2']

    scenario.growing_area_pilot = scenario.facility_size_pilot * scenario.percent_production_area_pilot
    scenario.stacked_growing_area_pilot = scenario.growing_area_pilot * scenario.growing_levels_pilot

    scenario.insurance_pilot = inputs['insurance_pilot']
    scenario.insurance_full = inputs['insurance_full']

    scenario.capex_pilot = inputs['capex_pilot']
    scenario.capex_full = inputs['capex_full']
    scenario.capex_lights = inputs['capex_lights']
    scenario.capex_facilities = inputs['capex_facilities']
    scenario.capex_building = inputs['capex_building']

    scenario.target_productivity_space = inputs['target_productivity_space']
    scenario.target_productivity_energy = inputs['target_productivity_energy']
    scenario.target_productivity_labour = inputs['target_productivity_labour']
    scenario.target_productivity_water = inputs['target_productivity_water']
    scenario.target_productivity_nutrients = inputs['target_productivity_nutrients']
    scenario.target_productivity_volume = inputs['target_productivity_volume']
    scenario.target_productivity_plants = inputs['target_productivity_plants']
    scenario.target_productivity_labour = inputs['target_productivity_labour']
    scenario.target_productivity_CO2_emit = inputs['target_productivity_CO2_emit']
    scenario.target_productivity_CO2_miti = inputs['target_productivity_CO2_miti']
    scenario.target_productivity_CO2_net = inputs['target_productivity_CO2_net']

    scenario.ipm = inputs['ipm']
    scenario.pest_detection = inputs['pest_detection']
    scenario.electrical_backup = inputs['electrical_backup']

    return scenario

def export_results(financial_annual_overview, financial_summary, risk_dataframe):
    """Export results function
        Notes: Defines job roles and attributes

     Args:
         financial_annual_overview (dataframe): An annual financial overview of the analysis period
         financial_summary (dataframe): A financial summary over the analysis period
         risk_dataframe (dataframe):A annual financial overview of the analysis period with risk included
     """

    with pd.ExcelWriter('/Users/Francis/PycharmProjects/VerticalFarming/results.xlsx') as writer:
        #financial_summary.to_excel(writer, "results.xlsx")
        financial_annual_overview.to_excel(writer, "results.xlsx")
        #risk_dataframe.to_excel(writer, "results.xlsx")
    return

# Staff List ( Edit this to fill in staff names)
def get_staff_list(scenario):
    """Get Staff List
        Notes: Defines job roles and attributes

     Args:
         scenario (object): The farm scenario
     Returns:
         ceo (object): CEO attributes
         headgrower (object): Head Grower attributes
         marketer (object): Marketer attributes
         scientist (object): Scientist attributes
         sales_person (object): Sales person attributes
         manager (object): Manager attributes
         delivery (object): Delivery attributes
         farmhand (object): Farm hand attributes
         admin (object): Admin attributes
         part_time (object): Part time attributes

     To Do:
     1. Add a staff list
     """

    # Staff
    staff_list=[]
    ceo = Staff('unknown', 'CEO', scenario.ceo_msalary, scenario.ceo_count_y1, scenario.ceo_count_y2, 'indirect', 0, 0)
    headgrower = Staff('Sam Bannon','Head Grower', scenario.hgrower_msalary, scenario.hgrower_count_y1, scenario.hgrower_count_y2, 'indirect', 0, 0)
    marketer = Staff('Paul Myers','Marketer', scenario.marketer_msalary, scenario.marketer_count_y1, scenario.marketer_count_y2, 'indirect', 0, 0)
    scientist = Staff('Jens Thomas', 'Scientist', scenario.scientist_msalary, scenario.scientist_count_y1, scenario.scientist_count_y2, 'indirect', 0, 0)
    sales_person = Staff('unknown', 'Sales Person', scenario.salesperson_msalary, scenario.salesperson_count_y1, scenario.salesperson_count_y2, 'indrect', 0, 0)
    manager = Staff('Jayne Goss', 'Manager', scenario.manager_msalary, scenario.manager_count_y1, scenario.manager_count_y2,'indrect', 0, 0)
    delivery = Staff('unknown', 'Delivery', scenario.delivery_msalary, scenario.delivery_count_y1, scenario.delivery_count_y2, 'direct', 0, 0)
    farmhand = Staff('unknown', 'Farm Hand', scenario.farmhand_msalary, scenario.farmhand_count_y1, scenario.farmhand_count_y2, 'direct', 0, 0)
    admin = Staff('unknown', 'Admin', scenario.admin_msalary, scenario.admin_count_y1, scenario.admin_count_y2, 'salary', 0, 0)
    part_time = Staff('unknown', 'Part-time Employee', scenario.parttime_wage, scenario.parttime_count_y1, scenario.parttime_count_y2, 'indirect', 8.72, 20)

    return ceo, headgrower, marketer, scientist, sales_person, manager, delivery, farmhand, admin, part_time       # Edit
# Date Time
def get_calendar(start_date, years):
    """Get Calendar Function

    Args:
        start_date (datetime): The date when the farm begins operations and the analysis starts
        years (int): The number of years that the analysis will look at
    Returns:
        end_date (datetime): The end date of the analysis
        timeseries_monthly (list of datetimes): A time series of monthly dates from start to end date
        timeseries_yearly (list of datetimes): A time series of annual dates from start to end date
    To Do:
    """
    start_date_counter = start_date
    end_date = start_date + relativedelta(years=years)
    month_step = relativedelta(months=1)
    year_step = relativedelta(years=1)

    timeseries_monthly = [start_date]
    timeseries_yearly = [start_date]

    while start_date_counter < end_date:
        start_date_counter += month_step
        timeseries_monthly.append(start_date_counter)

    start_date_counter = start_date

    while start_date_counter < end_date:
        start_date_counter += year_step
        timeseries_yearly.append(start_date_counter)

    return end_date, timeseries_monthly, timeseries_yearly
# Growth Plans
def get_gp(scenario):
    """Get Growth Plan

    Args:
        scenario (object): The farm scenario

    Returns:
        gp (object): The growth plan of the farm

    To Do:
    """

    gp = Growthplan()
    gp.upgrade_year = scenario.start_date + timedelta(days=days_in_year) # When scaling of pilot farm occurs
    gp.facility_size_full = scenario.facility_size_pilot * scenario.growing_area_mulitplier
    gp.percent_production_area_full = scenario.percent_production_area_pilot
    gp.growing_levels_full = scenario.growing_levels_pilot
    gp.no_lights_full = scenario.no_lights_pilot * scenario.growing_area_mulitplier
    gp.packaging_cost_full = scenario.packaging_cost_pilot
    gp.other_costs_full = scenario.other_costs_pilot
    gp.growing_area_full = scenario.growing_area_pilot * scenario.growing_area_mulitplier
    gp.stacked_growing_area_full = round(gp.growing_area_full * gp.growing_levels_full, 1)
    return gp

# CAPEX
def calc_capex(scenario, gp):

    """Calculate CAPEX Costs Function
        Note: PP. 51 of Plant Factory
        Initial cost including necessary facilities (15 tiers, 50cm distance between tiers)
        $4000 USD per sq-m x 0.8 for £

    Args:
        scenario (object): The farm scenario
        gp (object): Growth plans of farm

    Returns:
        capex_pilot (float): The capital costs associated with building the pilot farm
        capex_full (float): The capital costs associated with building the full-scale farm

    To Do:
    """

    if scenario.capex_pilot == 0:
        capex_pilot = 4000 * 0.8 * scenario.facility_size_pilot
        capex_full = 4000 * 0.8 * gp.facility_size_full
    else:
        capex_pilot = scenario.capex_pilot
        capex_full = scenario.capex_full

    return capex_pilot, capex_full

def calc_space_breakdown(scenario, gp):
    """ Space Breakdown - Gives a % breakdown based on desired farm characteristics

    args:
        scenario (object): The farm scenario

    return:
        space_breakdown (dataframe): The breakdown of different farm areas
    """
    biosecurity= 0.05
    walkways = 0.25
    walkways_with_p = 0.28
    seeding_germination = 0.124
    seeding_germination_with_p = 0.1
    nursery = 0.15
    production = 0.426
    production_with_p = 0.3
    production_scenario = scenario.percent_production_area_pilot
    processing = 0.1
    cold_storage = 0.02

    if scenario.processing_cold_storage == 'No':
        biosecurity_area = gp.facility_size_full * biosecurity
        walkway_area = gp.facility_size_full * walkways
        seeding_germination_area = gp.facility_size_full * seeding_germination
        nursery_area = gp.facility_size_full * nursery
        production_area = gp.growing_area_full

    elif scenario.processing_cold_storage == 'Yes':
        biosecurity_area = gp.facility_size_full * biosecurity
        walkway_area = gp.facility_size_full * walkways_with_p
        seeding_germination_area = gp.facility_size_full * seeding_germination_with_p
        nursery_area = gp.facility_size_full * nursery
        production_area = gp.growing_area_full
        processing_area = gp.facility_size_full * processing
        cold_storage_Area = gp.facility_size_full * cold_storage



    return space_breakdown


def calc_hvac_energy(scenario, days_in_year):
    """Heating, Ventilation and Air Cooling (HVAC) Energy Calculator
    Notes: Law of Thermodynamics: Change in Internal Energy = Heat added to the system - Work done by the system
           Q=UxSAx(Tin-Tout) x Efficiency
           To determine U-values refer to U-Value tableS: http://www.puravent.co.uk/Guide_Resources/AppendixA_UValues.pdf
    Args:
        scenario(objbect): The farm scenario
        set_points

    Returns:
        hvac_energy(list): Annual energy usage to accomodate for HVAC energy requirements

    """
    conv_factor_kJph_to_kWh = 0.00666667
    conv_factor_kJ_to_kWh = 0.000277778

    typical_U_values = {
        # Wall (outer)
        '9" solid brick': 2.2,
        '11" brick-block cavity - unfilled': 1.0,
        '11" brick-block cavity- insulated': 0.6,
        # Wall (interal)
        'plaster, 4.5 inch brick, plaster' : 2.2,
        'plaster, 4 inch heavyweight block, plaster': 2.5,
        'plaster, 4 inch lightweight block, plaster': 1.2,
        'plasterboard, 4 inch studding, plasterboard': 1.8,
        # Floor (Ground)
        'solid concrete': 0.8,
        'suspended - timber': 0.7,
        # Floors (Intermediate)
        'Plasterboard / 8 inch joist space / T & g boards - heat flow up': 1.7,
        'Plasterboard / 8 inch joist space / T & g boards - heat flow down': 1.4,
        # Roof
        'pitched with felt, 50mm insulation': 0.6,
        'pitched with felt, 100mm insulation': 0.3,
        'flat, 25mm insulation': 0.9,
        'flat, 50mm insulation': 0.7,
        # Windows
        'wooden/uvpc frame, single glazed': 5.0,
        'wooden/uvpc frame, double glazed': 2.9,
        'wooden/uvpc frame, double glazed - 20mm gap, Low-E': 1.7,
        'metal frame, single glazed': 5.8
    }



    q = 792.246 # Heat lost or gained due to outside temperature (kJ·h−1)
    u = 0.5 # Overall heat transfer coefficient (kJ·h−1·m−2·°C−1)
    sa = 406.28 # Surface area of greenhouse (m2)
    Tin = 23.9 # Inside air set point temperature (°C)
    Tout = 20 # Outside air temperature (°C)
    efficiency = 0.75  # Efficency of the heating, and air cooling system

    energy_consumption_from_HVAC = q * conv_factor_kJph_to_kWh * days_in_year



# Yields
def calc_best_yield(scenario, crop_typ1, crop_typ2, crop_typ3, crop_typ4, years):
    """Calculate Best Case Yield
    Note:
        Retrieves the best case yield for a given crop type by seeking the attribute that aligns with the system type

    Args:
        scenario (object): The farm scenario
        crop_typ1 (object): Crop type 1 that is grown on the farm
        crop_typ2 (object): Crop type 2 that is grown on the farm
        crop_typ3 (object): Crop type 3 that is grown on the farm
        crop_typ4 (object): Crop type 4 that is grown on the farm
        years (int): The number of years the analysis looks at

    Returns:
        byield_crop1 (list): The best case yield for crop type 1 as a time series
        byield_crop2 (list): The best case yield for crop type 2 as a time series
        byield_crop3 (list): The best case yield for crop type 3 as a time series
        byield_crop4 (list): The best case yield for crop type 4 as a time series

    To Do:
        1. Max yield needs to be made dependant on system selection scenario.crop1_system and corresponding attribute of object
        2. Crop type as on object is an input. Ideally crop_typ1 should be mapped onto scenario.crop_typ1 which is currently a string rather than an object.
    """

    byield_crop1 = [0]
    byield_crop2 = [0]
    byield_crop3 = [0]
    byield_crop4 = [0]
    max_yield_crop1 = crop_typ1.drip_tower
    max_yield_crop2 = crop_typ2.drip_tower
    max_yield_crop3 = crop_typ3.drip_tower
    max_yield_crop4 = crop_typ4.drip_tower

    for y in range(1, years+1):
        if y == 1:  # under upgrade year check gp.upgrade_year
            byield_crop1.append(max_yield_crop1  * scenario.stacked_growing_area_pilot * scenario.crop1_percent)
            byield_crop2.append(max_yield_crop2 * scenario.stacked_growing_area_pilot * scenario.crop2_percent)
            byield_crop3.append(max_yield_crop3 * scenario.stacked_growing_area_pilot * scenario.crop3_percent)
            byield_crop4.append(max_yield_crop4  * scenario.stacked_growing_area_pilot * scenario.crop4_percent)
        elif y > 1:
            byield_crop1.append(max_yield_crop1 * gp.stacked_growing_area_full * scenario.crop1_percent)
            byield_crop2.append(max_yield_crop2 * gp.stacked_growing_area_full * scenario.crop2_percent)
            byield_crop3.append(max_yield_crop3 * gp.stacked_growing_area_full * scenario.crop3_percent)
            byield_crop4.append(max_yield_crop4 * gp.stacked_growing_area_full * scenario.crop4_percent)

    return byield_crop1, byield_crop2, byield_crop3, byield_crop4

def calc_adjustment_factors(scenario):
    """Calculate Adjustment Factors
    Note:
        Adjustment factors are retrieved from DataFrame called Factor table. This a general way to computing reductions
        but this should be improved to consider how growth environment matches the specific crop requirements.

    Args:
        scenario (object): The farm scenario

    Returns:
        light_factor (int): The multiplier of reduction due to matching of light requirements to crops
        temp_factor (int): The multiplier of reduction due to matching of temperature requirements to crops
        nutrient_factor (int): The multiplier of reduction due to matching of nutrients requirements to crops
        co2_factor (int): The multiplier of reduction due to matching of co2 requirements to crops

    To Do:
        Currently the factors are generalised to the entire farm as opposed to comparing
        This should be adjusted according to ratios of requirements to grow environment
    """

    # Yield adjustment factors
    factor_table =  pd.DataFrame({'High': [1, 1, 1, 1, 'n/a'],
                                  'Medium': [0.9, 0.9, 0.9, 0.97, 'n/a'],
                                  'Low': [0.6, 0.85, 0.85, 0.95, 'n/a'],
                                  'Yes': ['n/a', 'n/a', 'n/a', 'n/a', 1],
                                    'No':['n/a', 'n/a', 'n/a', 'n/a', 0.9]})
    factor_table.index = ['Light Control', 'Climate Contol', 'Nutrient Control', 'Air Conditioning', 'CO2 Enrichment']

    light_factor = factor_table.loc['Light Control', scenario.lighting_control]
    temp_factor = factor_table.loc['Climate Contol', scenario.climate_control]
    nutrient_factor = factor_table.loc['Nutrient Control', scenario.nutrient_control]
    co2_factor = factor_table.loc['CO2 Enrichment', scenario.co2_enrichment]
    return light_factor, temp_factor, nutrient_factor, co2_factor

def calc_adjusted_yield(byield_crop1, byield_crop2, byield_crop3, byield_crop4, light_factor, temp_factor, nutrient_factor, co2_factor):
    ayield_crop1 = np.array(byield_crop1, dtype=int) * light_factor * temp_factor * nutrient_factor * co2_factor
    ayield_crop2 = np.array(byield_crop2, dtype=int) * light_factor * temp_factor * nutrient_factor * co2_factor
    ayield_crop3 = np.array(byield_crop3, dtype=int) * light_factor * temp_factor * nutrient_factor * co2_factor
    ayield_crop4 = np.array(byield_crop4, dtype=int) * light_factor * temp_factor * nutrient_factor * co2_factor
    return ayield_crop1, ayield_crop2, ayield_crop3, ayield_crop4

def calc_waste_adjusted_yield(scenario, ayield_crop1, ayield_crop2, ayield_crop3, ayield_crop4, years):
    """Calculate Waste Adjusted Yields Function

    Args:
        scenario (object): The farm scenario
        ayield_crop1 (list): The adjusted yields for crop 1 as a time series for X no. of years).
        ayield_crop2 (list): The adjusted yields for crop 2 as a time series for X no. of years).
        ayield_crop3 (list): The adjusted yields for crop 3 as a time series for X no. of years).
        ayield_crop4 (list): The adjusted yields for crop 4 as a time series for X no. of years).
        years (int): The number of years the analysis will look at

    Returns:
        wyield_crop1 (list): Annual waste adjusted yield of crop 1 as a time series
        wyield_crop2 (list): Annual waste adjusted yield of crop 2 as a time series
        wyield_crop3 (list): Annual waste adjusted yield of crop 3 as a time series
        wyield_crop4 (list): Annual waste adjusted yield of crop 4 as a time series

    To Do:
    """

    waste_rates = pd.DataFrame({'High': [0, 0.1254,	0.1129,	0.1016,	0.0934,	0.0860,	0.0791,	0.0728,	0.0684,	0.0643,	0.0604,	0.0568,	0.0534,	0.0502,	0.0472,	0.0444, 0.0444, 0.0444, 0.0444, 0.0444, 0.0444],
                  'Medium': [0, 0.1777, 0.1599,	0.1439,	0.1324,	0.1218,	0.1121,	0.1031,	0.0969,	0.0911,	0.0856,	0.0805,	0.0757,	0.0711,	0.0668,	0.0628,	0.0628,	0.0628,	0.0628,	0.0628,	0.0628],
                  'Low': [0, 0.2404,	0.2163,	0.1947,	0.1791,	0.1648,	0.1516,	0.1395,	0.1311,	0.1232,	0.1158,	0.1089,	0.1024,	0.0962,	0.0904,	0.0850,	0.0850,	0.0850,	0.0850,	0.0850,	0.850]})
    waste_rates.index = range(0, 21)

    # Learning curve for loop according to Dataframe
    wyield_crop1 =[]
    wyield_crop2 =[]
    wyield_crop3 =[]
    wyield_crop4 =[]
    for y in range(0, years+1):
        wyield_crop1.append(ayield_crop1[y]*(1-waste_rates.loc[y,scenario.grower_exp]))
        wyield_crop2.append(ayield_crop2[y]*(1-waste_rates.loc[y,scenario.grower_exp]))
        wyield_crop3.append(ayield_crop3[y]*(1-waste_rates.loc[y,scenario.grower_exp]))
        wyield_crop4.append(ayield_crop4[y]*(1-waste_rates.loc[y,scenario.grower_exp]))
    return wyield_crop1, wyield_crop2, wyield_crop3, wyield_crop4

def calc_no_of_plants(scenario, w1, w2, w3, w4):
    """Calculate No. of Plants Function

    Args:
        scenario (object): The farm scenario
        w1 (list): The waste-adjusted yields for crop 1 as a time series for X no. of years).
        w2 (list): The waste-adjusted yields for crop 2 as a time series for X no. of years).
        w3 (list): The waste-adjusted yields for crop 3 as a time series for X no. of years).
        w4 (list): The waste-adjusted yields for crop 4 as a time series for X no. of years).

    Returns:
        crop1_no_of_plants (list): Annual no. of crop 1 as a time series
        crop1_no_of_plants (list): Annual no. of crop 2 as a time series
        crop1_no_of_plants (list): Annual no. of crop 3 as a time series
        crop1_no_of_plants (list): Annual no. of crop 4 as a time series
        total_no_of_plants (list): Total annual no. of plants as a time series

    To Do:
    """
    crop1_no_plants = [i / scenario.crop1_harvest_weight for i in w1]
    crop2_no_plants = [i / scenario.crop2_harvest_weight for i in w2]
    crop3_no_plants = [i / scenario.crop3_harvest_weight for i in w3]
    crop4_no_plants = [i / scenario.crop4_harvest_weight for i in w4]

    total_no_of_plants = [a + b + c + d for a, b, c, d in zip(crop1_no_plants, crop2_no_plants, crop3_no_plants, crop4_no_plants)]

    return crop1_no_plants, crop2_no_plants, crop3_no_plants, crop4_no_plants, total_no_of_plants
# Revenue

def calc_produce_sales(w1, w2, w3, w4, scenario):
    """Calculate Product Sales Revenue Function

    Args:
       w1 (list): The waste-adjusted yields for crop 1 as a time series for X no. of years).
       w2 (list): The waste-adjusted yields for crop 2 as a time series for X no. of years).
       w3 (list): The waste-adjusted yields for crop 3 as a time series for X no. of years).
       w4 (list): The waste-adjusted yields for crop 4 as a time series for X no. of years).
       scenario (object): The farm scenario

    Returns:
        sales_crop1 (list): Annual sales of crop 1 as a time series
        sales_crop2 (list): Annual sales of crop 2 as a time series
        sales_crop3 (list): Annual sales of crop 3 as a time series
        sales_crop4 (list): Annual sales of crop 4 as a time series
        total_sales (list): Total annual sales as a time series

    To Do:
    """
    sales_crop1 = []
    sales_crop2 = []
    sales_crop3 = []
    sales_crop4 = []

    for x in range(0, len(w1)):
        sales_crop1.append((w1[x] * scenario.crop1_price1 * scenario.crop1_customer_percent / scenario.crop1_product_weight) + (w1[x] * scenario.crop1_price2 * (1-scenario.crop1_customer_percent) / scenario.crop1_product_weight))
        sales_crop2.append((w2[x] * scenario.crop2_price1 * scenario.crop2_customer_percent / scenario.crop2_product_weight) + (w2[x] * scenario.crop2_price2 * (1-scenario.crop2_customer_percent) / scenario.crop2_product_weight))
        sales_crop3.append((w3[x] * scenario.crop3_price1 * scenario.crop3_customer_percent / scenario.crop3_product_weight) + (w3[x] * scenario.crop3_price2 * (1-scenario.crop3_customer_percent) / scenario.crop3_product_weight))
        sales_crop4.append((w4[x] * scenario.crop4_price1 * scenario.crop4_customer_percent / scenario.crop4_product_weight) + (w4[x] * scenario.crop4_price2 * (1-scenario.crop4_customer_percent)/ scenario.crop4_product_weight))

    total_sales = [a + b + c + d for a, b, c, d in zip(sales_crop1, sales_crop2, sales_crop3, sales_crop4)]

    return sales_crop1, sales_crop2, sales_crop3, sales_crop4, total_sales
def calc_vadded_sales(scenario, years):
    """Calculate Value Added Revenue Function

    Args:
       scenario (object): The farm scenario
       years (int): The number of years the analysis will look at


    Returns:
        vadded_sales (list): Value Added Sales Revenue as a time series for each year

    To Do:
        Include associated costs as a rough estimation, should be accounted for in OpEx, however salaries are largest factor
    """


    vadded_sales = [0]
    annual_vadded_sales = scenario.vadded_avg_revenue_y1*12

    for y in range(1, years+1):
        vadded_sales.append(annual_vadded_sales)
        annual_vadded_sales *= scenario.vadded_products_multiplier

    return vadded_sales

def calc_education_rev(scenario, years):
    """Calculate Education Revenue Function

    Args:
       scenario (object): The farm scenario
       years (int): The number of years the analysis will look at


    Returns:
        education_rev (list): Tourism Revenue as a time series for each year

    To Do:
        Include randomness for education sales (frequency and amount) as a part of growth multiplier.
        Include associated costs as a rough estimation, should be accounted for in OpEx, however salaries are largest factor
    """
    education_rev = [0]
    annual_education_rev = scenario.education_avg_revenue_y1*12

    for y in range(1, years+1):
        education_rev.append(annual_education_rev)
        annual_education_rev *= scenario.education_multiplier

    return education_rev

def calc_tourism_rev(scenario, years):
    """Calculate Tourism Revenue Function

    Args:
       scenario (object): The farm scenario
       years (int): The number of years the analysis will look at


    Returns:
        tourism_rev (list): Tourism Revenue as a time series for each year

    To Do:
        Include randomness for tourism (frequency and amount) as a part of growth multiplier.
    """
    tourism_rev = [0]
    annual_tourism_rev = scenario.tourism_avg_revenue_y1*12

    for y in range(0, years):
        tourism_rev.append(annual_tourism_rev)
        annual_tourism_rev *= scenario.tourism_multiplier

    return tourism_rev

def calc_hospitality_rev(scenario, years):
    """Calculate Hospitality Revenue Function

    Args:
       scenario (object): The farm scenario
       years (int): The number of years the analysis will look at


    Returns:
        hospitality_revenue (list): Hospitality Revenue as a time series for each year

    To Do:
        Include randomness for hospitality as part of growth multiplier (frequency and amount).
    """

    hospitality_rev = [0]
    annual_hospitality = scenario.hospitality_avg_revenue_y1*12

    for y in range(1, years+1):
        hospitality_rev.append(annual_hospitality)
        annual_hospitality *= scenario.hospitality_multiplier

    return hospitality_rev

# Grants
def calc_grants_rev(years):
    """Calculate Grants Revenue Function

    Args:
       years (int): The number of years the analysis will look at
       scenario (object): The farm scenario

    Returns:
        grants_rev (list): Grants Revenue as a time series for each year
       #
    To Do:
        Incoporate a way to account for expenditure corresponding to a grant proposal. Perhaps a percentage?
        Include randomness for grant award (frequency and amount).
        Include crowdfunding
        Create a donation based function, decide whether it becomes a new revenue stream or incoporated into existing stream
    """
    grants_rev = [0]

    for y in range(1, years+1):

        annual_grant = 0

        if random.random() >= 1:
            annual_grant += 200000

        grants_rev.append(annual_grant)
    return grants_rev

# COGS

def calc_direct_labour(farmhand, delivery, part_time, years, months_in_a_year, scenario):
    """Calculate Direct Labour costs Function

    Args:
       farmhand (object): The role of farm hand and its attributes
       delivery (object): The role of delivery and its attributes
       part_time (object): The role of part-time and its attributes
       years (int): The number of years the analysis will look at
       months_in_a_year (int): The number of months in a year
       scenario (object): The farm scenario

    Returns:
        cogs_direct_labour (list): Cost of Goods Sold expenditure on Direct Labour as a time series for each year

    To Do:
        Labour efficiency improvement - Currently draws from a normal distribution for improvement of part-time hour reduction.
        requires checking and refinement.
        Hours estimation (list): Based on farm size, number of plants, etc. This will determine the amount of work needed to maintain the farm
        as well as part-time hours/wages. This should be an output
        Part-time hours  - Hours estimation will inform the amount of time required for part-time hours
    """

    cogs_direct_labour = [0]
    labour_efficency_counter = 0
    mu, sigma = scenario.labour_improvement, 2

    direct_labour = np.random.randint(2000, 2200, size=(1, 16))

    for y in range(1, years+1):

        if y == 1:
            direct_labour_cost = months_in_a_year*((farmhand.salary * farmhand.count_pilot) + (delivery.salary * delivery.count_pilot) + (part_time.count_pilot * part_time.hours * part_time.wage))
        elif y > 1:
            direct_labour_cost = months_in_a_year*((farmhand.salary * farmhand.count_full) + (delivery.salary * delivery.count_full) + (part_time.count_full * part_time.hours * part_time.wage * (1-labour_efficency_counter)))

        labour_efficency_counter += np.random.normal(mu, sigma)
        cogs_direct_labour.append(direct_labour_cost)

    return cogs_direct_labour, direct_labour

def calc_growing_media(total_sales):
    """Calculate Growing Media costs Function

    Args:
       total_sales (list): The total sales as a annual time series

    Returns:
        cogs_cogs_media (list): Cost of Goods Sold expenditure on Growing Media as a time series for each year

    To Do:
        Currently taken as an estimate as 2.5% of sales and should be improved to be dependant on growing media selected
        Similar to packaging, should take into consideration economic order quantity
    """

    percent_of_growing_media_to_sales = 0.025
    cogs_media = [i * percent_of_growing_media_to_sales for i in total_sales]

    #scenario.growing_media * price_of_media * no_of_plants
    return cogs_media
def calc_packaging(scenario, years, w1, w2, w3, w4):
    """Calculate Packaging costs Function

    Args:
       scenario (object): The farm scenario
       w1 (list): Time series of annual yields with waste_adjustment for crop 1
       w2 (list): Time series of annual yields with waste_adjustment for crop 2
       w3 (list): Time series of annual yields with waste_adjustment for crop 3
       w4 (list): Time series of annual yields with waste_adjustment for crop 4
       years (int): The no. of years the simulation will analyse


    Returns:
        cogs_packaging (list): Cost of Goods Sold expenditure on Packaging as a time series for each year

    To Do:
        Update packaging function to be more flexible and accurate
        Update for all crops, not just crop 1, 2, 3, 4
        Get costs from a table (perhaps taken from Excel spreadsheets) to take into economic order quantity
        Include order quantity as an output
    """

    cogs_packaging =[]

    for y in range(years+1):
        annual_packaging_cost = 0
        annual_packaging_cost += (w1[y] / scenario.crop1_product_weight)
        # annual_packaging_cost += (w2[y]/scenario.crop2_product_weight)
        # annual_packaging_cost += (w3[y]/scenario.crop3_product_weight)
        # annual_packaging_cost += (w4[y]/scenario.crop4_product_weight)
        if y <= 1:
            annual_packaging_cost *= scenario.packaging_cost_pilot
        elif y > 1:
            annual_packaging_cost *= scenario.packaging_cost_full
        cogs_packaging.append(annual_packaging_cost)

    return cogs_packaging

def calc_seeds_nutrients(crop1_no_of_plants, crop2_no_of_plants, crop3_no_of_plants, crop4_no_of_plants, crop1, crop2, crop3, crop4):
    """Calculate Nutrients and Seeds costs Function

    Args:
       crop1_no_of_plants (list): The number of plants of Crop 1 as a timeseries for each year
       crop2_no_of_plants (list): The number of plants of Crop 2 as a timeseries for each year
       crop3_no_of_plants (list): The number of plants of Crop 3 as a timeseries for each year
       crop4_no_of_plants (list): The number of plants of Crop 4 as a timeseries for each year
       crop1 (object): Crop 1 selected
       crop2 (object): Crop 2 selected
       crop3 (object): Crop 3 selected
       crop4 (object): Crop 4 selected

    Returns:
        cogs_seeds_nutrients (list): Cost of Goods Sold expenditure on Nutrients as a time series for each year
        nutrient_consumption (list): The amount of Nutrient consumed each year

    To Do:
        Update nutrient consumption to be realistic and not a random number generator
        Update seed costing algorithm
    """

    cogs_seeds_crop1 = [i * crop1.seed_cost * (1/crop1.germination_rate) for i in crop1_no_of_plants]
    cogs_seeds_crop2 = [i * crop2.seed_cost * (1/crop2.germination_rate) for i in crop2_no_of_plants]
    cogs_seeds_crop3 = [i * crop3.seed_cost * (1/crop3.germination_rate) for i in crop3_no_of_plants]
    cogs_seeds_crop4 = [i * crop4.seed_cost * (1/crop4.germination_rate) for i in crop4_no_of_plants]
    cogs_seeds_nutrients = [sum(x) for x in zip(cogs_seeds_crop1, cogs_seeds_crop2, cogs_seeds_crop3, cogs_seeds_crop4)]

# No nutrients YET
    nutrient_consumption = np.random.randint(900, 1100, size=(1, 16))
    #cogs_seeds_nutrients = sum(x) for x in zip(total_seeds_cost, total_nutrients_cost)

    return cogs_seeds_nutrients, nutrient_consumption


def calc_avg_photoperiod(scenario, crop1, crop2, crop3, crop4):
    """Calculate Average Photoperiod

    Args:
       scenario (object): The farm scenario
       crop1 (object): Crop 1 selected
       crop2 (object): Crop 2 selected
       crop3 (object): Crop 3 selected
       crop4 (object): Crop 4 selected

    Returns:
        avg_photoperiod (float): The average photoperiod of lights considering crop requirements and farm allocation
    """
    avg_photoperiod = (scenario.crop1_percent * crop1.photoperiod) + (scenario.crop2_percent * crop2.photoperiod) + (scenario.crop3_percent * crop3.photoperiod)+ (scenario.crop4_percent * crop4.photoperiod)
    return avg_photoperiod
def calc_electricity(scenario, gp, avg_photoperiod, light, days_in_year, years):
    """Calculate Electricity costs Function

    Args:
       scenario (object): The farm scenario
       gp (object): Growth plan for Farm
       avg_photoperiod (float): Average photoperiod of lights considering crop requirements
       light (object): The light selected by the user
       days_in_year (float): The number of days in a year
       years (int): The no. of years the simulation will analyse

    Returns:
        cogs_electricity (list): Cost of Goods Sold expenditure on Electricity as a time series for each year
        electricity_consumption (list): The amount of eletricity consumed each year

    To Do:
        Add HVAC model and remove HVAC multiplier of 1.25 for enhanced accuracy... leave multiplier as a default?
    """

    electricity_consumption =[0]
    HVAC_multiplier = 1.25

    for y in range(years+1):
        if y == 1:
            electricity_consumption.append(avg_photoperiod * light.max_power * scenario.no_lights_pilot * days_in_year/ 1000)
        elif y > 1: # Multiplied by 1.25 to accomodate HVAC upgrade
            electricity_consumption.append(avg_photoperiod * light.max_power * gp.no_lights_full * days_in_year * HVAC_multiplier/ 1000)

    cogs_electricity = [i * scenario.electricity_price for i in electricity_consumption]
    return cogs_electricity, electricity_consumption

def calc_water(scenario, years, days_in_year):
    """Calculate Water costs Function

    Args:
       scenario (object): The farm scenario
       years (int): The no. of years the simulation will analyse
       days_in_year (float): The number of days in a year

    Returns:
        cogs_water (list): Cost of Goods Sold expenditure on Water as a time series for each year
        water_consumption (list): The amount of water consumed each year
    """
    water_consumption = [0]

    for y in range(years+1):
        if y == 1:
            water_consumption.append(scenario.system_quantity * 0.95 * days_in_year + (1900*12))
        elif y > 1:
            water_consumption.append((scenario.system_quantity * 0.95 * days_in_year + (1900*12)) * scenario.growing_area_mulitplier)

    cogs_water = [i * scenario.water_price for i in water_consumption]

    return cogs_water, water_consumption

# OPEX

def calc_rent(scenario, years, month_in_a_year):
    """Calculate Rent costs Function

    Args:
       scenario (object): The farm scenario
       years (int): The no. of years the simulation will analyse
       months_in_a_year (int): The number of months in a year

    Returns:
        opex_rent (list): Operational expenditure on other costs as a time series for each year
    """
    opex_rent = [0]
    for y in range(years+1):
        if y == 1:
            opex_rent.append(scenario.monthly_rent_y1* months_in_a_year)
        elif y > 1:
            opex_rent.append(scenario.monthly_rent_y2 * months_in_a_year)

    return opex_rent

def calc_salaries(ceo, scientist, marketer, admin, manager, headgrower, sales_person, years, months_in_a_year):
    """Calculate Salaries costs Function

    Args:
       ceo (object): The role of ceo and its associated values
       scientist (object): The role of scientist and its associated values
       marketer (object): The role of marketer and its associated values
       admin (object): The role of admin and its associated values
       manager (object): The role of manager and its associated values
       headgrower (object): The role of head grower and its associated values
       sales_person (object): The role of sales person and its associated values
       years (int): The no. of years the simulation will analyse
       months_in_a_year (int)

    Returns:
        opex_salaries (list): Operational expenditure on salaries as a time series for each year
    """
    opex_salaries = [0]

    for y in range(1, years+1):

        if y == 1:
            staff_cost = months_in_a_year * (ceo.cost_pilot + scientist.cost_pilot +\
                        marketer.cost_pilot + admin.cost_pilot +\
                        manager.cost_pilot + headgrower.cost_pilot + \
                        sales_person.cost_pilot)
        elif y > 1:
            staff_cost = months_in_a_year * (ceo.cost_full + scientist.cost_full +\
                        marketer.cost_full + admin.cost_full +\
                        manager.cost_full + headgrower.cost_full + \
                        sales_person.cost_full)

        opex_salaries.append(staff_cost)

    return opex_salaries

def calc_other_costs(scenario, opex_staff, years):
    """Calculate Other costs Function

    Args:
       scenario (object): The farm scenario
       opex_staff (list): The operational costs for salaries as a time series
       years (int): The no. of years the simulation will analyse

    Returns:
        opex_other_costs (list): Operational expenditure on other costs as a time series for each year
    """
    opex_other_costs = [0]

    for y in range(1, years+1):

            opex_other_costs.append(scenario.other_costs_pilot * opex_staff[y])

    return opex_other_costs

def calc_insurance(scenario, years, months_in_a_year):
    """Calculate Insurance costs Function

    Args:
       scenario (object): The farm scenario
       years (int): The no. of years the simulation will analyse
       months_in_a_year (int): The no. of months in a year

    Returns:
        opex_insurance (list): Operational expenditure on insurance as a time series for each year
    """
    opex_insurance = [0]
    for y in range(years + 1):
        if y == 1:
            opex_insurance.append(scenario.insurance_pilot * months_in_a_year)
        elif y > 1:
            opex_insurance.append(scenario.insurance_full * months_in_a_year)

    return opex_insurance


def calc_distribution(scenario, years, months_in_a_year):
    """Calculate Distribution costs Function

    Args:
       scenario (object): The farm scenario
       years (int): The no. of years the simulation will analyse
       months_in_a_year (int): The no. of months in a year

    Returns:
        opex_distribution (list): Operational expenditure on distribution as a time series for each year
    """

    opex_distribution = [0]
    for y in range(years + 1):
        if y == 1:
            opex_distribution.append(scenario.monthly_distribution_y1 * months_in_a_year)
        elif y > 1:
            opex_distribution.append(scenario.monthly_distribution_y2 * months_in_a_year)

    return opex_distribution


# Loan

def calc_loan_repayments(scenario, years):
    """Calculate Loan Repayments and Loan Balance Function

    Args:
       scenario (object): The farm scenario
       years (int): The no. of years the simulation will analyse

    Returns:
        loan_repayments (list): Loan repayments as a time series of repayments
        loan_balance (list): Loan balance as a time series of loan balance remaining
    """


    loan_balance = [scenario.loan_amount]
    loan_repayments = [0]

    for y in range(1, years+1):

        if scenario.loan_tenure/y >= 1:
            loan_repayment = (scenario.loan_interest * scenario.loan_amount)/(1-(1+scenario.loan_interest)**(-scenario.loan_tenure))
        else:
            loan_repayment = 0

        loan_repayments.append(loan_repayment)
        loan_balance.append(round(loan_balance[y-1]-loan_repayments[y]+(loan_balance[y-1]*scenario.loan_interest),2))
    return loan_repayments, loan_balance

def calc_depreciation(scenario, lights, avg_photoperiod, years, days_in_year):

    """Calculate Depreciation Function to Compute Total Farm Depreciation each Year
       Typically accounts for 21 production costs

    Args:
       scenario (object): The farm scenario
       lights (object): The lights used on the farm
       avg_photoperiod (float): The average photoperiod of lights on the farm
       years (int): The no. of years the simulation will analyse
       days_in_year (float): The no. of days in the year

    Returns:
        depreciation (list): Depreciation as a timeseries of costs

    Notes:
    Construction - Depreciation over 15 years for building.
    Facilities   - Depreciation over 10 years for facilities.
    Lights - Depreciation over 5 years for LED (typically) but dependant for lifetime of LEDs
    """

    building_lifetime = 15
    facilities_lifetime = 10

    # Building
    building_depreciaiton_percent = 1/building_lifetime
    building_depreciation = scenario.capex_building * building_depreciaiton_percent

    # Facilities
    facilities_depreciation_percent = 1/facilities_lifetime
    facilities_depreciation = scenario.capex_facilities * facilities_depreciation_percent

    # Lights
    life_time_acceleration_factor = 0.8
    life_time = lights.life_time * life_time_acceleration_factor # Hours
    life_span = (life_time / avg_photoperiod)/days_in_year
    lights_depreciation_percent = 1/life_span
    lights_depreciation = lights_depreciation_percent * scenario.capex_lights

    # Pilot
    pilot_depreciation = (lights_depreciation+facilities_depreciation+building_depreciation)/scenario.growing_area_mulitplier

    depreciation = [0]

    for y in range(1, years+1):
        if y == 1:
            depreciation.append(pilot_depreciation)
        elif y > 1:
            depreciation.append(lights_depreciation + facilities_depreciation + building_depreciation)

    return depreciation, life_span

def calc_roi(scenario, financial_annual_overview, years):
    """Return on Investment Time Series Function

    Args:
       scenario (object): The farm scenario
       financial_annual_overview (dataframe): The corresponding financial dataframe
       years (int): No. of years the analysis will analyse

    Returns:
        roi (list): Return on investment time series for the no. of years
    """

    roi = []

    for y in range(years+1):
        #if y >= 2:
            roi.append((financial_annual_overview.iloc[30,y] / scenario.capex_full)*100)
        #elif y < 2:
        #   roi.append((financial_annual_overview.iloc[30,y] / scenario.capex_pilot)*100)

    return roi

def calc_payback_period(scenario, financial_annual_overview, years):
    """Calculating Payback Period for given Farm Scenario

            Notes:
                Computes the number of years to successfully pay off investment into the farm

            Args:
                scenario (object): Specified farm scenario
                financial_annual_overview (dataframe): Annual financial overview of important data
                years (int): Number of years for the analysis


            Returns:
                investment_balance (list): Timeseries of remaining investment balance
                pay_back_period (int): The number of years to pay off the farm or print statement about profitability

            TO DO:
                Does the investment balance straddle zero? - P-box scenario must say what proportion of P-Box is
                straddling zeros and which parameters are responsible for this.
        """

    investment_balance = [scenario.capex_full]
    payback_period_list = []

    for y in range(years):
        investment_balance.append(investment_balance[y] - financial_annual_overview.iloc[30,y+1])

        if investment_balance[y] <= 0:
            payback_period_list.append(y)
        else:
            payback_period_list.append(0)

    try:
        payback_period = payback_period_list.index(1, 0, years+1)
    except ValueError:
        payback_period = 'The Farm it not economically sustainable and will not turn a profit during the {} years of simulation'.format(years)
# Does the investment balance straddle zero - P-box scenario.
    return investment_balance, payback_period

# Financial Dataframe Construction

def build_dataframe(timeseries_yearly, timeseries_monthly):
    """Constructing financial overview dataframe

            Notes:
                Creates dataframe with indices for annual and monthly finances

            Args:
                timeseries_yearly (list): Timeseries of annual dates
                timeseries_monthly (list): Timeseries of monthly dates


            Returns:
                financial_annual_overview (dataframe): Annual financial overview of important data
                financial_monthly_overview (dataframe): Annual financial overview of important data
        """

    financial_annual_overview = pd.DataFrame(index= ['Yield Crop 1', 'Yield Crop 2', 'Yield Crop 3', 'Yield Crop 4',
                         'Revenue - Crop Sales', 'Revenue - Value-Added Products', 'Revenue - Education', 'Revenue - Tourism', 'Revenue - Hospitality', 'Revenue - Grants', 'Total Revenue',
                         'COGS - Direct Labour', 'COGS - Growing Media', 'COGS - Packaging', 'COGS - Seeds & Nutrients', 'COGS - Electricity', 'COGS - Water', 'Total COGS',                                  
                         'Gross Profit',                                                                                                                                                                      
                         'OPEX - Rent', 'OPEX - Staff (non-direct)', 'OPEX - Other Costs','OPEX - Insurance', 'OPEX - Distribution', 'Total OPEX',                                                            
                         'EBITDA',                                                                                                                                                                            
                         'Loan Repayments', 'Loan Balance', 'Taxes', 'Depreciation',                                                                                                                          
                         'Net Profit', 'Return on Investment'] ,columns=timeseries_yearly)

    financial_monthly_overview = pd.DataFrame(index= ['Yield Crop 1', 'Yield Crop 2', 'Yield Crop 3', 'Yield Crop 4',
                         'Revenue - Crop Sales', 'Revenue - Value-Added Products', 'Revenue - Education', 'Revenue - Tourism', 'Revenue - Hospitality', 'Revenue - Grants', 'Total Revenue',
                         'COGS - Direct Labour', 'COGS - Growing Media', 'COGS - Packaging', 'COGS - Seeds & Nutrients', 'COGS - Electricity', 'COGS - Water', 'Total COGS',
                         'Gross Profit',
                         'OPEX - Rent', 'OPEX - Staff (non-direct)', 'OPEX - Other Costs','OPEX - Insurance', 'OPEX - Distribution', 'Total OPEX',
                         'EBITDA',
                         'Loan Repayments', 'Loan Balance', 'Taxes', 'Depreciation',
                         'Net Profit', 'Return on Investment'] ,columns=timeseries_monthly)
    return financial_annual_overview, financial_monthly_overview

def crop_and_revenue_to_df(financial_annual_overview, w1, w2, w3, w4, total_sales):
    """Adding yields and sales information to financial overview

            Notes:
                Adds waste-adjusted yields for crops 1, 2, 3 and 4 with total sales to dataframe

            Args:
                financial_annual_overview (dataframe): An annual overview of financial data
                w1 (list): Timeseries of expected yield for crop 4
                w2 (list): Timeseries of expected yield for crop 4
                w3 (list): Timeseries of expected yield for crop 4
                w4 (list): Timeseries of expected yield for crop 4
                total_sales (list): Timeseries of total sales

            Returns:
                financial_annual_overview (dataframe): Financial overview of important data
        """

    financial_annual_overview.loc['Yield Crop 1'] = w1
    financial_annual_overview.loc['Yield Crop 2'] = w2
    financial_annual_overview.loc['Yield Crop 3'] = w3
    financial_annual_overview.loc['Yield Crop 4'] = w4
    financial_annual_overview.loc['Revenue - Crop Sales'] = total_sales
    financial_annual_overview.loc['Revenue - Value-Added Products'] = vadded_sales
    financial_annual_overview.loc['Revenue - Education'] = education_rev
    financial_annual_overview.loc['Revenue - Tourism'] = tourism_rev
    financial_annual_overview.loc['Revenue - Hospitality'] = hospitality_rev
    financial_annual_overview.loc['Revenue - Grants'] = grants_rev
    financial_annual_overview.loc['Total Revenue'] = financial_annual_overview.loc['Revenue - Grants'] + financial_annual_overview.loc['Revenue - Hospitality'] + \
                                                     financial_annual_overview.loc['Revenue - Crop Sales'] + financial_annual_overview.loc['Revenue - Value-Added Products'] + financial_annual_overview.loc['Revenue - Tourism'] \
                                                     + financial_annual_overview.loc['Revenue - Education']
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    return financial_annual_overview
def cogs_to_df(financial_annual_overview, cogs_labour, cogs_media, cogs_packaging, cogs_seeds_nutrients, cogs_electricity, cogs_water):
    """Adding Cost of Goods Sold to financial overview

            Notes:
                Adds direct labour, growing media, packaging, seeds, nutrients, electricity, water and total COGS to dataframe

            Args:
                financial_annual_overview (dataframe): An annual overview of financial data
                cogs_labour (list): Timeseries of labour costs
                cogs_media (list): Timeseries of media costs
                cogs_packaging (list): Timeseries of packaging costs
                cogs_seeds_nutrients (list): Timeseries of nutrient costs
                cogs_electricity (list): Timeseries of electricity costs
                cogs_water (list): Timeseries of water costs

            Returns:
                financial_annual_overview (dataframe): Financial overview of important data
        """

    financial_annual_overview.loc['COGS - Direct Labour'] = cogs_labour
    financial_annual_overview.loc['COGS - Growing Media'] = cogs_media
    financial_annual_overview.loc['COGS - Packaging'] = cogs_packaging
    financial_annual_overview.loc['COGS - Seeds & Nutrients'] = cogs_seeds_nutrients
    financial_annual_overview.loc['COGS - Electricity'] = cogs_electricity
    financial_annual_overview.loc['COGS - Water'] = cogs_water
    financial_annual_overview.loc['Total COGS'] = financial_annual_overview.loc['COGS - Direct Labour'] + financial_annual_overview.loc['COGS - Growing Media'] + \
                                                  financial_annual_overview.loc['COGS - Packaging'] + financial_annual_overview.loc['COGS - Seeds & Nutrients'] + \
                                                     financial_annual_overview.loc['COGS - Electricity'] + financial_annual_overview.loc['COGS - Water']
    return financial_annual_overview
def opex_to_df(financial_annual_overview, opex_rent, opex_salaries, opex_other_costs, opex_insurance, opex_distribution):
    """Adding operational expenditures to financial overview

        Notes:
            Adds rent, salaries, other costs, insurance, distribution and total OPEX to dataframe

        Args:
            financial_annual_overview (dataframe): An annual overview of financial data
            opex_rent (list): Timeseries of rent costs
            opex_salaries (list): Timeseries of salary costs
            opex_other_costs (list): Timeseries of other costs calculated as a percentage of salaries
            opex_insurance (list): Timeseries of insurance costs
            opex_distribution (list): Time series of distribution costs

        Returns:
            financial_annual_overview (dataframe): Financial overview of important data
    """

    financial_annual_overview.loc['OPEX - Rent'] = opex_rent
    financial_annual_overview.loc['OPEX - Staff (non-direct)'] = opex_salaries
    financial_annual_overview.loc['OPEX - Other Costs'] = opex_other_costs
    financial_annual_overview.loc['OPEX - Insurance'] = opex_insurance
    financial_annual_overview.loc['OPEX - Distribution'] = opex_distribution
    financial_annual_overview.loc['Total OPEX'] = financial_annual_overview.loc['OPEX - Rent'] + financial_annual_overview.loc['OPEX - Staff (non-direct)'] \
                                                  + financial_annual_overview.loc['OPEX - Other Costs'] +financial_annual_overview.loc['OPEX - Insurance'] \
                                                  + financial_annual_overview.loc['OPEX - Distribution']
    return financial_annual_overview
def extra_to_df(financial_annual_overview, loan_repayments, loan_balance, scenario, depreciation):
    """Adding calculations and final details to financial overview

        Notes:
            Adds loan repayments, loan balance, depreciation, gross profit, EBITDA, taxes and net profit to dataframe

        Args:
            financial_annual_overview (dataframe): An annual overview of financial data
            loan_repayments (list): Timeseries of loan repayments
            loan_balance (list): Timeseries of loan balance
            scenario (object): Farm scenario
            depreciation (list): Timeseries of depreciation costs

        Returns:
            financial_annual_overview (dataframe): Financial overview of important data
    """

    financial_annual_overview.loc['Gross Profit'] = financial_annual_overview.loc['Total Revenue'] - financial_annual_overview.loc['Total COGS']
    financial_annual_overview.loc['EBITDA'] = financial_annual_overview.loc['Gross Profit'] - financial_annual_overview.loc['Total OPEX']
    financial_annual_overview.loc['Loan Repayments'] = loan_repayments
    financial_annual_overview.loc['Loan Balance'] = loan_balance
    financial_annual_overview.loc['Taxes'] = scenario.tax_rate * financial_annual_overview.loc['EBITDA']
    financial_annual_overview.loc['Depreciation'] = depreciation
    financial_annual_overview.loc['Net Profit'] = financial_annual_overview.loc['EBITDA'] - financial_annual_overview.loc['Loan Repayments'] - financial_annual_overview.loc['Taxes'] - financial_annual_overview.loc['Depreciation']
    return financial_annual_overview

def build_financial_summary(financial_annual_overview, investment_balance, roi, timeseries_yearly):
    """Build financial summary

        Notes:
            Summarises key data from financial_annual_overview

        Args:
            financial_annual_overview (dataframe): An annual summary of financial data
            investment_balance (list): Timeseries of investment balance
            roi (list): Timeseries of ROI generated through farm activities
            timeseries_yearly (list): Timeseries of dates from start-date specified by user

        Returns:
            financial_summary (dataframe): Financial summary of important data
    """

    financial_summary = pd.DataFrame(index= ['Gross Revenue', 'Cost of Goods Sold', 'Total Operating Expenses', 'EBITDA', 'Loan Repayments', 'Depreciation', 'Net Profit/Loss', 'Investment Left', 'Return on Investment'], columns=timeseries_yearly)
    financial_summary.loc['Gross Revenue'] = financial_annual_overview.loc['Total Revenue']
    financial_summary.loc['Cost of Goods Sold'] = financial_annual_overview.loc['Total COGS']
    financial_summary.loc['Total Operating Expenses'] = financial_annual_overview.loc['Total OPEX']
    financial_summary.loc['EBITDA'] = financial_annual_overview.loc['Total Revenue']
    financial_summary.loc['Loan Repayments'] = financial_annual_overview.loc['Loan Repayments']
    financial_summary.loc['Depreciation'] = financial_annual_overview.loc['Depreciation']
    financial_summary.loc['Net Profit/Loss'] = financial_annual_overview.loc['Net Profit']
    financial_summary.loc['Investment Left'] = investment_balance
    financial_summary.loc['Return on Investment'] = roi
    return financial_summary

# Financial Dataframe with Risk
def build_risk_dataframe(financial_annual_overview):
    """Build risk dataframe

        Notes:
            Copies financial_annual_overview
        Args:
            financial_annual_overview (dataframe): An annual overview of financial data

        Returns:
            risk_dataframe (dataframe): An instance of a annual overview of financial data with a simulation of risk
    """

    risk_dataframe = financial_annual_overview.copy()
    return risk_dataframe

# ROI Risk Assessment Curves
def build_risk_curves(years):
    """Creating lines/curves for risk thresholds on risk assessment graph for critical, moderate, substantial and safe zones

        Notes:
            Safe zone is categorised as under moderate risk
        Args:
            years (int): No. of years for analysis

        Returns:
            critical_risk (list):
            moderate_risk (list):
            substantial_risk (list):

        TO DO:
            Allow flexibility of risk threshold definitions which are currently fixed

    """

    crit_def_prob = 0.50
    crit_def_years = 3
    sub_def_prob = 0.25
    sub_def_years = 5
    mod_def_prob = 0.1
    mod_def_years = 10

    critical_risk =[]
    substantial_risk =[]
    moderate_risk = []

    for y in range(years+1):
        critical_risk.append(y * crit_def_prob / crit_def_years)
        substantial_risk.append(y * sub_def_prob / sub_def_years)
        moderate_risk.append(y * mod_def_prob / mod_def_years)

    return critical_risk, substantial_risk, moderate_risk
def build_bankruptcy_definition(years):
    """Build a bankruptcy definition

        Notes:
            This function is set according to a line of best fit from Year 0 at -10% ROI to 10% ROI by Year 7.

        Args:
            years (int): No. of years for analysis

        Returns:
            Bankruptcy definition (list): A timeseries of the bankruptcy threshold graph

        TO DO:
        Allow flexibility of bankruptcy definition by allowing input of two data points rather than assuming (-10%, 0) and (10%, 7)

    """

    bankruptcy_definition =[]
    for y in range(years+1):
        # Threshold for bankruptcy
        if y <= 7:
            bankruptcy_definition.append(y*2.8571 - 10) # Year 0 - below 10% ROI, Year 7 - 10% ROI
        elif y > 7:
            bankruptcy_definition.append(10)

    return bankruptcy_definition


    return bankruptcy_definition

def build_risk_assessment_counter(years):
    """Build a risk counter

        Args:
            years (int): No. of years for analysis

        Returns:
            risk_counter (list): An empty list for keeping track of bankruptcy events
    """

    risk_counter = []
    for y in range(years+1):
        risk_counter.append(0)
    return risk_counter

def risk_assessment(roi, bankruptcy_definition, years, risk_counter):
    """Risk Assessment of Bankruptcy Calculation

        Args:
            roi (list): The farm scenario
            bankruptcy_definition (list): The threshold line of bankruptcy
            years (int): No. of years for analysis
            risk_counter (list): Waste-adjusted yield for crop 1
            # Investment balance (list)

        Returns:
            risk_counter (list): A counter for each year that tallies up the number of times that the ROI falls under the bankruptcy threshold

        TO DO:
        Include investment balance < 0 as a necessary requisite for bankruptcy
    """

    for y in range(years+1):

        if roi[y] < bankruptcy_definition[y]:
            risk_counter[y] += 1
        else:
            risk_counter[y] += 0

    return risk_counter
def risk_assessment_probability(risk_assessment_counter, years, simulations):
    """Risk Assessment Probability of Bankruptcy out of X Simulations

        Args:
            risk_assessment_counter (list): The farm scenario
            years (int): No. of years for analysis
            simulations (int): The number of simulations for Montecarlo Analysis

        Returns:
            risk_assessment_probability (list): Timeseries of probabiltiy of simulations that go bankrupt
    """

    risk_assessment_probability = risk_assessment_counter

    for y in range(years+1):
        risk_assessment_probability[y] /= simulations

    return risk_assessment_probability

# Risks
def calc_pathogen_outbreak(scenario, years, w1, w2, w3, w4):
    """RISK: Pathogen outbreak on the farm

        Args:
            scenario (object): The farm scenario
            years (int): No. of years for analysis
            w1 (list): Waste-adjusted yield for crop 1
            w2 (list): Waste-adjusted yield for crop 2
            w3 (list): Waste-adjusted yield for crop 3
            w4  (list): Waste-adjusted yield for crop 4

        Returns:
            w1_risk (list): Adjusted yield for crop 1 with pathogen risk
            w2_risk (list): Adjusted yield for crop 2 with pathogen risk
            w3_risk (list): Adjusted yield for crop 3 with pathogen risk
            w4_risk (list): Adjusted yield for crop 4 with pathogen risk

        Uncertainty Notes:
             Reduced yield for a given month
             Max: 100% reduced yield
             Minimum: 5%
             AVG: 15%
             Std Dev: 4
             Frequency: 1x a year
             Cause: Low grower experience/low humditiy control increase risk of disease
    """

    if scenario.biosecurity_level == 'High':
        p_outbreak = 0.05 # Probability of outbreak for a given year
        p_no_outbreak = 0.95 # Probability of no outbreak for a given year
        pathogen_occurence = np.random.choice(2, years, p=[p_no_outbreak, p_outbreak])
    elif scenario.biosecurity_level == 'Medium':
        p_outbreak = 0.1 # Probability of outbreak for a given year
        p_no_outbreak = 0.9 # Probability of no outbreak for a given year
        pathogen_occurence = np.random.choice(2, years, p=[p_no_outbreak, p_outbreak])

    elif scenario.biosecurity_level == 'Low' or scenario.climate_control == 'Low':
        p_outbreak = 0.2 # Probability of outbreak for a given year
        p_no_outbreak = 0.8 # Probability of no outbreak for a given year
        pathogen_occurence = np.random.choice(2, years, p=[p_no_outbreak, p_outbreak])

    elif scenario.biosecurity_level == 'Low' and scenario.climate_control == 'Low':
        p_outbreak = 0.25 # Probability of outbreak for a given year
        p_no_outbreak = 0.75 # Probability of no outbreak for a given year
        pathogen_occurence = np.random.choice(2, years, p=[p_no_outbreak, p_outbreak])

    pathogen_occurence = [0, *pathogen_occurence]

    pathogen_outbreak =[]

    for y in range(years+1):

        if pathogen_occurence[y] == 1:
            pathogen_outbreak.append(np.random.beta(8, 2))
        else:
            pathogen_outbreak.append(1)

    w1_risk = [a * b for a, b in zip(w1, pathogen_outbreak)]
    w2_risk = [a * b for a, b in zip(w2, pathogen_outbreak)]
    w3_risk = [a * b for a, b in zip(w3, pathogen_outbreak)]
    w4_risk = [a * b for a, b in zip(w4, pathogen_outbreak)]

    return w1_risk, w2_risk, w3_risk, w4_risk

def calc_repairs(scenario, years):
    """RISK: Repairs of equipment on the farm

        Args:
            scenario (object): The farm scenario
            years (int): No. of years for analysis

        Returns:
            repair (list): Repair costs taken as a percentage of capital costs for facilities and lighting

        Uncertainty Notes:
            After 12 months
            Max: 20% of equipment
            Minimum: 0.2% of equipment
            AVG: 1%
            Std Dev: 4
            Frequency: 2x a year
            Typical case: high automation, higher repair costs
    """

    if   scenario.automation_level == 'High':
        p_small_repair = 0.65 # Probability of small repair for a given year
        p_big_repair = 0.02 # Probability of a big repair for a given year
        p_no_repair = 0.33 # Probability of no repair needed for a given year
        repair_occurence = np.random.choice(3, years, p=[p_no_repair, p_small_repair, p_big_repair])
    elif scenario.automation_level == 'Medium':
        p_small_repair = 0.45  # Probability of small repair for a given year
        p_big_repair = 0.01  # Probability of a big repair for a given year
        p_no_repair = 0.54  # Probability of no repair needed for a given year
        repair_occurence = np.random.choice(3, years, p=[p_no_repair, p_small_repair, p_big_repair])
    elif scenario.automation_level == 'Low':
        p_small_repair = 0.4  # Probability of small repair for a given year
        p_big_repair = 0.002  # Probability of a big repair for a given year
        p_no_repair = 0.598  # Probability of no repair needed for a given year
        repair_occurence = np.random.choice(3, years, p=[p_no_repair, p_small_repair, p_big_repair])

    repair_occurence = [0, 0, *repair_occurence]

    repair = []

    for y in range(years+1):

        if repair_occurence[y] == 1:
            repair.append((scenario.capex_lights + scenario.capex_facilities) * np.random.beta(0.5, 40))
        elif repair_occurence == 2:
            repair.append((scenario.capex_lights + scenario.capex_facilities) * np.random.beta(1.5, 8))
        else:
            repair.append(0)

    return repair
#
def calc_customer_withdrawal(scenario, years, total_sales):
    """RISK: Customer contract withdrawal (i.e. list individual customers or supermarket pulls order)

        Args:
            scenario (object): The farm scenario
            years (int): No. of years for analysis
            total_sales (list): Total sales for all crops every year

        Returns:
            customer_withdrawal (list): Customer withdrawals as a percentage of annual total sales to be deducted from total sales.

        Uncertainty Notes:
           Max: 30% Revenue
           Min: 1% revenue
           AVG: 5%
           Std Dev: 8
           Frequency: 1x every 2 years
           Typical case: To retail business model
    """

    if  scenario.business_model == 'Wholesale':
        p_withdrawal = 0.05  # Probability of customer withdrawal for given year
        p_no_withdrawal = 0.95  # Probability of no withdrawal for given year
        customer_withdrawal_occurrence = np.random.choice(2, years, p=[p_withdrawal, p_no_withdrawal])
    elif scenario.business_model == 'Retail':
        p_withdrawal = 0.05  # Probability of customer withdrawal for given year
        p_no_withdrawal = 0.95   # Probability of no withdrawal for given year
        customer_withdrawal_occurrence = np.random.choice(2, years, p=[p_withdrawal, p_no_withdrawal])
    elif scenario.business_model == 'Hybrid':
        p_withdrawal = 0.05  # Probability of customer withdrawal for given year
        p_no_withdrawal = 0.95 # Probability of no withdrawal for given year
        customer_withdrawal_occurrence = np.random.choice(2, years, p=[p_withdrawal, p_no_withdrawal])

    customer_withdrawal_occurrence = [0, *customer_withdrawal_occurrence]

    customer_withdrawal = []

    for y in range(years+1):

        if customer_withdrawal_occurrence[y] == 1 and scenario.business_model == 'Wholesale':
            customer_withdrawal.append(total_sales[y] * np.random.beta(5, 10))
        elif customer_withdrawal_occurrence[y] == 1 and scenario.business_model == 'Retail':
            customer_withdrawal.append(total_sales[y] * np.random.beta(0.5, 40))
        elif customer_withdrawal_occurrence[y] == 1 and scenario.business_model == 'Hybrid':
            customer_withdrawal.append(total_sales[y] * np.random.beta(1, 20))
        else:
            customer_withdrawal.append(0)

    return customer_withdrawal
#
def labour_challenges(scenario, years, total_sales, cogs_labour):
    """RISK: Calculating likelihood and impact of labour challenges

        Args:
            scenario (object): The farm scenario
            years (int): No. of years for analysis
            total_sales (list): Total sales for all crops every year
            cogs_labour (list) Total expenses for direct labour (cost of goods sold)

        Returns:
            labour_damage (list): Damage to crops or equipment as a percentage of total sales through acciedents or sabotage
            labour_labour_extra_cost (list): Increased cost due to underestimated labour costs (farmhands, delivery or part-time labour)

        Uncertainty Notes:
        High labour costs, reduced yield
        Max: 5% more labour, reduced yield (1 month)
        AVG: 15%
        Std Dev: 5
        Frequency: Continous after 6 months
        Cause: Low automation, high no. of tiers
    """

    if scenario.automation_level == 'High':
        p_sabotage = 0.01  # Probability of a labour mistake resulting in lost crop
        p_extra_cost = 0.05  # Probability of underestimated labour costs
        p_no_issue = 0.94  # Probability of no problem
        labour_challenge_occurence = np.random.choice(3, years, p=[p_no_issue, p_sabotage, p_extra_cost])
    elif scenario.automation_level == 'Medium':
        p_sabotage = 0.03  # Probability of a labour mistake resulting in lost crop
        p_extra_cost = 0.07  # Probability of underestimated labour costs
        p_no_issue = 0.9  # Probability of no problem
        labour_challenge_occurence = np.random.choice(3, years, p=[p_no_issue, p_sabotage, p_extra_cost])
    elif scenario.automation_level == 'Low':
        p_sabotage = 0.07  # Probability of a labour mistake resulting in lost crop
        p_extra_cost = 0.15  # Probability of underestimated labour costs
        p_no_issue = 0.78  # Probability of no problem
        labour_challenge_occurence = np.random.choice(3, years, p=[p_no_issue, p_sabotage, p_extra_cost])

    labour_challenge_occurence = [0, *labour_challenge_occurence]

    labour_damage = []
    labour_extra_cost = []

    for y in range(years + 1):
        if labour_challenge_occurence[y] == 0:
            labour_damage.append(0)
            labour_extra_cost.append(0)
        elif labour_challenge_occurence[y] == 1:
            labour_damage.append(total_sales[y] * np.random.beta(0.5, 50))
            labour_extra_cost.append(0)
        elif labour_challenge_occurence[y] == 2:
            labour_damage.append(0)
            labour_extra_cost.append(cogs_labour[y] * np.random.beta(10, 50))

    return labour_damage, labour_extra_cost

def reduced_product_quality(scenario):
    """Reduced Product Quality
        reduced yield
        Max: 20% price reduction
        Minimum: 5%
        AVG: 15%
        Std Dev: 3
        Frequency: 2x a year
        Cause: First year, low grower experience, no climate control
    """

    return reduced_product_quality

def calc_pest_outbreak(scenario, years, w1, w2, w3, w4):
    """RISK: Pest outbreak on the farm

        Args:
            scenario (object): The farm scenario
            years (int): No. of years for analysis
            w1 (list): Waste-adjusted yield for crop 1
            w2 (list): Waste-adjusted yield for crop 2
            w3 (list): Waste-adjusted yield for crop 3
            w4  (list): Waste-adjusted yield for crop 4

        Returns:
            w1_risk (list): Adjusted yield for crop 1 with pathogen risk
            w2_risk (list): Adjusted yield for crop 2 with pathogen risk
            w3_risk (list): Adjusted yield for crop 3 with pathogen risk
            w4_risk (list): Adjusted yield for crop 4 with pathogen risk

        Notes:
            Pest Outbreak
            reduced yield
            Max: 100% reduced yield/month
            Minimum: 0
            AVG: 10%
            Std Dev: 4
            Frequency: 1x a year
            Cause: Poor insulation, no IPM, low humidity control
            Preventitive: High insulation, high humditity control, IPM, Pest detection technology
        """

    if scenario.climate_control == 'High' and scenario.insulation_level == 'High' and scenario.pest_detection == 'Yes':
        p_outbreak = 0.005 # Probability of pest outbreak for a given year
        p_no_outbreak = 0.995 # Probability of no pest outbreak for a given year
        pest_occurence = np.random.choice(2, years, p=[p_no_outbreak, p_outbreak])
    elif scenario.climate_control == 'High' and scenario.insulation_level == 'High' and scenario.pest_detection == 'No':
        p_outbreak = 0.05 # Probability of pest outbreak for a given year
        p_no_outbreak = 0.95 # Probability of no pest outbreak for a given year
        pest_occurence = np.random.choice(2, years, p=[p_no_outbreak, p_outbreak])
    elif scenario.climate_control == 'Medium' or scenario.insulation_level == 'Medium' or scenario.pest_detection == 'No':
        p_outbreak = 0.2 # Probability of pest outbreak for a given year
        p_no_outbreak = 0.8 # Probability of no pest outbreak for a given year
        pest_occurence = np.random.choice(2, years, p=[p_no_outbreak, p_outbreak])
    elif scenario.climate_control == 'Low' or scenario.insulation_level == 'Low' and scenario.pest_detection == 'No':
        p_outbreak = 0.35 # Probability of pest outbreak for a given year
        p_no_outbreak = 0.65 # Probability of no pest outbreak for a given year
        pest_occurence = np.random.choice(2, years, p=[p_no_outbreak, p_outbreak])
    elif scenario.climate_control == 'Low' and scenario.insulation_level == 'Low' and scenario.pest_detection == 'No' :
        p_outbreak = 0.4 # Probability of pest outbreak for a given year
        p_no_outbreak = 0.6 # Probability of no pest outbreak for a given year
        pest_occurence = np.random.choice(2, years, p=[p_no_outbreak, p_outbreak])

    pest_occurence = [0, *pest_occurence]

    pest_outbreak =[]

    for y in range(years+1):

        if pest_occurence[y] == 1:
            if scenario.ipm == 'No':
                pest_outbreak.append(np.random.beta(60, 0.5))
            elif scenario.ipm == 'Yes':
                pest_outbreak.append(np.random.beta(120, 0.3))
        else:
            pest_outbreak.append(1)

    w1_risk = [a * b for a, b in zip(w1, pest_outbreak)]
    w2_risk = [a * b for a, b in zip(w2, pest_outbreak)]
    w3_risk = [a * b for a, b in zip(w3, pest_outbreak)]
    w4_risk = [a * b for a, b in zip(w4, pest_outbreak)]

    return w1_risk, w2_risk, w3_risk, w4_risk

def competitors_risk():
#         """Competitor
#             reduced revenue
#             Max: 25% revenue
#             Minimum: 0
#             AVG: 5%
#             Std Dev: 4
#             Frequency: Low
#             Cause: Crop/business model dependant
#         """
    return competitors_risk

def calc_power_outage(scenario, years, w1, w2, w3, w4):
    """RISK: Power Outage
    Notes: A power outage can be caused by:
     - excessive wind generation
     - power line fault
     - a brownout: a drop in voltage in electrical power supply
     = a blackout: total loss of power to an area
     - Electrics tripped due to circuit overloads, short circuits or ground fault surgers
    - Witihout back-up protection an aeroponic system would be at high-risk of losing an entire farm's crops
    Damage: 1 month's yield lost
    Cause: Aeroponic system without back-up

    Args:
        scenario (object): The farm scenario
        years (int): No. of years for analysis
        w1 (list): Waste-adjusted yield for crop 1
        w2 (list): Waste-adjusted yield for crop 2
        w3 (list): Waste-adjusted yield for crop 3
        w4  (list): Waste-adjusted yield for crop 4

    Returns:
        w1_risk (list): Adjusted yield for crop 1 with pathogen risk
        w2_risk (list): Adjusted yield for crop 2 with pathogen risk
        w3_risk (list): Adjusted yield for crop 3 with pathogen risk
        w4_risk (list): Adjusted yield for crop 4 with pathogen risk
    """

    months_harvest = 1/12

    p_outage = 0.05  # Probability of one power outage for a given year
    p_two_outage = 0.01  # Probability of two power outages for a given year
    p_no_outage = 0.94  # Probability of no power outage for a given year
    power_outage = np.random.choice(3, years, p=[p_no_outage, p_outage, p_two_outage])

    power_outage = [x * months_harvest for x in power_outage]

    if scenario.electrical_backup == 'No':

        if scenario.crop1_system == 'Aeroponics':
            w1_risk = [a * b for a, b in zip(w1, power_outage)]
        else:
            w1_risk = w1

        if scenario.crop2_system == 'Aeroponics':
            w2_risk = [a * b for a, b in zip(w2, power_outage)]
        else:
            w2_risk = w2

        if scenario.crop3_system == 'Aeroponics':
            w3_risk = [a * b for a, b in zip(w3, power_outage)]
        else:
            w3_risk = w3

        if scenario.crop4_system == 'Aeroponics':
            w4_risk = [a * b for a, b in zip(w4, power_outage)]
        else:
            w4_risk = w4

    else:
        w1_risk = w1
        w2_risk = w2
        w3_risk = w3
        w4_risk = w4

    return w1_risk, w2_risk, w3_risk, w4_risk

def calc_planning_delay(risk_dataframe, timeseries_yearly, years):
    """RISK: Calculate Planning Delay
        A planning delay results in scaling up from pilot to full-scale farm is delayed by X years

    args:
        risk_dataframe (dataframe): The financial annual overview including risk
        annual_timeseries (list): List of dates for simulation
        years (int): Number of years that the analysis runs for

    return:
        risk_dataframe (dataframe): updated risk dataframe
    """

    p_delay = 0.15  # Probability of planning permission delay by one year
    p_no_delay = 0.85  # Probability of no planning permission delay
    delay_occurence = np.random.choice(2, 1, p=[p_no_delay, p_delay])

    if delay_occurence == 1:
        risk_dataframe = risk_dataframe.drop(columns=timeseries_yearly[2])
        risk_dataframe.insert(loc=2, column=timeseries_yearly[2], value=risk_dataframe.iloc[:,1], allow_duplicates = False)

    return risk_dataframe

# Opportunities

def improved_labour_efficiency():
#         """Improved labour efficency
#             Reduction in hours
#             Max: 60% reduction in COGS - direct labour
#             Minimum: 0
#             AVG: 30%
#             Std Dev: 2
#             Frequency: over 6 years
#             Cause: further capex introduction of automation and manufacturing principles
#         """
    return labour_efficiency


def calc_improved_light_efficiency(scenario, gp, avg_photoperiod, lights, life_span, electricity_consumption, days_in_year):
    """Opportunity: Light Efficiency Improvement when Lights depreciated and replaced

    Notes:
        Haitz' Law
        Every decade, the cost per lumen falls by a factor of 10,
        and the amount of light generated per LED package increases by a factor of 20
        Diode efficiency increases
        Water cooling technologies to decrease heat output

    Args:
        scenario (object): The farm scenario
        gp (object): The growth plan of the farm
        avg_photoperiod (float): average photoperiod for plant requirements
        lights (object): The light specified by the user
        life_span (float): The life span of the light fixtures before it requires replacing
        electricity_consumption (list): The annual electricity consumption
        days_in_year (float): The number of days in a year


    Returns:
        wattage_requirement (float): The new wattage requirement for replacement lights based on improved light efficiency

        Max: 50% reduction in COGS - direct labour
        Minimum: 10
        AVG: 30% # 30% efficiency improvement
        Std Dev: 3
        Frequency: After LEDs depreciate
        Cause: After LEDs depreciated update better lights
    """
    HVAC_multiplier = 1.25
    mu, sigma = 0.7, 0.08
    s = np.random.normal(mu, sigma)
    new_wattage_requirement = s * lights.max_power
    life_span = math.ceil(life_span)

    new_lights_consumption = (avg_photoperiod * new_wattage_requirement * gp.no_lights_full * days_in_year)

    for y in range(life_span, years):
            electricity_consumption[y+1] = (new_lights_consumption * HVAC_multiplier)/ 1000

    cogs_electricity = [i * scenario.electricity_price for i in electricity_consumption]

    return cogs_electricity, electricity_consumption



def calc_consumer_sentiment(scenario, years, total_sales):
    """OPPORTUNITY: Consumer Sentiment - Increasing consumer sentiment and increasing sales of products

        Args:
            scenario (object): The farm scenario
            years (int): No. of years for analysis
            total_sales (list): Waste-adjusted yield for crop 1

        Returns:
           total_sales (list): Adjusted sales with market sentiment included
    """



# Productivity Metrics
def calc_productivity_metrics(timeseries_yearly, w1, w2, w3, w4, electricity_consumption, direct_labour,
                              water_consumption, staff, nutrient_consumption, no_of_plants):

    """Calculating Productivity Metrics for the Farm

        Args:
           timeseries_yearly (list): The farm scenario
           w1 (list): The corresponding financial dataframe
           w2 (list): No. of years the analysis will analyse
           w3 (list)
           w4 (list)
           electricity_consumption (list)
           direct_labour (list)
           water_consumption (list)
           staff (object)
           nutrient_consumption (list)
           no_of_plants (list)

        Returns:
            list: Return on investment time series for the no. of years

        Notes:
            Water
            Information about water usage of conventional farming compared to hydroponic or vertical farming methods has been studied by Barbosa (2015).
            Water usage depends on application method and crop. For lettuce conventionally grown, uses approximately 250 L/kg/year, whilst hydroponic methods use 20 L/kg/year. For 41,000kg yield per year, the usage is compared

            Energy
            Energy to CO2e https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2019
            Conversion factor from kJ to kWh 0.000277778
            conversion factor from kJ/h to kWh 0.00666667
            Assumption of energy used from HVAC system in Vertical farm per year	1927.799564 kWh/year
            Assumption of energy used for conventionally grown lettuce	1100        1100 kJ/kg/y
            Assumption of energy used for hydroponic  greenhouse grown lettuce	90000 kJ/kg/y
        """

    kg_of_CO2e_per_kwh = 0.283  # https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2019
    tonnes = 1000
    millions_of_litres = 1000000
    kg_of_co2e_per_million_litres = 344
    litres_per_kg_annual = 20
    conventional_water_multiplier = 0.1  # Typically hydroponics is uses 10% less water than conventional farming

    productivity_metrics = pd.DataFrame(
        index=['Total Yield (kg)', 'Energy Consumption (kWh)', 'Direct Labour (man-hours)', 'Water Consumption (L)',
               'Nutrient Consumption (kg)', 'No. of Plants', 'CO2 Emitted (kg CO2e)', 'CO2 Mitigated (kg CO2e)',
               'Net CO2 (kg CO2e)'], columns=timeseries_yearly)

    productivity_metrics.loc['Total Yield (kg)'] = [a + b + c + d for a, b, c, d in zip(w1, w2, w3, w4)]
    productivity_metrics.loc['Energy Consumption (kWh)'] = electricity_consumption
    productivity_metrics.loc['Direct Labour (man-hours)'] = direct_labour
    productivity_metrics.loc['Water Consumption (L)'] = water_consumption
    productivity_metrics.loc['Nutrient Consumption (kg)'] = nutrient_consumption
    productivity_metrics.loc['No. of Plants'] = no_of_plants

    productivity_co2_emit_energy = (productivity_metrics.loc['Energy Consumption (kWh)'] * (
                1 - scenario.percentage_renewable_energy) * kg_of_CO2e_per_kwh / tonnes)
    productivity_co2_emit_water = (((productivity_metrics.loc[
                                         'Water Consumption (L)'] / millions_of_litres) * kg_of_co2e_per_million_litres) / tonnes)

    productivity_metrics.loc['CO2 Emitted (kg CO2e)'] = productivity_co2_emit_energy + productivity_co2_emit_water

    productivity_co2_miti_energy = ((productivity_metrics.loc[
                                         'Energy Consumption (kWh)'] * scenario.percentage_renewable_energy * kg_of_CO2e_per_kwh) / tonnes)
    productivity_co2_miti_water = ((((productivity_metrics.loc[
                                          'Water Consumption (L)'] / conventional_water_multiplier) / millions_of_litres) * kg_of_co2e_per_million_litres) / tonnes)

    productivity_metrics.loc['CO2 Mitigated (kg CO2e)'] = productivity_co2_miti_energy + productivity_co2_miti_water
    productivity_metrics.loc['Net CO2 (kg CO2e)'] = productivity_metrics.loc['CO2 Mitigated (kg CO2e)'] - \
                                                    productivity_metrics.loc['CO2 Emitted (kg CO2e)']

    return productivity_metrics


def calc_crop_productivity_metrics(productivity_metrics, gp, scenario):
    """Calculating Crop Productivity Metrics for the Farm

        Args:
           productivity_metrics (dataframe): Productivity metrics
           gp (object): The growth plan of the farm
           scenario (object): The farm scenario

        Returns:
            dataframe: crop productivity metrics for space, labour, nutrients, no. of plants, and co2
    """

    crop_productivity_metrics = productivity_metrics.copy()
    crop_productivity_metrics.rename(
        index={0: 'Crop Productivity per Unit Area', 1: 'Crop Productivity per Unit Energy',
               2: 'Crop Productivity per Unit Labour', 3: 'Crop Productivity per Unit Water',
               4: 'Crop Productivity per Unit Nutrient', 5: 'Crop Productivity per Unit Growing Volume',
               6: 'No. of Plants per unit area', 7: 'Yield per kg CO2 emitted', 8: 'Yield per kg CO2 mitigated',
               8: 'Yield per kg Net CO2e'}, inplace=True)
    crop_productivity_metrics.loc['Crop Productivity per Unit Area'] = productivity_metrics.loc[
                                                                           'Total Yield (kg)'] / gp.growing_area_full
    crop_productivity_metrics.loc['Crop Productivity per Unit Energy'] = productivity_metrics.loc['Total Yield (kg)'] / \
                                                                         productivity_metrics.loc[
                                                                             'Energy Consumption (kWh)']
    crop_productivity_metrics.loc['Crop Productivity per Unit Labour'] = productivity_metrics.loc['Total Yield (kg)'] / \
                                                                         productivity_metrics.loc[
                                                                             'Direct Labour (man-hours)']
    crop_productivity_metrics.loc['Crop Productivity per Unit Water'] = productivity_metrics.loc['Total Yield (kg)'] / \
                                                                        productivity_metrics.loc[
                                                                            'Water Consumption (L)']
    crop_productivity_metrics.loc['Crop Productivity per Unit Nutrients'] = productivity_metrics.loc[
                                                                                'Total Yield (kg)'] / \
                                                                            productivity_metrics.loc[
                                                                                'Nutrient Consumption (kg)']
    crop_productivity_metrics.loc['Crop Productivity per Unit Growing Volume'] = productivity_metrics.loc[
                                                                                     'Total Yield (kg)'] / (
                                                                                             gp.growing_area_full * scenario.ceiling_height)
    crop_productivity_metrics.loc['No. of Plants per unit area'] = productivity_metrics.loc['No. of Plants'] / (
                gp.growing_area_full * scenario.ceiling_height)
    crop_productivity_metrics.loc['Yield per kg CO2 emitted'] = productivity_metrics.loc['Total Yield (kg)'] / \
                                                                productivity_metrics.loc['CO2 Emitted (kg CO2e)']
    crop_productivity_metrics.loc['Yield per kg CO2 mitigated'] = productivity_metrics.loc['Total Yield (kg)'] / \
                                                                  productivity_metrics.loc['CO2 Mitigated (kg CO2e)']
    crop_productivity_metrics.loc['Yield per kg Net CO2e'] = productivity_metrics.loc['Total Yield (kg)'] / \
                                                             productivity_metrics.loc['Net CO2 (kg CO2e)']
    return crop_productivity_metrics


def productivity_targets(crop_productivity_metrics, scenario):
    """Calculating Crop Productivity Metrics Normalised accoridng to User Targets

        Args:
           crop_productivity_metrics (dataframe): Crop Productivity metrics
           scenario (object): The farm scenario

        Returns:
            dataframe: Productivity metrics normalised to targets ready for radar chart plotting
    """

    normalised_area = crop_productivity_metrics.loc['Crop Productivity per Unit Area',
                      :] / scenario.target_productivity_space
    normalised_energy = crop_productivity_metrics.loc['Crop Productivity per Unit Energy',
                        :] / scenario.target_productivity_energy
    normalised_labour = crop_productivity_metrics.loc['Crop Productivity per Unit Labour',
                        :] / scenario.target_productivity_labour
    normalised_water = crop_productivity_metrics.loc['Crop Productivity per Unit Water',
                       :] / scenario.target_productivity_water
    normalised_nutrients = crop_productivity_metrics.loc['Crop Productivity per Unit Nutrients',
                           :] / scenario.target_productivity_nutrients
    normalised_growing_volume = crop_productivity_metrics.loc['Crop Productivity per Unit Growing Volume',
                                :] / scenario.target_productivity_volume
    normalised_plants = crop_productivity_metrics.loc['No. of Plants per unit area',
                        :] / scenario.target_productivity_plants
    normalised_net_co2 = crop_productivity_metrics.loc['Yield per kg Net CO2e',
                         :] / scenario.target_productivity_CO2_net

    normalised_productivity_targets = pd.DataFrame({
        'metric': ['A', 'B'],
        'Yield/Unit Area': [normalised_area[-1], 1],
        'Yield/Unit Energy': [normalised_energy[-1], 1],
        'Yield/Unit Labour': [normalised_labour[-1], 1],
        'Yield/Unit Water': [normalised_water[-1], 1],
        'Yield/Unit Nutrients': [normalised_nutrients[-1], 1],
        'Yield/Unit Grow Volume': [normalised_growing_volume[-1], 1],
        '# Plants/Unit Area': [normalised_plants[-1], 1],
        'Yield/kg Net CO2e': [normalised_net_co2[-1], 1]
    })

    return normalised_productivity_targets


scenario = get_scenario()
ceo, headgrower, marketer, scientist, sales_person, manager, delivery, farmhand, admin, part_time = get_staff_list(scenario)
end_date, timeseries_monthly, timeseries_yearly = get_calendar(scenario.start_date, years)
gp = get_gp(scenario)
staff_list = get_staff_list(scenario)
capex_pilot, capex_full = calc_capex(scenario, gp)
risk_counter = build_risk_assessment_counter(years)

#scenario.electricity_price = pba.norm(0.6, 0.1)

byield_crop1, byield_crop2, byield_crop3, byield_crop4 = calc_best_yield(scenario, lettuce_fu_mix, basil_lemon, basil_genovese, none, years)
light_factor, temp_factor, nutrient_factor, co2_factor = calc_adjustment_factors(scenario)
ayield_crop1, ayield_crop2, ayield_crop3, ayield_crop4 = calc_adjusted_yield(byield_crop1, byield_crop2, byield_crop3, byield_crop4, light_factor, temp_factor, nutrient_factor, co2_factor)
w1, w2, w3, w4 = calc_waste_adjusted_yield(scenario, ayield_crop1, ayield_crop2, ayield_crop3, ayield_crop4, years)
crop1_no_of_plants, crop2_no_of_plants, crop3_no_of_plants, crop4_no_of_plants, total_no_of_plants = calc_no_of_plants(scenario, w1, w2, w3, w4)
sales_crop1, sales_crop2, sales_crop3, sales_crop4, total_sales = calc_produce_sales(w1, w2, w3, w4, scenario)
vadded_sales = calc_vadded_sales(scenario, years)
education_rev = calc_education_rev(scenario, years)
tourism_rev = calc_tourism_rev(scenario, years)
hospitality_rev = calc_hospitality_rev(scenario, years)
grants_rev = calc_grants_rev(years)

cogs_labour, direct_labour = calc_direct_labour(farmhand, delivery, part_time, years, months_in_a_year, scenario)
cogs_media = calc_growing_media(total_sales)
cogs_packaging = calc_packaging(scenario, years, w1, w2, w3, w4)
cogs_seeds_nutrients, nutrient_consumption = calc_seeds_nutrients(crop1_no_of_plants, crop2_no_of_plants, crop3_no_of_plants, crop4_no_of_plants, lettuce_fu_mix, basil_lemon, basil_genovese, none)
avg_photoperiod = calc_avg_photoperiod(scenario, lettuce_fu_mix, basil_lemon, basil_genovese, basil_genovese)
cogs_electricity, electricity_consumption = calc_electricity(scenario, gp, avg_photoperiod, Spectra_Blade_Single_Sided_J, days_in_year, years)
cogs_water, water_consumption = calc_water(scenario, years, days_in_year)

opex_rent = calc_rent(scenario, years, months_in_a_year)
opex_salaries = calc_salaries(ceo, scientist, marketer, admin, manager, headgrower, sales_person, years, months_in_a_year)
opex_other_costs = calc_other_costs(scenario, opex_salaries, years)
opex_insurance = calc_insurance(scenario, years, months_in_a_year)
opex_distribution = calc_distribution(scenario, years, months_in_a_year)
 #
loan_repayments, loan_balance = calc_loan_repayments(scenario, years)
depreciation, life_span = calc_depreciation(scenario, Spectra_Blade_Single_Sided_J, avg_photoperiod, years, days_in_year)
# Constructing Financial Overview Data Frame
financial_annual_overview, financial_monthly_overview = build_dataframe(timeseries_yearly, timeseries_monthly)
financial_annual_overview = crop_and_revenue_to_df(financial_annual_overview, w1, w2, w3, w4, total_sales)
financial_annual_overview = cogs_to_df(financial_annual_overview, cogs_labour, cogs_media, cogs_packaging, cogs_seeds_nutrients, cogs_electricity, cogs_water)
financial_annual_overview = opex_to_df(financial_annual_overview, opex_rent, opex_salaries, opex_other_costs, opex_insurance, opex_distribution)
financial_annual_overview = extra_to_df(financial_annual_overview, loan_repayments, loan_balance, scenario, depreciation)

roi = calc_roi(scenario, financial_annual_overview, years)
financial_annual_overview.loc['Return on Investment'] = roi
investment_balance, payback_period = calc_payback_period(scenario, financial_annual_overview, years)

financial_summary = build_financial_summary(financial_annual_overview, investment_balance, roi, timeseries_yearly)

# Productivity Metrics

productivity_metrics = calc_productivity_metrics(timeseries_yearly, w1, w2, w3, w4, electricity_consumption, direct_labour, water_consumption, staff_list, nutrient_consumption, total_no_of_plants)
crop_productivity_metrics = calc_crop_productivity_metrics(productivity_metrics, gp, scenario)
productivity_targets = productivity_targets(crop_productivity_metrics, scenario)

# Where it gets risky
critical_risk, substantial_risk, moderate_risk = build_risk_curves(years)
bankruptcy_definition = build_bankruptcy_definition(years)
risk_dataframe = build_risk_dataframe(financial_annual_overview)

# Setting up Plots
plt.close(fig=None)
fig1, ax1 = plt.subplots()
fig1, ax2 = plt.subplots()
fig1, ax3 = plt.subplots()
fig1, ax4 = plt.subplots()
fig1, ax5 = plt.subplots()
fig1, ax6 = plt.subplots()



for s in range(simulations):
     risk_dataframe = build_risk_dataframe(financial_annual_overview)

     # Pathogen Outbreak
     w1_risk, w2_risk, w3_risk, w4_risk = calc_pathogen_outbreak(scenario, years, w1, w2, w3, w4)
     w1_risk, w2_risk, w3_risk, w4_risk = calc_pest_outbreak(scenario, years, w1_risk, w2_risk, w3_risk, w4_risk)
     w1_risk, w2_risk, w3_risk, w4_risk = calc_power_outage(scenario, years, w1_risk, w2_risk, w3_risk, w4_risk)
     scrop1, scrop2, scrop3, scrop4, total_sales_risk = calc_produce_sales(w1_risk, w2_risk, w3_risk, w4_risk, scenario)
     customer_withdrawal = calc_customer_withdrawal(scenario, years, total_sales_risk)
     repair = calc_repairs(scenario, years)
     labour_damage, labour_extra_cost = labour_challenges(scenario, years, total_sales_risk, cogs_labour)
     cogs_electricity, electricity_consumption = calc_improved_light_efficiency(scenario, gp, avg_photoperiod, Spectra_Blade_Single_Sided_J, life_span, electricity_consumption, days_in_year)
     # Recomposing Dataframe
     risk_dataframe = crop_and_revenue_to_df(risk_dataframe, w1_risk, w2_risk, w3_risk, w4_risk, total_sales_risk)
     risk_dataframe.loc['Revenue - Crop Sales'] -= customer_withdrawal
     #risk_dataframe.loc['Revenue - Crop Sales'] -= labour_damage

     risk_dataframe = cogs_to_df(risk_dataframe, cogs_labour, cogs_media, cogs_packaging,
                                            cogs_seeds_nutrients, cogs_electricity, cogs_water)
     risk_dataframe.loc['COGS - Direct Labour'] += labour_extra_cost


     risk_dataframe = opex_to_df(risk_dataframe, opex_rent, opex_salaries, opex_other_costs,
                                            opex_insurance, opex_distribution)
     risk_dataframe.loc['OPEX - Other Costs'] += repair
     risk_dataframe = extra_to_df(risk_dataframe, loan_repayments, loan_balance, scenario,
                                             depreciation)

     risk_dataframe = calc_planning_delay(risk_dataframe, timeseries_yearly, years)

     # ROI
     roi_risk = calc_roi(scenario, risk_dataframe, years)
     risk_dataframe.loc['Return on Investment'] = roi_risk
     risk_counter = risk_assessment(roi_risk, bankruptcy_definition, years, risk_counter)

     # COMMENT OUT IF NOT INTERESTED IN RISK PLOTS
     ax2.plot(risk_dataframe.columns, roi_risk)
     ax4.plot(risk_dataframe.columns, risk_dataframe.loc['Revenue - Crop Sales'])
     ax5.plot(risk_dataframe.columns, repair)

risk_assessment_probability = risk_assessment_probability(risk_counter, years, simulations)
export_results(financial_annual_overview, financial_summary, risk_dataframe)


ax1.plot(financial_annual_overview.columns, financial_annual_overview.loc['Total Revenue'], label='Revenue')
ax1.plot(financial_annual_overview.columns, financial_annual_overview.loc['Total COGS'], label='COGS')
ax1.plot(financial_annual_overview.columns, financial_annual_overview.loc['Total OPEX'], label='OPEX')
ax1.plot(financial_annual_overview.columns, financial_annual_overview.loc['Gross Profit'], label='Gross Profit')
ax1.plot(financial_annual_overview.columns, financial_annual_overview.loc['Net Profit'], label='Net Profit')
ax1.set_xlabel('Year')
ax1.set_ylabel('Finance (£)')
ax1.set_title('Annual Financial Overview')
ax1.legend()

ax2.plot(financial_annual_overview.columns, roi, label = 'ROI no Risk', linewidth=4)
ax2.set_xlabel('Year')
ax2.set_ylabel('ROI (%)')
ax2.set_title('Return on Investment')
ax2.legend()

ax3.plot(timeseries_yearly, critical_risk, linestyle='dashed', color='g') #label='Critical')
ax3.plot(timeseries_yearly, moderate_risk, linestyle='dashed', color='g') #label='Moderate')
ax3.plot(timeseries_yearly, substantial_risk, linestyle='dashed', color='g') #label='Substantial')
ax3.plot(timeseries_yearly, risk_assessment_probability, linewidth=2, color='red', label='Risk Curve')
ax3.set_xlim(timeseries_yearly[0], timeseries_yearly[-1])
ax3.set_ylim(0, 1)
ax3.set_ylabel('Probabiltiy of Bankruptcy')
ax3.set_xlabel('Year')
ax3.set_title('Risk Assessment')
ax3.text(timeseries_yearly[1], 0.8, 'Critical')
ax3.text(timeseries_yearly[years-10], 0.6, 'Substantial')
ax3.text(timeseries_yearly[years-5], 0.3, 'Moderate')
ax3.text(timeseries_yearly[years-3], 0.05, 'Safe')

ax4.plot(financial_annual_overview.columns, financial_annual_overview.loc['Revenue - Crop Sales'], label='Crop Sales no Risk', linewidth=4)
ax4.set_xlabel('Year')
ax4.set_ylabel('Sales (£)')
ax4.set_title('Crop Sales')
ax4.legend()

ax5.set_xlabel('Year')
ax5.set_ylabel('Repairs (£)')
ax5.set_title('Repair Costs')

# RADAR CHART
# number of variable
categories = list(productivity_targets)[1:]
N = len(categories)

# We are going to plot the first line of the data frame.
# But we need to repeat the first value to close the circular graph:
values = productivity_targets.loc[0].drop('metric').values.flatten().tolist()
values += values[:1]

values2 = productivity_targets.loc[1].drop('metric').values.flatten().tolist()
values2 += values2[:1]


# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Initialise the spider plot
ax6 = plt.subplot(111, polar=True)

# Draw one axe per variable + add labels labels yet
plt.xticks(angles[:-1], categories, color='grey', size=8)

# Draw ylabels
ax6.set_rlabel_position(0)
plt.yticks([-1, 0.5, 0, 0.5, 1, 1.5], ["-1", "-0.5", "0", "0.5","1", "1.5"], color="grey", size=7)
ax6.set_ylim(-1, 1.5)

# Plot data
ax6.plot(angles, values, linewidth=1, linestyle='solid', label='Crop Productivity')
ax6.plot(angles, values2, linewidth=1, linestyle='solid', label='Target')


# Fill area
ax6.fill(angles, values, 'b', alpha=0.1)
ax6.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2)

plt.show()

print (scenario.start_date.strftime('The simulation computes from %d, %b, %Y'), end_date.strftime('until %d, %b, %Y'))      # format_str = "%B %d, %Y"')
print('The farm is growing Crop1: {}, Crop2 :{}, Crop3: {} and Crop 4:{}'.format(scenario.crop_typ1, scenario.crop_typ2, scenario.crop_typ3, scenario.crop_typ4))
print('Estimated capital expenditure for full-scale farm is: £{}'.format(capex_full))
print(financial_annual_overview)
print(payback_period)



