import pba
from datetime import datetime
from dateutil.relativedelta import relativedelta

import os
import matplotlib.pyplot as plt
import math
import pba
import numpy as np
#from pbox import pnt
#from pbox import rng

from math import pi

from vf_overview import truncate
from vf_overview import build_dataframe
from vf_overview import build_financial_summary
from vf_overview import calc_adjusted_yield
from vf_overview import calc_adjustment_factors
from vf_overview import calc_avg_photoperiod
from vf_overview import calc_best_yield
from vf_overview import calc_capex
from vf_overview import calc_crop_productivity_metrics
from vf_overview import calc_depreciation
from vf_overview import calc_direct_labour
from vf_overview import calc_distribution
from vf_overview import calc_education_rev
from vf_overview import calc_electricity
from vf_overview import calc_grants_rev
from vf_overview import calc_growing_media
from vf_overview import calc_hospitality_rev
from vf_overview import calc_insurance
from vf_overview import calc_loan_repayments
from vf_overview import calc_nutrients_and_num_plants
from vf_overview import calc_other_costs
from vf_overview import calc_packaging
from vf_overview import calc_payback_period
from vf_overview import calc_produce_sales
from vf_overview import calc_productivity_metrics
from vf_overview import calc_rent
from vf_overview import calc_roi
from vf_overview import calc_financial_balance
from vf_overview import calc_salaries
from vf_overview import calc_tourism_rev
from vf_overview import calc_vadded_sales
from vf_overview import calc_waste_adjusted_yield
from vf_overview import calc_water
from vf_overview import cogs_to_df
from vf_overview import crop_and_revenue_to_df
from vf_overview import export_results
from vf_overview import extra_to_df
from vf_overview import get_calendar
from vf_overview import get_gp
from vf_overview import get_scenario
from vf_overview import get_staff_list
from vf_overview import get_currency
from vf_overview import opex_to_df
from vf_overview import productivity_targets
from vf_overview import plot_radar_chart

from vf_equipment import Lights
from vf_equipment import get_lights

from pba_plot import pltem
from pba_plot import pltem_med
from pba_plot import med_pbox
from pba_plot import cut
from pba_plot import median
from pba_plot import minmaxmean
from pba_plot import minmaxmedian

from risk_pba import build_risk_assessment_counter
from risk_pba import build_risk_curves
from risk_pba import build_risk_dataframe
from risk_pba import calc_customer_withdrawal
from risk_pba import calc_improved_light_efficiency
from risk_pba import calc_pathogen_outbreak
from risk_pba import calc_repairs
from risk_pba import calc_pest_outbreak
from risk_pba import calc_planning_delay
from risk_pba import calc_power_outage
from risk_pba import competitors_risk
from risk_pba import labour_challenges
from risk_pba import build_counter
from risk_pba import calc_percent_annual_decline
from risk_pba import calc_probability_of_decline
from risk_pba import decline_data
from risk_pba import cdf_bankruptcy_counter
from risk_pba import build_bankruptcy_definition
from risk_pba import threshold_probability
from risk_pba import probability_df
from risk_pba import reduced_product_quality
from risk_pba import pba_risk_assessment
from risk_pba import risk_assessment_probability
from risk_pba import improved_labour_efficiency
from risk_pba import labour_challenges
from risk_pba import play_risks
from risk_pba import play_opportunities

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
filename = './Current_Financial_Model_FU_v1.xlsx'

years = 15 # Time series length !!UP TO 20!!
simulations = 1
p_box = "yes"
percent_list = []
repairs = []

#Scenario

