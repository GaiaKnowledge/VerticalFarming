# coding=utf-8
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import random
import math
from math import pi
import matplotlib.pyplot as plt
import pba

# Local imports
from inputs import Scenario
from inputs import Growthplan
from inputs import Staff
import vf_crops
import copy

MONTHS_IN_YEAR = 12
DAYS_IN_YEAR = 365.25

# Input File
def get_scenario():
    """Get Scenario
        Notes: Scenario is extracted from /Users/Francis/PycharmProjects/VerticalFarming/Current_Financial_Model.xlsx
        This should be edited according to the file path and name of the saved excel model.

    Returns:
        scenario (object): The farm scenario that provided the basis of the analysis

    To Do:
    """

    input_filepath = './Current_Financial_Model.xlsx'  # Make a copy and call spreadsheet this name
    inputs = pd.read_excel(input_filepath, index_col=0).to_dict()
    inputs = inputs['Inputs']
    zipgrow_growing_area = 24.481536

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
    scenario.other_costs_full = inputs['other_costs_full']

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
    scenario.insulation_level = inputs['insulation_level']
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

    scenario.currency=inputs['currency']

    # for crop_type in ['lettuce_fu_mix', 'basil_lemon', 'basil_genovese']:
    for i in range(1,5):
        crop_parameter = vf_crops.CropParameters()
        crop_parameter.type = inputs[f"crop_typ{i}"]
        crop_parameter.percent = inputs[f"crop{i}_percent"]
        crop_parameter.system = inputs[f"crop{i}_system"]
        crop_parameter.harvest_weight = inputs[f"crop{i}_harvest_weight"]
        crop_parameter.product_weight = inputs[f"crop{i}_product_weight"]
        crop_parameter.customer_percent = inputs[f"crop{i}_customer_percent"]
        crop_parameter.price1 = inputs[f"crop{i}_price1"]
        crop_parameter.price2 = inputs[f"crop{i}_price2"]
        scenario.crop_parameters.append(crop_parameter)

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

    if scenario.system_type == 'ZipRack':
        scenario.stacked_growing_area_pilot = round(scenario.system_quantity * zipgrow_growing_area, 1)
    else:
        scenario.stacked_growing_area_pilot = round(scenario.growing_area_pilot * scenario.growing_levels_pilot, 1)

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

    scenario.energy_type = inputs['energy_type']
    scenario.daily_energy_consumption = inputs['daily_energy_consumption']

    scenario.grants_rev_y0 = inputs['grants_rev_y0']
    scenario.grants_rev_y1 = inputs['grants_rev_y1']
    scenario.grants_rev_y2 = inputs['grants_rev_y2']
    scenario.grants_rev_y3 = inputs['grants_rev_y3']
    scenario.grants_rev_y4 = inputs['grants_rev_y4']
    scenario.grants_rev_y5 = inputs['grants_rev_y5']
    scenario.grants_rev_y6 = inputs['grants_rev_y6']
    scenario.grants_rev_y7 = inputs['grants_rev_y7']
    scenario.grants_rev_y8 = inputs['grants_rev_y8']
    scenario.grants_rev_y9 = inputs['grants_rev_y9']
    scenario.grants_rev_y10 = inputs['grants_rev_y10']
    scenario.grants_rev_y11 = inputs['grants_rev_y11']


    return scenario

def export_results(financial_annual_overview, financial_summary, risk_dataframe, p_box):
    """Export results function
        Notes: Defines job roles and attributes

     Args:
         financial_annual_overview (dataframe): An annual financial overview of the analysis period
         financial_summary (dataframe): A financial summary over the analysis period
         risk_dataframe (dataframe):A annual financial overview of the analysis period with risk included
     """
    writer = pd.ExcelWriter('results.xlsx', engine='xlsxwriter')
    financial_summary.to_excel(writer, sheet_name='Summary')
    financial_annual_overview.to_excel(writer, sheet_name='Overview')

    writer.save()

    #if p_box == 'yes':


    # with pd.ExcelWriter('./results.xlsx') as writer:
    #     financial_summary.to_excel(writer, "results.xlsx")
    #     financial_annual_overview.to_excel(writer, "results.xlsx")

        #risk_dataframe.to_excel(writer, "results.xlsx")
    return

# def mean_dataframe(risk_dataframe, timeseries_yearly):
#     """Average the p-boxe dataframe for mean values
#
#     Args:
#         risk_dataframe (dataframe)
#     Returns:
#         mean_dataframe (dataframe)
#     To do:
#        1. Mean the P-Box"""
#
#     indices = [1, 6, 11, 16]
#     new_timeseries = []
#
#     for index in indices:
#         new_timeseries.append(timeseries_yearly[index])
#     new_timeseries.append('Total')
#
#     mean_dataframe = pd.DataFrame(index= ['Cumulative Yield', 'Total Revenue', 'Total COGS', 'Gross Profit',
#                             'Total OPEX', 'EBITDA', 'Loan Balance', 'Depreciation', 'Net Profit', 'Return on Investment', 'Financial Balance'] ,columns=new_timeseries)
#
#     for i in range(risk_dataframe.shape[0]):  # iterate over rows
#         for j in range(risk_dataframe.shape[1]):  # iterate over columns
#             a = sum(dataframe.at[i, j])/400
#             # get cell value
#             print(value, end="\t")
#         print()
#     return