scenario = get_scenario(filename)
light = get_lights(scenario.light_system)
scenario.currency = get_currency(scenario)
ceo, headgrower, marketer, scientist, sales_person, manager, delivery, farmhand, admin, part_time = get_staff_list(scenario)
end_date, timeseries_monthly, timeseries_yearly = get_calendar(scenario.start_date, years)
growth_plan = get_gp(scenario)
staff_list = get_staff_list(scenario)
capex_pilot, capex_full = calc_capex(scenario, growth_plan)
risk_counter = build_risk_assessment_counter(years)
pes_counter = build_risk_assessment_counter(years)
trad_counter = build_risk_assessment_counter(years)
cdf_counter = build_risk_assessment_counter(years)
cdf_pes_counter = build_risk_assessment_counter(years)
cdf_trad_counter = build_risk_assessment_counter(years)
threshold_counter = build_counter(thresholds=11)

## INPUTS OVERWRITTEN WITH UNCERTAINTY
HVAC_multiplier = 1
scenario.electricity_price = minmaxmean(0.0734, 0.1079, 0.09065)
#part_time.hours_full = part_time.hours * pba.Pbox(pba.I(scenario.growing_area_mulitplier*0.6, scenario.growing_area_mulitplier*1))
#scenario.education_multiplier = 1.05
#scenario.vadded_products_multiplier = pba.norm(scenario.vadded_products_multiplier, (scenario.vadded_products_multiplier*1.5 - scenario.vadded_products_multiplier*0.5)/4)
# scenario.education_multiplier = minmaxmean(scenario.education_multiplier*0.9, scenario.education_multiplier*1.1, scenario.education_multiplier)
#scenario.tourism_multiplier =
#scenario.hospitality_multiplier =
#scenario.labour_improvement = minmaxmean(scenario.labour_improvement*0.85, scenario.labour_improvement*1.15, scenario.labour_improvement)
light_improvement = minmaxmean(0.5, 0.8, 0.65)
#scenario.monthly_distribution_y2 = pba.Pbox(pba.I(scenario.monthly_distribution_y1,scenario.monthly_distribution_y2))
#scenario.crop_parameters[0].price1 = pba.Pbox(pba.I(0,30))#THIS INTERVAL SHOULD AFFECT RISK GRAPH DRASICTLLY
#scenario.other_costs_full = pba.Pbox(pba.I(scenario.other_costs_full*0.8,scenario.other_costs_full*1.2))
#part_time.hours_full = pba.Pbox(pba.I(250, 300))
water_use = pba.mmms(1325, 8325, 3730, 2039)

"""INPUTS CHANGED FOR AFTER INTERVENTIONS"""
# scenario.capex_full += 30000
# HVAC_multiplier = 1.2
# light_improvement = minmaxmean(0.5, 0.7, 0.6)
# sales_person.count_pilot = 1
# admin.count_full = 1
# scenario.climate_control = 'Medium'
# scenario.nutrient_control = 'High'
# scenario.co2_enrichment = 'Yes'
# scenario.packaging_cost_full = 0.60
# scenario.packaging_cost_pilot = 1
# scenario.monthly_distribution_y2 = scenario.monthly_distribution_y1
# scenario.tourism_avg_revenue_y1 = 2000
# scenario.tourism_multiplier = 1.1
# #scenario.education_avg_revenue_y1 = 2000
# scenario.grants_rev_y2 += 100000 #pba.Pbox(pba.I(75000,100000))
# scenario.electricity_price = minmaxmean(0.0734, 0.085, 0.079)
# scenario.other_costs_full = 0.05
# scenario.biosecurity_level = 'High'

# byield_crop1, byield_crop2, byield_crop3, byield_crop4 = calc_best_yield(scenario, growth_plan, lettuce_fu_mix, basil_lemon, basil_genovese, none, years)
crop_yields = calc_best_yield(scenario, growth_plan, years, p_box)
print(crop_yields)
light_factor, temp_factor, nutrient_factor, co2_factor = calc_adjustment_factors(scenario, p_box)
adjusted_yields = calc_adjusted_yield(crop_yields, light_factor, temp_factor, nutrient_factor, co2_factor)
waste_adjusted_yields = calc_waste_adjusted_yield(scenario, adjusted_yields, years, p_box)
crop_sales, total_sales = calc_produce_sales(waste_adjusted_yields, scenario)
vadded_sales = calc_vadded_sales(scenario, years)
education_rev = calc_education_rev(scenario, years)
tourism_rev = calc_tourism_rev(scenario, years)
hospitality_rev = calc_hospitality_rev(scenario, years)
grants_rev = calc_grants_rev(years, scenario)

cogs_labour, direct_labour = calc_direct_labour(farmhand, delivery, part_time, years, scenario)
cogs_media = calc_growing_media(scenario, total_sales, adjusted_yields)
cogs_packaging = calc_packaging(scenario, years, waste_adjusted_yields)
cogs_seeds_nutrients, nutrient_consumption, total_no_of_plants = calc_nutrients_and_num_plants(scenario, cogs_media, adjusted_yields, years)
avg_photoperiod = calc_avg_photoperiod(scenario)
cogs_electricity, electricity_consumption = calc_electricity(scenario, growth_plan, avg_photoperiod, light, years, HVAC_multiplier)
cogs_water, water_consumption = calc_water(scenario, years, waste_adjusted_yields, water_use)
print(water_consumption)
opex_rent = calc_rent(scenario, years)
opex_salaries = calc_salaries(ceo, scientist, marketer, admin, manager, headgrower, sales_person, years)
opex_other_costs = calc_other_costs(scenario, opex_salaries, repairs, years)
opex_insurance = calc_insurance(scenario, years)
opex_distribution = calc_distribution(scenario, years)

loan_repayments, loan_balance = calc_loan_repayments(scenario, years)
depreciation, life_span = calc_depreciation(scenario, light, avg_photoperiod, years)
# Constructing Financial Overview Data Frame
financial_annual_overview, financial_monthly_overview = build_dataframe(timeseries_yearly, timeseries_monthly)
financial_annual_overview = crop_and_revenue_to_df(financial_annual_overview, waste_adjusted_yields, total_sales, vadded_sales, education_rev, tourism_rev, hospitality_rev, grants_rev)
financial_annual_overview = cogs_to_df(financial_annual_overview, cogs_labour, cogs_media, cogs_packaging, cogs_seeds_nutrients, cogs_electricity, cogs_water)
financial_annual_overview = opex_to_df(financial_annual_overview, opex_rent, opex_salaries, opex_other_costs, opex_insurance, opex_distribution)
financial_annual_overview = extra_to_df(financial_annual_overview, loan_repayments, loan_balance, scenario, depreciation)

roi = calc_roi(scenario, financial_annual_overview, years)
financial_annual_overview.loc['Return on Investment'] = roi

# BROKEN HERE - FIX ME
investment_balance, payback_period = calc_payback_period(scenario, financial_annual_overview, years, p_box)

financial_annual_overview, financial_balance = calc_financial_balance(financial_annual_overview, scenario, years, p_box)

# BROKEN HERE - FIX ME
# financial_summary = build_financial_summary(financial_annual_overview, investment_balance, roi, timeseries_yearly)

# Productivity Metrics
#productivity_metrics = calc_productivity_metrics(scenario, timeseries_yearly, waste_adjusted_yields, electricity_consumption, direct_labour, water_consumption, staff_list, nutrient_consumption, total_no_of_plants)
#crop_productivity_metrics = calc_crop_productivity_metrics(productivity_metrics, growth_plan, scenario)
#productivity_targets = productivity_targets(crop_productivity_metrics, scenario)

# Where it gets risky
critical_risk, substantial_risk, moderate_risk = build_risk_curves(years)
bankruptcy_definition, balance_threshold = build_bankruptcy_definition(years)
risk_dataframe = build_risk_dataframe(financial_annual_overview)