def get_currency(scenario):

    if scenario.currency == 'GBP':
        scenario.currency = '£'
    elif scenario.currency == 'USD':
        scenario.currency = '$'
    elif scenario.currency == 'JPY':
        scenario.currency = '¥'
    elif scenario.currency == 'AUD':
        scenario.currency = 'AUS $'
    elif scenario.currency == 'EUR':
        scenario.currency = '€'
    else:
        raise RuntimeError(f"Unknown currency: {scenario.currency}")
    return scenario.currency


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
    ceo = Staff('unknown', 'CEO', scenario.ceo_msalary, scenario.ceo_count_y1, scenario.ceo_count_y2, 'indirect', 0, 0, 0)
    headgrower = Staff('unknown','Head Grower', scenario.hgrower_msalary, scenario.hgrower_count_y1, scenario.hgrower_count_y2, 'indirect', 0, 0, 0)
    marketer = Staff('unknown','Marketer', scenario.marketer_msalary, scenario.marketer_count_y1, scenario.marketer_count_y2, 'indirect', 0, 0, 0)
    scientist = Staff('unknown', 'Scientist', scenario.scientist_msalary, scenario.scientist_count_y1, scenario.scientist_count_y2, 'indirect', 0, 0, 0)
    sales_person = Staff('unknown', 'Sales Person', scenario.salesperson_msalary, scenario.salesperson_count_y1, scenario.salesperson_count_y2, 'indrect', 0, 0, 0)
    manager = Staff('unknown', 'Manager', scenario.manager_msalary, scenario.manager_count_y1, scenario.manager_count_y2,'indrect', 0, 0, 0)
    delivery = Staff('unknown', 'Delivery', scenario.delivery_msalary, scenario.delivery_count_y1, scenario.delivery_count_y2, 'direct', 0, 0, 0)
    farmhand = Staff('unknown', 'Farm Hand', scenario.farmhand_msalary, scenario.farmhand_count_y1, scenario.farmhand_count_y2, 'direct', 0, 0, 0)
    admin = Staff('unknown', 'Admin', scenario.admin_msalary, scenario.admin_count_y1, scenario.admin_count_y2, 'salary', 0, 0, 0)
    part_time = Staff('unknown', 'Part-time Employee', 0, 0, 0, 'direct', scenario.parttime_wage, scenario.parttime_count_y1, scenario.parttime_count_y2)
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
    zipgrow_growing_area = 24.481536 #m^2
    gp = Growthplan()
    gp.upgrade_year = scenario.start_date + timedelta(days=DAYS_IN_YEAR) # When scaling of pilot farm occurs
    gp.facility_size_full = scenario.facility_size_pilot * scenario.growing_area_mulitplier
    gp.percent_production_area_full = scenario.percent_production_area_pilot
    gp.growing_levels_full = scenario.growing_levels_pilot
    gp.no_lights_full = scenario.no_lights_pilot * scenario.growing_area_mulitplier
    gp.packaging_cost_full = scenario.packaging_cost_pilot
    gp.other_costs_full = scenario.other_costs_full
    gp.growing_area_full = scenario.growing_area_pilot * scenario.growing_area_mulitplier

    if scenario.system_type == 'ZipRack':
        gp.stacked_growing_area_full = round(scenario.system_quantity * scenario.growing_area_mulitplier * zipgrow_growing_area, 1)
    else:
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

def calc_hvac_energy(scenario):
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

    energy_consumption_from_HVAC = q * conv_factor_kJph_to_kWh * DAYS_IN_YEAR