# Financial Overview
fig1, ax1 = plt.subplots() # ROI
fig1, ax2 = plt.subplots() # Risk Assessment Curve - ROI + Balance
fig1, ax3 = plt.subplots() # Risk Assessment Curve - ROI or Balance
fig1, ax4 = plt.subplots() # Risk Assessment Curve - Balance
fig1, ax5 = plt.subplots() # Threshold Curve
fig1, ax6 = plt.subplots() # Financial Balance
fig1, ax7 = plt.subplots() # Percent change curve
fig1, ax8 = plt.subplots() # Gross Margins
fig1, ax9 = plt.subplots() # Revenue
fig1, ax10 = plt.subplots() # COGS
fig1, ax11 = plt.subplots() # OPEX
fig1, ax12 = plt.subplots() # Net Profit
fig1, ax13 = plt.subplots() # Yield


# BUILD THE RISK DATAFRAME
risk_dataframe = build_risk_dataframe(financial_annual_overview)

'''RISKS START OCCURING HERE - NEED TO BE ADJUSTED FOR PBA'''

# Pathogen Outbreak
w_risks = calc_pathogen_outbreak(scenario, years, waste_adjusted_yields, p_box)
# Pest Outbreak
# w_risks = calc_pest_outbreak(scenario, years, w_risks)
# Power Outage
#w_risks = calc_power_outage(scenario, years, w_risks)
# Sales Risk
#_, total_sales_risk = calc_produce_sales(w_risks, scenario)
# Customer Withdrawal
#total_sales_risk = calc_customer_withdrawal(scenario, years, total_sales_risk)
# Repair Risk
#repairs = calc_repairs(scenario, years)
#opex_other_costs = calc_other_costs(scenario, opex_salaries, repairs, years)
# Labour Risks
#total_sales_risk, cogs_labour = labour_challenges(scenario, years, total_sales_risk, cogs_labour)

"""THIS EXECUTES THE RISKS - PICK THE SELECTED AS TRUE"""
waste_adjusted_yields_risks, total_sales_risk, opex_other_costs, cogs_labour, risk_dataframe = play_risks(pathogen_outbreak=True, pest_outbreak=True, power_outage=True, customer_withdrawal=False, repair_risk=True,labour_problems=False, planning_delay=False,
                                                                      scenario=scenario, years=years, waste_adjusted_yields=waste_adjusted_yields, p_box=p_box, opex_salaries=opex_salaries, cogs_labour=cogs_labour, risk_dataframe=risk_dataframe, timeseries_yearly=timeseries_yearly)

# opex_other_costs = calc_other_costs(scenario, opex_salaries, repairs, years)

# Electricity efficiency improvements
"""THIS EXECUTES THE OPPORTUNITIES - PICK THE SELECTED AS TRUE"""
cogs_electricity, electricity_consumption = play_opportunities(light_efficiency=True, labour_efficiency=False,
                                                               scenario=scenario, years=years, growth_plan=growth_plan, avg_photoperiod=avg_photoperiod, light=light, life_span=life_span, electricity_consumption=electricity_consumption, HVAC_multiplier=HVAC_multiplier, light_improvement=light_improvement, cogs_electricity=cogs_electricity)
#cogs_electricity, electricity_consumption = calc_improved_light_efficiency(scenario, years, growth_plan, avg_photoperiod, light, life_span, electricity_consumption, HVAC_multiplier, light_improvement)

'''Recomposing Dataframe'''
risk_dataframe = crop_and_revenue_to_df(risk_dataframe, waste_adjusted_yields_risks, total_sales_risk, vadded_sales, education_rev, tourism_rev, hospitality_rev, grants_rev)
risk_dataframe = cogs_to_df(risk_dataframe, cogs_labour, cogs_media, cogs_packaging,
                                                cogs_seeds_nutrients, cogs_electricity, cogs_water)
risk_dataframe = opex_to_df(risk_dataframe, opex_rent, opex_salaries, opex_other_costs,
                                                opex_insurance, opex_distribution)
# PLANNING DELAY
#risk_dataframe = calc_planning_delay(risk_dataframe, timeseries_yearly, years, scenario)
# REBALANCE DATAFRAME
risk_dataframe = extra_to_df(risk_dataframe, loan_repayments, loan_balance, scenario,
                                                 depreciation)

# ROI

roi_risk = calc_roi(scenario, risk_dataframe, years)
risk_dataframe.loc['Return on Investment'] = roi_risk

risk_dataframe, risk_financial_balance = calc_financial_balance(risk_dataframe, scenario, years, p_box)
risk_counter, pes_counter, trad_counter = pba_risk_assessment(roi_risk, risk_financial_balance, bankruptcy_definition, balance_threshold, years, risk_counter, pes_counter, trad_counter, p_box)
risk_summary = build_financial_summary(risk_dataframe, investment_balance,roi_risk, timeseries_yearly)
         # Rate of Decline
#percent_list = calc_percent_annual_decline(risk_dataframe) # FIX ME

    # CDF Bankruptcy
cdf_counter, cdf_pes_counter, cdf_trad_counter = cdf_bankruptcy_counter(bankruptcy_definition, cdf_counter, cdf_pes_counter, cdf_trad_counter, roi_risk, risk_financial_balance, years, balance_threshold, p_box)

    # CDF Threshold
threshold_counter, thresholds_axis = threshold_probability(threshold_counter, roi, risk_financial_balance, bankruptcy_definition, balance_threshold)

         # COMMENT OUT IF NOT INTERESTED IN RISK PLOTS
#fig1, ax2.plot(risk_dataframe.columns, roi_risk)
#fig1, ax3.plot(risk_dataframe.columns, risk_dataframe.loc['Revenue - Crop Sales'])
#fig1, ax5.plot(risk_dataframe.columns, risk_dataframe.loc['Financial Balance'])

# FIRST PASSAGE TIME
first_passage_df = risk_assessment_probability(cdf_counter, years, simulations, timeseries_yearly, p_box)
first_passage_pes_df = risk_assessment_probability(cdf_pes_counter, years, simulations, timeseries_yearly, p_box)
first_passage_trad_df = risk_assessment_probability(cdf_trad_counter, years, simulations, timeseries_yearly, p_box)

# BANKRUPTCY WITH RECOVERY
risk_assessment_probability_df = risk_assessment_probability(risk_counter, years, simulations, timeseries_yearly, p_box)
risk_assessment_pes_df = risk_assessment_probability(pes_counter, years, simulations, timeseries_yearly, p_box)
risk_assessment_trad_df = risk_assessment_probability(trad_counter, years, simulations, timeseries_yearly, p_box)

percent_df = calc_probability_of_decline(percent_list, simulations) #FIX ME
threshold_df = probability_df(threshold_counter, simulations, thresholds_axis)

'''HERE ARE THE PLOTS!'''
# THIS GRAPH IS TOO CLUTTERED WITH PROBABILITY BOUNDS
#pltem(ax1, financial_annual_overview.columns, financial_annual_overview.loc['Total Revenue'], label='Revenue')
#pltem(ax1, financial_annual_overview.columns, financial_annual_overview.loc['Total COGS'])
#ax1.plot(financial_annual_overview.columns, financial_annual_overview.loc['Total OPEX'], label='OPEX')
#pltem(ax1, financial_annual_overview.columns, financial_annual_overview.loc['Gross Profit'])
#pltem(ax1, financial_annual_overview.columns, financial_annual_overview.loc['Net Profit'])
#pltem(ax6, financial_annual_overview.columns, financial_annual_overview.loc['Total OPEX'])
#ax1.plot(financial_annual_overview.columns, financial_annual_overview.loc['Total OPEX'], label='OPEX')
#ax1.set_xlabel('Year')
#ax1.set_ylabel('Finance (£)')
#ax1.set_title('Annual Financial Overview')
#ax1.legend()
#

SMALL = 8
MEDIUM = 10
LARGE = 12
VLARGE = 20
xticks = 4
yticks = 3