# Yields
def calc_best_yield(scenario, growth_plan, years, p_box):
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
        2. Crop type as on object is an input. Ideally crop_typ1 should be mapped onto scenario.crop_typ1 which is currently a string rather than an object.
    """

    crop_yields = []
    for crop_parameter in scenario.crop_parameters:
        crop = vf_crops.get_crop(crop_parameter.type)
        current_crop_yield = [0]
        #if p_box == 'no':
        if crop_parameter.system == 'Drip Tower':
            max_yield = crop.drip_tower # This needs to be adaptable to whichever system is in selection
        elif crop_parameter.system == 'NFT':
            max_yield = crop.nft
        elif crop_parameter.system == 'Aeroponic':
            max_yield = crop.aeroponic
        elif crop_parameter.system == 'Ebb/Flow':
            max_yield = crop.ebb_flow
        elif crop_parameter.system == 'DWC':
            max_yield = crop.dwc
        elif crop_parameter.system == 'Bucket':
            max_yield = crop.bucket
        elif crop_parameter.systemm == 'Slab':
            max_yield = crop.slab
        elif crop_parameter.system == 'Soil':
            max_yield = crop.soil
        else:
            raise RuntimeError(f"Unknown system: {crop_parameter.system}")

        for y in range(1, years+1):
            if y == 1:  # under upgrade year check gp.upgrade_year
                current_crop_yield.append(max_yield  * scenario.stacked_growing_area_pilot * crop_parameter.percent)
            elif y > 1:
                current_crop_yield.append(max_yield * growth_plan.stacked_growing_area_full * crop_parameter.percent)
        crop_yields.append(current_crop_yield)
    return crop_yields


def calc_adjustment_factors(scenario, p_box):
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
    if p_box == 'no':
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

    elif p_box == 'yes':
        factor_table =  pd.DataFrame({'High': [pba.Pbox([0.95,1]), pba.Pbox([0.95,1]), pba.Pbox([0.95,1]), pba.Pbox([0.97,1]), 'n/a'],
                                   'Medium': [pba.Pbox([0.75,0.95]), pba.Pbox([0.85,0.95]), pba.Pbox([0.85,0.95]), pba.Pbox([0.96,0.97]), 'n/a'],
                                   'Low': [pba.Pbox([0.6,0.75]), pba.Pbox([0.85,0.95]), pba.Pbox([0.85,0.95]), pba.Pbox([0.95,0.96]), 'n/a'],
                                   'Yes': ['n/a', 'n/a', 'n/a', 'n/a', pba.Pbox([0.85,1])],
                                       'No':['n/a', 'n/a', 'n/a', 'n/a', pba.Pbox([0.85,00.95])]})
        factor_table.index = ['Light Control', 'Climate Contol', 'Nutrient Control', 'Air Conditioning', 'CO2 Enrichment']
        # factor_table = pd.DataFrame({'High': [1, 1, 1, 1, 'n/a'],
        #                              'Medium': [0.9, 0.9, 0.9, 0.97, 'n/a'],
        #                              'Low': [0.6, 0.85, 0.85, 0.95, 'n/a'],
        #                              'Yes': ['n/a', 'n/a', 'n/a', 'n/a', 1],
        #                              'No': ['n/a', 'n/a', 'n/a', 'n/a', 0.9]})
        # factor_table.index = ['Light Control', 'Climate Contol', 'Nutrient Control', 'Air Conditioning',
        #                       'CO2 Enrichment']

        light_factor = factor_table.loc['Light Control', scenario.lighting_control]
        temp_factor = factor_table.loc['Climate Contol', scenario.climate_control]
        nutrient_factor = factor_table.loc['Nutrient Control', scenario.nutrient_control]
        co2_factor = factor_table.loc['CO2 Enrichment', scenario.co2_enrichment]


    return light_factor, temp_factor, nutrient_factor, co2_factor

def calc_adjusted_yield(crop_yields, light_factor, temp_factor, nutrient_factor, co2_factor):
    adjusted_yields = []
    for cyield in crop_yields:
        adjusted_yields.append(np.array(cyield, dtype=int) * light_factor * temp_factor * nutrient_factor * co2_factor)
    return adjusted_yields

def calc_waste_adjusted_yield(scenario, crop_yields, years, p_box):
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
        1. Update with uncertainty and pboxes
    """
    if p_box == 'no':
        multiply_factor = 0.5
    if p_box == 'yes':
        multiply_factor = pba.Pbox(pba.I(0.5, 0.75))
        #multiply_factor = 0.5


    high = [0]
    medium =[0]
    low = [0]

    for x in range(1, years+1):
        low.append(multiply_factor *(((-5*10**-5)-5E-05*x**3) + (0.0018*x**2) - (0.0281*x) + 0.2659))
        medium.append(multiply_factor*(((-4*10**-5)*x**3) + (0.0013*x**2) - (0.0208*x) + 0.1966))
        high.append(multiply_factor*(((-2*10**-5)*x**3) + (0.0009*x**2) - (0.0146*x) + 0.1387))

    waste_rates = pd.DataFrame({'High': high,
                  'Medium': medium,
                  'Low': low})
    waste_rates.index = range(years+1)
    # Learning curve for loop according to Dataframe
    waste_adjusted_yields = []
    for cyield in crop_yields:
        this_yield = []
        for y in range(years+1):
            this_yield.append(cyield[y]*(1-waste_rates.loc[y,scenario.grower_exp]))
        waste_adjusted_yields.append(this_yield)

    return waste_adjusted_yields

# Revenue
def calc_produce_sales(waste_adjusted_yields, scenario):
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
    crop_sales = []
    for i, crop in enumerate(scenario.crop_parameters):
        this_crop_sales = []
        w = waste_adjusted_yields[i]
        for yw in w:
            this_crop_sales.append((yw * crop.price1 * crop.customer_percent / crop.product_weight) + (yw * crop.price2 * (1-crop.customer_percent) / crop.product_weight))
        crop_sales.append(this_crop_sales)
    total_sales = [sum(sales) for sales in zip(*crop_sales)]
    return crop_sales, total_sales

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
def calc_grants_rev(years, scenario):
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
    grants_rev = [scenario.grants_rev_y0, scenario.grants_rev_y1, scenario.grants_rev_y2, scenario.grants_rev_y3,scenario.grants_rev_y4,scenario.grants_rev_y5,scenario.grants_rev_y6,scenario.grants_rev_y7,scenario.grants_rev_y8,scenario.grants_rev_y9,scenario.grants_rev_y10,scenario.grants_rev_y11]
    g_len = len(grants_rev)

    for y in range(g_len, years+1):

        grants_rev.append(0)

    return grants_rev