#fig, axes = plt.subplots(nrows=10, ncols=1)
#plt.setp(ax1, xtickslabels =xticks, ytickslabels=yticks)
#plt.locator_params(axis="x", nbins=4)
#plt.locator_params(axis="y", nbins=3)
#plt.rc('xtick', labelsize=MEDIUM)
#plt.rc('ytick', labelsize=MEDIUM)

# ROI GRAPH
pltem_med(ax1, risk_dataframe.columns, roi_risk, shade=True)
pltem(ax1, risk_dataframe.columns, roi_risk, label = '', shade=True)
ax1.plot(timeseries_yearly, bankruptcy_definition, label = 'Threshold', color='k', linestyle='dashed')
ax1.set_xlim(timeseries_yearly[1], timeseries_yearly[-1])
ax1.set_xlabel('Year', fontsize=MEDIUM)
ax1.set_ylabel('ROI (%)', fontsize = MEDIUM)
ax1.set_title('Return on Investment for Farm Lifetime', fontsize=LARGE)
ax1.legend()
ax1.grid()

# Financial Balance Graph
balance_threshold_p = [balance_threshold for i in range(years+1)]
pltem_med(ax2, risk_dataframe.columns, risk_financial_balance, shade=True)
pltem(ax2, risk_dataframe.columns, risk_financial_balance, label='', shade=True)
ax2.plot(timeseries_yearly, balance_threshold_p, label='Threshold', color='k', linestyle='dashed')
ax2.set_xlabel('Year')
ax2.set_ylabel('Financial Balance ({})'.format(scenario.currency))
ax2.set_title('Financial Balance for Farm Lifetime')
ax2.legend()
ax2.grid()

ax3.plot(timeseries_yearly, critical_risk, linestyle='dashed', color='k', lw=1) #label='Critical')
ax3.plot(timeseries_yearly, moderate_risk, linestyle='dashed', color='k', lw=1) #label='Moderate')
ax3.plot(timeseries_yearly, substantial_risk, linestyle='dashed', color='k', lw=1) #label='Substantial')
pltem(ax3, risk_assessment_probability_df.columns, risk_assessment_probability_df.loc['cdf'], label='', shade=True) # ROI AND FINANCIAL BALANCE
ax3.legend()
ax3.set_xlim(timeseries_yearly[0], timeseries_yearly[-1])
ax3.set_ylim(0, 1)
ax3.set_ylabel('Cumulative Probability of Insolvency')
ax3.set_xlabel('Year')
ax3.set_title('Risk Assessment for ROI and Balance')
ax3.text(timeseries_yearly[1], 0.8, 'Critical')
ax3.text(timeseries_yearly[years-10], 0.6, 'Substantial')
ax3.text(timeseries_yearly[years-5], 0.3, 'Moderate')
ax3.text(timeseries_yearly[years-3], 0.05, 'Safe')

ax4.plot(timeseries_yearly, critical_risk, linestyle='dashed', color='k', lw=1) #label='Critical')
ax4.plot(timeseries_yearly, moderate_risk, linestyle='dashed', color='k', lw=1) #label='Moderate')
ax4.plot(timeseries_yearly, substantial_risk, linestyle='dashed', color='k', lw=1) #label='Substantial')
pltem(ax4, risk_assessment_pes_df.columns, risk_assessment_pes_df.loc['cdf'], label='', shade=True) # ROI OR FINANCIAL BALANCE
ax4.legend()
ax4.set_xlim(timeseries_yearly[0], timeseries_yearly[-1])
ax4.set_ylim(0, 1)
ax4.set_ylabel('Probability of Insolvency')
ax4.set_xlabel('Year')
ax4.set_title('Risk Assessment for ROI or Balance')
ax4.text(timeseries_yearly[1], 0.8, 'Critical')
ax4.text(timeseries_yearly[years-10], 0.6, 'Substantial')
ax4.text(timeseries_yearly[years-5], 0.3, 'Moderate')
ax4.text(timeseries_yearly[years-3], 0.05, 'Safe')

ax5.plot(timeseries_yearly, critical_risk, linestyle='dashed', color='k', lw=1) #label='Critical')
ax5.plot(timeseries_yearly, moderate_risk, linestyle='dashed', color='k', lw=1) #label='Moderate')
ax5.plot(timeseries_yearly, substantial_risk, linestyle='dashed', color='k', lw=1) #label='Substantial')
pltem(ax5, risk_assessment_trad_df.columns, risk_assessment_trad_df.loc['cdf'], label='', shade=True) # JUST FINANCIAL BALANCE
ax5.legend()
ax5.set_xlim(timeseries_yearly[0], timeseries_yearly[-1])
ax5.set_ylim(0, 1)
ax5.set_ylabel('Probability of Insolvency')
ax5.set_xlabel('Year')
ax5.set_title('Risk Assessment for Negative Cashflow')
ax5.text(timeseries_yearly[1], 0.8, 'Critical')
ax5.text(timeseries_yearly[years-10], 0.6, 'Substantial')
ax5.text(timeseries_yearly[years-5], 0.3, 'Moderate')
ax5.text(timeseries_yearly[years-3], 0.05, 'Safe')

# pltem(ax6, threshold_df.columns, threshold_df.loc['cdf'], label='CDF', shade=True)
# ax6.set_xlabel('Threshold Financial Balance ({})'.format(scenario.currency))
# ax6.set_ylabel('Probability of Bankruptcy after {} years'.format(years))
# ax6.plot()
# ax6.legend()
# ax6.grid()

# Gross Margin GRAPH
pltem(ax7, risk_dataframe.columns, risk_dataframe.loc['Gross Profit'], label = 'Gross Profit', shade=True)
pltem_med(ax7, risk_dataframe.columns, risk_dataframe.loc['Gross Profit'], shade=True)
ax7.set_xlim(timeseries_yearly[1], timeseries_yearly[-1])
ax7.set_xlabel('Year')
ax7.set_ylabel('Gross Profit ({})'.format(scenario.currency))
ax7.set_title('Gross Profit Chart')
ax7.legend()
ax7.grid()

# REVENUE GRAPH
pltem(ax8, risk_dataframe.columns, risk_dataframe.loc['Total Revenue'], label = '', shade=True)
pltem_med(ax8, risk_dataframe.columns, risk_dataframe.loc['Total Revenue'], shade=True)
ax8.set_xlim(timeseries_yearly[1], timeseries_yearly[-1])
ax8.set_xlabel('Year')
ax8.set_ylabel('Revenue ({})'.format(scenario.currency))
ax8.set_title('Revenue Chart')
ax8.legend()
ax8.grid()

# Cost of Goods Sold GRAPH
pltem(ax9, risk_dataframe.columns, risk_dataframe.loc['Total COGS'], label = '', shade=True)
pltem_med(ax9, risk_dataframe.columns, risk_dataframe.loc['Total COGS'], shade=True)
ax9.set_xlim(timeseries_yearly[1], timeseries_yearly[-1])
ax9.set_xlabel('Year')
ax9.set_ylabel('Cost of Goods Sold ({})'.format(scenario.currency))
ax9.set_title('Cost of Goods Sold Chart')
ax9.legend()
ax9.grid()

# OPEX GRAPH
pltem(ax10, risk_dataframe.columns, risk_dataframe.loc['Total OPEX'], label = '', shade=True)
pltem_med(ax10, risk_dataframe.columns, risk_dataframe.loc['Total OPEX'], shade=True)
ax10.set_xlim(timeseries_yearly[1], timeseries_yearly[-1])
ax10.set_xlabel('Year')
ax10.set_ylabel('OPEX ({})'.format(scenario.currency))
ax10.set_title('Operational Expenditure Chart')
ax10.legend()
ax10.grid()