# COGS

def calc_direct_labour(farmhand, delivery, part_time, years, scenario):
    """Calculate Direct Labour costs Function

    Args:
       farmhand (object): The role of farm hand and its attributes
       delivery (object): The role of delivery and its attributes
       part_time (object): The role of part-time and its attributes
       years (int): The number of years the analysis will look at
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
    direct_labour = [0]
    part_time_hours =[0] # Annual
    cogs_direct_labour = [0]
    HOURS_IN_WEEK = 40
    WEEKS_IN_MONTH = 4
    MONTHS_IN_YEAR

    for y in range(1, years+1):

        if y == 1:
            direct_labour_cost = MONTHS_IN_YEAR*((farmhand.salary * farmhand.count_pilot) + (delivery.salary * delivery.count_pilot) + (part_time.hours * part_time.wage))
            part_time_hours.append(part_time.hours*MONTHS_IN_YEAR)
            direct_labour.append(((farmhand.count_pilot+delivery.count_pilot)*HOURS_IN_WEEK*WEEKS_IN_MONTH*MONTHS_IN_YEAR) + part_time_hours[y])
        elif y == 2:
            direct_labour_cost = MONTHS_IN_YEAR*((farmhand.salary * farmhand.count_full) + (delivery.salary * delivery.count_full) + (part_time.hours_full * part_time.wage))
            part_time_hours.append(part_time.hours_full*MONTHS_IN_YEAR)
            direct_labour.append(((farmhand.count_full+delivery.count_full)*HOURS_IN_WEEK*WEEKS_IN_MONTH*MONTHS_IN_YEAR)+part_time_hours[y])
        elif y > 2:
            part_time_hours.append(part_time_hours[y-1] * (1 - scenario.labour_improvement))
            direct_labour_cost = (MONTHS_IN_YEAR * ((farmhand.salary * farmhand.count_full) + (delivery.salary * delivery.count_full))) + (part_time_hours[y] * part_time.wage)
            direct_labour.append(((farmhand.count_full+delivery.count_full)*HOURS_IN_WEEK*WEEKS_IN_MONTH*MONTHS_IN_YEAR)+part_time_hours[y])

        cogs_direct_labour.append(direct_labour_cost)

    return cogs_direct_labour, direct_labour

def calc_growing_media(scenario, total_sales, adjusted_yields):
    """Calculate Growing Media costs Function

    Args:
       total_sales (list): The total sales as a annual time series

    Returns:
        cogs_cogs_media (list): Cost of Goods Sold expenditure on Growing Media as a time series for each year

    To Do:
        Currently taken as an estimate as 2.5% of sales and should be improved to be dependant on growing media selected
        Similar to packaging, should take into consideration economic order quantity
    """
    cogs_media = []
    num_plants = []

    media = vf_crops.get_media(scenario.growing_media)

    for i, crop_param in enumerate(scenario.crop_parameters):
        a = adjusted_yields[i]
        crop = vf_crops.get_crop(crop_param.type)
        this_num_plants = [i / crop_param.harvest_weight for i in a]
        this_cogs_media = [i * media.cost for i in this_num_plants]
        num_plants.append(this_num_plants)
        cogs_media.append(this_cogs_media)

    # No of plants
    total_no_of_plants = [sum(n) for n in zip(*num_plants)]
    cogs_media = [sum(x) for x in zip(*cogs_media)]

    # for y in range(years + 1):
    #     annual_media_cost = 0
    #     for i, a in enumerate(adjusted_yields):
    #         annual_media_cost += (a[y] / scenario.crop_parameters[i].harvest_weight)
    #     if y <= 1:
    #         annual_packaging_cost *= scenario.packaging_cost_pilot
    #     elif y > 1:
    #         annual_packaging_cost *= scenario.packaging_cost_full
    #     cogs_packaging.append(annual_packaging_cost)



    #percent_of_growing_media_to_sales = 0.025
    #cogs_media = [i * percent_of_growing_media_to_sales for i in total_sales]

    #scenario.growing_media * price_of_media * no_of_plants
    return cogs_media

def calc_packaging(scenario, years, waste_adjusted_yields):
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
        for i, w in enumerate(waste_adjusted_yields):
            annual_packaging_cost += (w[y] / scenario.crop_parameters[i].product_weight)
        if y <= 1:
            annual_packaging_cost *= scenario.packaging_cost_pilot
        elif y > 1:
            annual_packaging_cost *= scenario.packaging_cost_full
        cogs_packaging.append(annual_packaging_cost)

    return cogs_packaging


def calc_nutrients_and_num_plants(scenario, cogs_media, adjusted_yields, years):
    num_plants = []
    cogs_seeds = []
    cogs_nutrients =[]
    for i, crop_param in enumerate(scenario.crop_parameters):
        a = adjusted_yields[i]
        crop = vf_crops.get_crop(crop_param.type)
        this_num_plants = [i / crop_param.harvest_weight for i in a]
        this_cogs_seeds = [i * crop.seed_cost * (1.0/crop.germination_rate) for i in this_num_plants]
        num_plants.append(this_num_plants)
        cogs_seeds.append(this_cogs_seeds)

    # No of plants
    total_no_of_plants = [sum(n) for n in zip(*num_plants)]
    cogs_seeds_nutrients = [sum(x) for x in zip(*cogs_seeds)]

    for y in range(years+1):
        nutrient_cost = (cogs_seeds_nutrients[y] /0.25) - cogs_media[y] - cogs_seeds_nutrients[y]
        # Seeds, nutrients and growing media comprise of 25%, 21% and 54% of input costs respectively
        # Based on State of Indoor Farming Report 2017. Divide by 0.25 to get total input cost
        cogs_nutrients.append(nutrient_cost)
        cogs_seeds_nutrients[y] += cogs_nutrients[y]

    nutrient_consumption = [1000] * 16 # Needs to be changed

    return cogs_seeds_nutrients, nutrient_consumption, total_no_of_plants

def calc_avg_photoperiod(scenario):
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
    avg_photoperiod = 0.0
    for crop_param in scenario.crop_parameters:
        crop = vf_crops.get_crop(crop_param.type)
        avg_photoperiod += crop_param.percent * crop.photoperiod
    return avg_photoperiod

def calc_electricity(scenario, gp, avg_photoperiod, light, years, HVAC_multiplier):
    """Calculate Electricity costs Function

    Args:
       scenario (object): The farm scenario
       gp (object): Growth plan for Farm
       avg_photoperiod (float): Average photoperiod of lights considering crop requirements
       light (object): The light selected by the user
       years (int): The no. of years the simulation will analyse

    Returns:
        cogs_electricity (list): Cost of Goods Sold expenditure on Electricity as a time series for each year
        electricity_consumption (list): The amount of eletricity consumed each year

    To Do:
        Add HVAC model and remove HVAC multiplier of 1.25 for enhanced accuracy... leave multiplier as a default?
    """

    electricity_consumption =[0]
    for y in range(years+1):
        if y == 1:
            electricity_lights_pilot = avg_photoperiod * light.max_power * scenario.no_lights_pilot * DAYS_IN_YEAR/ 1000
            electricity_other_pilot = scenario.daily_energy_consumption * DAYS_IN_YEAR
            electricity_consumption.append(electricity_lights_pilot+electricity_other_pilot)
        elif y > 1: # Multiplied by 1.25 to accomodate HVAC upgrade
            electricity_lights_full = avg_photoperiod * light.max_power * gp.no_lights_full * DAYS_IN_YEAR /1000
            electricity_other_full = electricity_other_pilot
            combined_electricity = (electricity_lights_full * HVAC_multiplier) + electricity_other_full
            electricity_consumption.append(combined_electricity)
    cogs_electricity = [i * scenario.electricity_price for i in electricity_consumption]
    return cogs_electricity, electricity_consumption

def calc_water(scenario, years):
    """Calculate Water costs Function

    Args:
       scenario (object): The farm scenario
       years (int): The no. of years the simulation will analyse

    Returns:
        cogs_water (list): Cost of Goods Sold expenditure on Water as a time series for each year
        water_consumption (list): The amount of water consumed each year
    """
    water_consumption = [0]

    for y in range(years+1):
        if y == 1:
            water_consumption.append(scenario.system_quantity * 0.95 * DAYS_IN_YEAR + (1900*12))
        elif y > 1:
            water_consumption.append((scenario.system_quantity * 0.95 * DAYS_IN_YEAR + (1900*12)) * scenario.growing_area_mulitplier)

    cogs_water = [i * scenario.water_price for i in water_consumption]

    return cogs_water, water_consumption

# OPEX

def calc_rent(scenario, years):
    """Calculate Rent costs Function

    Args:
       scenario (object): The farm scenario
       years (int): The no. of years the simulation will analyse

    Returns:
        opex_rent (list): Operational expenditure on other costs as a time series for each year
    """
    opex_rent = [0]
    for y in range(years+1):
        if y == 1:
            opex_rent.append(scenario.monthly_rent_y1* MONTHS_IN_YEAR)
        elif y > 1:
            opex_rent.append(scenario.monthly_rent_y2 * MONTHS_IN_YEAR)

    return opex_rent

def calc_salaries(ceo, scientist, marketer, admin, manager, headgrower, sales_person, years):
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

    Returns:
        opex_salaries (list): Operational expenditure on salaries as a time series for each year
    """
    opex_salaries = [0]

    for y in range(1, years+1):

        if y == 1:
            staff_cost = MONTHS_IN_YEAR * (ceo.cost_pilot + scientist.cost_pilot +\
                        marketer.cost_pilot + admin.cost_pilot +\
                        manager.cost_pilot + headgrower.cost_pilot + \
                        sales_person.cost_pilot)
        elif y > 1:
            staff_cost = MONTHS_IN_YEAR * (ceo.cost_full + scientist.cost_full +\
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
        if y ==1:
            opex_other_costs.append(scenario.other_costs_pilot * opex_staff[y])
        elif y > 1:
            opex_other_costs.append(scenario.other_costs_full * opex_staff[y])
    return opex_other_costs

def calc_insurance(scenario, years):
    """Calculate Insurance costs Function

    Args:
       scenario (object): The farm scenario
       years (int): The no. of years the simulation will analyse

    Returns:
        opex_insurance (list): Operational expenditure on insurance as a time series for each year
    """
    opex_insurance = [0]
    for y in range(years + 1):
        if y == 1:
            opex_insurance.append(scenario.insurance_pilot * MONTHS_IN_YEAR)
        elif y > 1:
            opex_insurance.append(scenario.insurance_full * MONTHS_IN_YEAR)

    return opex_insurance


def calc_distribution(scenario, years):
    """Calculate Distribution costs Function

    Args:
       scenario (object): The farm scenario
       years (int): The no. of years the simulation will analyse

    Returns:
        opex_distribution (list): Operational expenditure on distribution as a time series for each year
    """

    opex_distribution = [0]
    for y in range(years + 1):
        if y == 1:
            opex_distribution.append(scenario.monthly_distribution_y1 * MONTHS_IN_YEAR)
        elif y > 1:
            opex_distribution.append(scenario.monthly_distribution_y2 * MONTHS_IN_YEAR)

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

def calc_depreciation(scenario, lights, avg_photoperiod, years):

    """Calculate Depreciation Function to Compute Total Farm Depreciation each Year
       Typically accounts for 21 production costs

    Args:
       scenario (object): The farm scenario
       lights (object): The lights used on the farm
       avg_photoperiod (float): The average photoperiod of lights on the farm
       years (int): The no. of years the simulation will analyse

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
    life_span = (life_time / avg_photoperiod)/DAYS_IN_YEAR
    lights_depreciation_percent = 1/life_span
    lights_depreciation = lights_depreciation_percent * scenario.capex_lights
    # Pilot
    pilot_depreciation = (lights_depreciation+facilities_depreciation+building_depreciation)/scenario.growing_area_mulitplier
    total_depreciation = lights_depreciation+facilities_depreciation+building_depreciation
    depreciation = [0]

    for y in range(1, years+1):
        if y == 1:
            depreciation.append(pilot_depreciation)
        elif y > 1:
            depreciation.append(total_depreciation)

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

def calc_payback_period(scenario, financial_annual_overview, years, p_box):
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
        investment_balance.append(investment_balance[y] + financial_annual_overview.iloc[30,y+1])

        if p_box == 'no':
            if investment_balance[y] <= 0:
                payback_period_list.append(y)
            else:
                payback_period_list.append(0)
        if p_box == 'yes':
            if investment_balance[y] <= 0:
                payback_period_list.append(investment_balance[y] < 0)
            else:
                payback_period_list.append(investment_balance[y] > 0)
    try:
        payback_period = payback_period_list.index(1, 0, years+1)
    except ValueError:
        payback_period = 'The Farm it not economically sustainable and will not turn a profit during the {} years of simulation'.format(years)
# Does the investment balance straddle zero - P-box scenario.
    return investment_balance, payback_period

def calc_financial_balance(financial_annual_overview, scenario, years,p_box):
    """Financial Balance

        Notes:

        TO DO:
        1. Financial balance does not seem accurate. Combining two P-boxes does not accurately convey positives and negatives"""

    initial_capital = scenario.grants_rev_y0 + scenario.loan_amount - scenario.capex_pilot
    starting_balance1 = initial_capital + scenario.grants_rev_y1 + financial_annual_overview.iloc[30,1] - (scenario.capex_full - scenario.capex_pilot)
    starting_balance2 = starting_balance1 + financial_annual_overview.iloc[30,2] + financial_annual_overview.iloc[9,2]
    financial_balance = [initial_capital, starting_balance1, starting_balance2]
    financial_balance_min_max = copy.copy(financial_balance)

    a=financial_balance[2]
    b=financial_annual_overview.iloc[30,3]
    c = a + b
    #d = pba.Pbox([min(a) + min(b),max(a)+max(b)])
    print(c)
    print(financial_balance[2])
    print(financial_annual_overview.iloc[30,3])
    print(pba.Pbox(pba.I(64776, 1097624))+pba.Pbox(pba.I(-334682.47, 1157849.5204)))
    #print(d)
    print("WHY ARE THESE NUMBERS NOT THE SAME (above/below)")
    print(financial_balance[2]+financial_annual_overview.iloc[30,3])

    if p_box == 'yes':
        for y in range(2, years):
            b = financial_balance[y]
            p = financial_annual_overview.iloc[30,y+1]
            g = financial_annual_overview.iloc[9,y+1]
            #b_max.append(max(financial_balance[y]))
            #p_max.append(max(financial_annual_overview.iloc[30,y+1]))
            #g_max.append(max(financial_annual_overview.iloc[9,y+1]))
            # New balance = current financial balance + net profit + grants
            """THIS IS A TEMP HACK"""
            new_balance_min_max = pba.Pbox([min(b) + min(p) + g, max(b) + max(p)+ g])
            new_balance = financial_balance[y] + financial_annual_overview.iloc[30,y+1] + financial_annual_overview.iloc[9,y+1]
            financial_balance_min_max.append(new_balance_min_max)
            financial_balance.append(new_balance)
        print(financial_balance[3])
        print("TEMP HACK THE FINANCIAL BALANCE GRAPH SHOULD LOOK LIKE THIS ")
        print(financial_balance)
        financial_annual_overview.loc['Financial Balance'] = financial_balance
    elif p_box == 'no':
        for y in range(2, years):
            new_balance = financial_balance[y] + financial_annual_overview.iloc[30,y+1] + financial_annual_overview.iloc[9,y+1]
            financial_balance.append(new_balance)
        financial_annual_overview.loc['Financial Balance'] = financial_balance
        financial_balance_min_max = 0

    return financial_annual_overview, financial_balance, financial_balance_min_max

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
                         'Net Profit', 'Return on Investment', 'Financial Balance'] ,columns=timeseries_yearly)

    financial_monthly_overview = pd.DataFrame(index= ['Yield Crop 1', 'Yield Crop 2', 'Yield Crop 3', 'Yield Crop 4',
                         'Revenue - Crop Sales', 'Revenue - Value-Added Products', 'Revenue - Education', 'Revenue - Tourism', 'Revenue - Hospitality', 'Revenue - Grants', 'Total Revenue',
                         'COGS - Direct Labour', 'COGS - Growing Media', 'COGS - Packaging', 'COGS - Seeds & Nutrients', 'COGS - Electricity', 'COGS - Water', 'Total COGS',
                         'Gross Profit',
                         'OPEX - Rent', 'OPEX - Staff (non-direct)', 'OPEX - Other Costs','OPEX - Insurance', 'OPEX - Distribution', 'Total OPEX',
                         'EBITDA',
                         'Loan Repayments', 'Loan Balance', 'Taxes', 'Depreciation',
                         'Net Profit', 'Return on Investment'] ,columns=timeseries_monthly)
    return financial_annual_overview, financial_monthly_overview

def crop_and_revenue_to_df(financial_annual_overview, waste_adjusted_yields, total_sales, vadded_sales, education_rev, tourism_rev, hospitality_rev, grants_rev):
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

    for i, w in enumerate(waste_adjusted_yields):
        financial_annual_overview.loc[f"Yield Crop {i+1}"] = w
    financial_annual_overview.loc['Revenue - Crop Sales'] = total_sales
    financial_annual_overview.loc['Revenue - Value-Added Products'] = vadded_sales
    financial_annual_overview.loc['Revenue - Education'] = education_rev
    financial_annual_overview.loc['Revenue - Tourism'] = tourism_rev
    financial_annual_overview.loc['Revenue - Hospitality'] = hospitality_rev
    financial_annual_overview.loc['Revenue - Grants'] = grants_rev
    financial_annual_overview.loc['Total Revenue'] = financial_annual_overview.loc['Revenue - Hospitality'] + \
                                                     financial_annual_overview.loc['Revenue - Crop Sales'] + financial_annual_overview.loc['Revenue - Value-Added Products'] + financial_annual_overview.loc['Revenue - Tourism'] \
                                                     + financial_annual_overview.loc['Revenue - Education'] # REMOVAL OF + financial_annual_overview.loc['Revenue - Grants']

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




# Productivity Metrics
def calc_productivity_metrics(scenario, timeseries_yearly, waste_adjusted_yields, electricity_consumption, direct_labour,
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
               'Nutrient Consumption (kg)', 'No. of Plants', 'CO2 Emitted (tonnes CO2e)', 'CO2 Mitigated (tonnes CO2e)',
               'Net CO2 (tonnes CO2e)'], columns=timeseries_yearly)

    productivity_metrics.loc['Total Yield (kg)'] = [sum(s) for s in zip(*waste_adjusted_yields)] # First value needs to be zero
    productivity_metrics.loc['Energy Consumption (kWh)'] = electricity_consumption
    productivity_metrics.loc['Direct Labour (man-hours)'] = direct_labour # First value needs to be zero
    productivity_metrics.loc['Water Consumption (L)'] = water_consumption
    productivity_metrics.loc['Nutrient Consumption (kg)'] = nutrient_consumption # First value needs to be zero
    productivity_metrics.loc['No. of Plants'] = no_of_plants

    productivity_co2_emit_energy = (productivity_metrics.loc['Energy Consumption (kWh)'] * (
                1 - scenario.percentage_renewable_energy) * kg_of_CO2e_per_kwh / tonnes)
    productivity_co2_emit_water = (((productivity_metrics.loc[
                                         'Water Consumption (L)'] / millions_of_litres) * kg_of_co2e_per_million_litres) / tonnes)

    productivity_metrics.loc['CO2 Emitted (tonnes CO2e)'] = productivity_co2_emit_energy + productivity_co2_emit_water

    productivity_co2_miti_energy = ((productivity_metrics.loc[
                                         'Energy Consumption (kWh)'] * scenario.percentage_renewable_energy * kg_of_CO2e_per_kwh) / tonnes)
    productivity_co2_miti_water = ((((productivity_metrics.loc[
                                          'Water Consumption (L)'] / conventional_water_multiplier) / millions_of_litres) * kg_of_co2e_per_million_litres) / tonnes)

    productivity_metrics.loc['CO2 Mitigated (tonnes CO2e)'] = productivity_co2_miti_energy + productivity_co2_miti_water
    productivity_metrics.loc['Net CO2 (tonnes CO2e)'] = productivity_metrics.loc['CO2 Emitted (tonnes CO2e)'] - productivity_metrics.loc['CO2 Mitigated (tonnes CO2e)']
    productivity_metrics.drop(productivity_metrics.columns[0], axis=1, inplace=True)

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
               6: 'No. of Plants per unit area', 7: 'Yield per tonne CO2 emitted', 8: 'Yield per tonne CO2 mitigated',
               8: 'Yield per tonne Net CO2e'}, inplace=True)
    crop_productivity_metrics.loc['Crop Productivity per Unit Area'] = productivity_metrics.loc[
                                                                           'Total Yield (kg)'] / gp.growing_area_full
    try:
        crop_productivity_metrics.loc['Crop Productivity per Unit Energy'] = productivity_metrics.loc['Total Yield (kg)'] / \
                                                                             productivity_metrics.loc[
                                                                                 'Energy Consumption (kWh)']
    except ZeroDivisionError:
        print("*** ERROR DIVIDING BY ZERO IN calc_crop_productivity_metrics ENERGY - FIX ME!!! ***")
    crop_productivity_metrics.loc['Crop Productivity per Unit Labour'] = productivity_metrics.loc['Total Yield (kg)'] / \
                                                                         productivity_metrics.loc[
                                                                             'Direct Labour (man-hours)']
    try:
        crop_productivity_metrics.loc['Crop Productivity per Unit Water'] = productivity_metrics.loc['Total Yield (kg)'] / \
                                                                            productivity_metrics.loc[
                                                                                'Water Consumption (L)']
    except ZeroDivisionError:
        print("*** ERROR DIVIDING BY ZERO IN calc_crop_productivity_metrics WATER - FIX ME!!! ***")

    crop_productivity_metrics.loc['Crop Productivity per Unit Nutrients'] = productivity_metrics.loc[
                                                                                'Total Yield (kg)'] / \
                                                                            productivity_metrics.loc[
                                                                                'Nutrient Consumption (kg)']
    crop_productivity_metrics.loc['Crop Productivity per Unit Growing Volume'] = productivity_metrics.loc[
                                                                                     'Total Yield (kg)'] / (
                                                                                             gp.growing_area_full * scenario.ceiling_height)
    crop_productivity_metrics.loc['No. of Plants per unit area'] = productivity_metrics.loc['No. of Plants'] / (
                gp.growing_area_full * scenario.ceiling_height)
    try:
        crop_productivity_metrics.loc['Yield per tonne CO2 emitted'] = productivity_metrics.loc['Total Yield (kg)'] / \
                                                                    productivity_metrics.loc['CO2 Emitted (tonnes CO2e)']
        crop_productivity_metrics.loc['Yield per tonne CO2 mitigated'] = productivity_metrics.loc['Total Yield (kg)'] / \
                                                                    productivity_metrics.loc['CO2 Mitigated (tonnes CO2e)']

        crop_productivity_metrics.loc['Yield per tonne Net CO2e'] = productivity_metrics.loc['Total Yield (kg)'] / \
                                                             productivity_metrics.loc['Net CO2 (tonnes CO2e)']
    except ZeroDivisionError:
        print("*** ERROR DIVIDING BY ZERO IN calc_crop_productivity_metrics CO2 - FIX ME!!! ***")

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
    normalised_net_co2 = crop_productivity_metrics.loc['Yield per tonne Net CO2e',
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
        'Yield/tonne Net CO2e': [normalised_net_co2[-1], 1]
    })

    return normalised_productivity_targets

def plot_radar_chart(dataframe, ax):
    # number of variable
    categories = list(dataframe)[1:]
    N = len(categories)

    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    values = dataframe.loc[0].drop('metric').values.flatten().tolist()
    values += values[:1]

    values2 = dataframe.loc[1].drop('metric').values.flatten().tolist()
    values2 += values2[:1]


    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='grey', size=8)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([-1, 0.5, 0, 0.5, 1, 1.5], ["-1", "-0.5", "0", "0.5","1", "1.5"], color="grey", size=7)
    ax.set_ylim(-1, 1.5)

    # Plot data
    ax.plot(angles, values, linewidth=1, linestyle='solid', label='Crop Productivity')
    ax.plot(angles, values2, linewidth=1, linestyle='solid', label='Target')

    # Fill area
    ax.fill(angles, values, 'b', alpha=0.1)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2)

    return ax