# Net Profit GRAPH
pltem(ax11, risk_dataframe.columns, risk_dataframe.loc['Net Profit'], label = '', shade=True)
pltem_med(ax11, risk_dataframe.columns, risk_dataframe.loc['Net Profit'], shade=True)
ax11.set_xlim(timeseries_yearly[1], timeseries_yearly[-1])
ax11.set_xlabel('Year')
ax11.set_ylabel('Net Profit ({})'.format(scenario.currency))
ax11.set_title('Net Profit Chart')
ax11.legend()
ax11.grid()

# Yield Graph
cumulative_yield = risk_dataframe.loc['Yield Crop 1'] + risk_dataframe.loc['Yield Crop 2']+ risk_dataframe.loc['Yield Crop 3']+ risk_dataframe.loc['Yield Crop 4']
pltem(ax12, risk_dataframe.columns, cumulative_yield, label = '', shade=True)
pltem_med(ax12, risk_dataframe.columns, cumulative_yield, label = '', shade=True)
ax12.set_xlim(timeseries_yearly[1], timeseries_yearly[-1])
ax12.set_xlabel('Year')
ax12.set_ylabel('Total Yield ({})'.format(scenario.weight_unit))
ax12.set_title('Annual Yield for All Crops')
ax12.legend()
ax12.grid()
plt.show()

# # ax6.plot(percent_decline, probability_of_decline)
# ax6.set_title('Percent Financial Balance Change after {} years'.format(years))
# pltem(ax6, percent_df.columns, percent_df.loc['cdf'], label='CDF')
# ax6.set_xlabel('Percent Balance Change (%)')
# ax6.set_ylabel('Probability of Change')
# #fig2, ax8.set_xlim(-500, 500)
# ax6.set_ylim(0, 1)
# ax6.legend()
# ax6.grid()

# # ax6.plot(percent_decline, probability_of_decline)
# ax6.set_title('Percent Financial Balance Change after {} years'.format(years))
# pltem(ax6, percent_df.columns, percent_df.loc['cdf'], label='CDF')
# ax6.set_xlabel('Percent Balance Change (%)')
# ax6.set_ylabel('Probability of Change')
# #fig2, ax8.set_xlim(-500, 500)
# ax6.set_ylim(0, 1)
# ax6.legend()
# ax6.grid()

#fig1, ax2.plot(risk_dataframe.columns, roi_risk)

# Revenue Graph - NO UNCERTAINTY YET
# pltem(ax2, risk_dataframe.columns, risk_dataframe.loc['Revenue - Crop Sales'], label='Crop Sales' )
# ax2.set_xlabel('Year')
# ax2.set_ylabel('Crop Sales ({})'.format(scenario.currency))ax1.grid()

# ax2.set_title('Crop Sales')
# ax2.legend()

risk_dataframe['Cumulative Sum'] = risk_dataframe.sum(axis=1)
risk_summary['Cumulative Sum'] = risk_dataframe.sum(axis=1)

cum_profit = risk_dataframe.loc['Net Profit']['Cumulative Sum']

export_results(risk_dataframe, risk_summary, risk_dataframe, p_box, 'results_UK.xlsx')

"""FINAL STATEMENTS"""
print (scenario.start_date.strftime('The simulation computes from %d, %b, %Y'), end_date.strftime('until %d, %b, %Y'))      # format_str = "%B %d, %Y"')
#print('The farm is growing Crop1: {}, Crop2 :{}, Crop3: {} and Crop 4:{}'.format(scenario.crop_typ1, scenario.crop_typ2, scenario.crop_typ3, scenario.crop_typ4))
print('Estimated capital expenditure for full-scale farm is: {}{}'.format(scenario.currency,capex_full))
print(risk_dataframe)
print(payback_period)
print('Estimated 15 year cumulative profit is between: {}{} and {}. Avg: {}'.format(scenario.currency,truncate(min(cum_profit)), truncate(max(cum_profit)), median(cum_profit)))


''''END'''