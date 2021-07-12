import pba

import os
import matplotlib.pyplot as plt
import math
import pba
#from pbox import pnt
#from pbox import rng

from math import pi

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

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory

years = 15 # Time series length !!UP TO 20!!
simulations = 1
p_box = "yes"
percent_list = []

#Scenario

scenario = get_scenario()
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
scenario.electricity_price = pba.Pbox(pba.I(0.0734, 0.1079))
part_time.hours_full = part_time.hours * pba.Pbox(pba.I(scenario.growing_area_mulitplier*0.6, scenario.growing_area_mulitplier*1))
scenario.education_multiplier = 1.05
HVAC_multiplier = pba.Pbox(pba.I(1.05,1.2))
scenario.vadded_products_multiplier = pba.norm(scenario.vadded_products_multiplier, (scenario.vadded_products_multiplier*1.5 - scenario.vadded_products_multiplier*0.5)/4)
scenario.education_multiplier = pba.norm(scenario.education_multiplier, (scenario.education_multiplier*1.5 - scenario.education_multiplier*0.5)/4)
scenario.tourism_multiplier = pba.norm(scenario.tourism_multiplier, (scenario.tourism_multiplier*1.5 - scenario.tourism_multiplier*0.5)/4)
scenario.hospitality_multiplier = pba.norm(scenario.hospitality_multiplier, (scenario.hospitality_multiplier*1.5 - scenario.hospitality_multiplier*0.5)/4)
scenario.labour_improvement = pba.Pbox(pba.I(scenario.labour_improvement*0.5, scenario.labour_improvement*1.5))
light_improvement = pba.Pbox(pba.I(0.5, 0.9)) # Upper lower guess
scenario.monthly_distribution_y2 = pba.Pbox(pba.I(scenario.monthly_distribution_y1,scenario.monthly_distribution_y2))
#scenario.crop_parameters[0].price1 = pba.Pbox(pba.I(10,13))#THIS INTERVAL SHOULD AFFECT RISK GRAPH DRASICTLLY
scenario.other_costs_full = pba.Pbox(pba.I(scenario.other_costs_full*0.5,scenario.other_costs_full*1.5))

"""INPUTS CHANGED FOR AFTER INTERVENTIONS"""
scenario.capex_full += pba.Pbox(pba.I(20000,30000))
#manager.count_pilot = 2
#manager.count_full = 2
#sales_person.count_pilot = 1
#sales_person.count_full = 1
scenario.climate_control = 'High'
scenario.climate_control = 'Medium'
scenario.nutrient_control = 'High'
scenario.co2_enrichment = 'Yes'
scenario.packaging_cost_full = 0.60
scenario.packaging_cost_pilot = 1
scenario.monthly_distribution_y2 = pba.Pbox(pba.I(scenario.monthly_distribution_y1,scenario.monthly_distribution_y1*1.3))
#scenario.education_avg_revenue_y1 = 4000
scenario.grants_rev_y2 += 70000 #pba.Pbox(pba.I(75000,100000))
scenario.electricity_price = 0.0734
scenario.other_costs_full = pba.Pbox(pba.I(scenario.other_costs_full,scenario.other_costs_full*2.5))

#scenario.crop_parameters[0].customer_percent = 1


# byield_crop1, byield_crop2, byield_crop3, byield_crop4 = calc_best_yield(scenario, growth_plan, lettuce_fu_mix, basil_lemon, basil_genovese, none, years)
crop_yields = calc_best_yield(scenario, growth_plan, years, p_box)
light_factor, temp_factor, nutrient_factor, co2_factor = calc_adjustment_factors(scenario, p_box)
adjusted_yields = calc_adjusted_yield(crop_yields, light_factor, temp_factor, nutrient_factor, co2_factor)
waste_adjusted_yields = calc_waste_adjusted_yield(scenario, adjusted_yields, years, p_box)
crop_sales, total_sales = calc_produce_sales(waste_adjusted_yields, scenario)
vadded_sales = calc_vadded_sales(scenario, years)
education_rev = calc_education_rev(scenario, years)
tourism_rev = calc_tourism_rev(scenario, years)
hospitality_rev = calc_hospitality_rev(scenario, years)
grants_rev = calc_grants_rev(years, scenario)
grants_rev[1] = 89000 # How can we factor this into inputs for example?
#grants_rev[2] = 105000 # How can we factor this into inputs for example?

cogs_labour, direct_labour = calc_direct_labour(farmhand, delivery, part_time, years, scenario)
cogs_media = calc_growing_media(scenario, total_sales, adjusted_yields)
cogs_packaging = calc_packaging(scenario, years, waste_adjusted_yields)
cogs_seeds_nutrients, nutrient_consumption, total_no_of_plants = calc_nutrients_and_num_plants(scenario, cogs_media, adjusted_yields, years)
avg_photoperiod = calc_avg_photoperiod(scenario)
cogs_electricity, electricity_consumption = calc_electricity(scenario, growth_plan, avg_photoperiod, light, years, HVAC_multiplier)
cogs_water, water_consumption = calc_water(scenario, years)

opex_rent = calc_rent(scenario, years)
opex_salaries = calc_salaries(ceo, scientist, marketer, admin, manager, headgrower, sales_person, years)
opex_other_costs = calc_other_costs(scenario, opex_salaries, years)
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

financial_annual_overview, financial_balance, financial_balance_min_max = calc_financial_balance(financial_annual_overview, scenario, years, p_box)

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
_, total_sales_risk = calc_produce_sales(w_risks, scenario)
# Customer Withdrawalpathogen_outbreak
#customer_withdrawal = calc_customer_withdrawal(scenario, years, total_sales_risk)
# Repair Risk
#repair = calc_repairs(scenario, years)
# Labour Risks
#labour_damage, labour_extra_cost = labour_challenges(scenario, years, total_sales_risk, cogs_labour)
# Electricity efficiency improvements
cogs_electricity, electricity_consumption = calc_improved_light_efficiency(scenario, years, growth_plan, avg_photoperiod, light, life_span, electricity_consumption, HVAC_multiplier, light_improvement)

'''Recomposing Dataframe'''
risk_dataframe = crop_and_revenue_to_df(risk_dataframe, w_risks, total_sales_risk, vadded_sales, education_rev, tourism_rev, hospitality_rev, grants_rev)
#risk_dataframe.loc['Revenue - Crop Sales'] -= customer_withdrawal
         #risk_dataframe.loc['Revenue - Crop Sales'] -= labour_damage

risk_dataframe = cogs_to_df(risk_dataframe, cogs_labour, cogs_media, cogs_packaging,
                                                cogs_seeds_nutrients, cogs_electricity, cogs_water)

#risk_dataframe.loc['COGS - Direct Labour'] += labour_extra_cost

risk_dataframe = opex_to_df(risk_dataframe, opex_rent, opex_salaries, opex_other_costs,
                                                opex_insurance, opex_distribution)
#risk_dataframe.loc['OPEX - Other Costs'] += repair
risk_dataframe = extra_to_df(risk_dataframe, loan_repayments, loan_balance, scenario,
                                                 depreciation)

#risk_dataframe = calc_planning_delay(risk_dataframe, timeseries_yearly, years)

         # ROI

roi_risk = calc_roi(scenario, risk_dataframe, years)
risk_dataframe.loc['Return on Investment'] = roi_risk

risk_dataframe, risk_financial_balance, risk_balance_min_max = calc_financial_balance(risk_dataframe, scenario, years, p_box)
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

# ROI GRAPH
pltem(ax1, risk_dataframe.columns, roi_risk, label = 'ROI', shade=True)
ax1.plot(timeseries_yearly, bankruptcy_definition, label = 'Threshold', color='k', linestyle='dashed')
ax1.set_xlabel('Year')
ax1.set_ylabel('ROI (%)')
ax1.set_title('Return on Investment')
ax1.legend()
ax1.grid()

#fig1, ax2.plot(risk_dataframe.columns, roi_risk)

# Revenue Graph - NO UNCERTAINTY YET
# pltem(ax2, risk_dataframe.columns, risk_dataframe.loc['Revenue - Crop Sales'], label='Crop Sales' )
# ax2.set_xlabel('Year')
# ax2.set_ylabel('Crop Sales ({})'.format(scenario.currency))ax1.grid()

# ax2.set_title('Crop Sales')
# ax2.legend()
ax2.plot(timeseries_yearly, critical_risk, linestyle='dashed', color='g') #label='Critical')
ax2.plot(timeseries_yearly, moderate_risk, linestyle='dashed', color='g') #label='Moderate')
ax2.plot(timeseries_yearly, substantial_risk, linestyle='dashed', color='g') #label='Substantial')
pltem(ax2, risk_assessment_probability_df.columns, risk_assessment_probability_df.loc['cdf'], label='ROI + Balance', shade=True) # ROI AND FINANCIAL BALANCE
ax2.legend()
ax2.set_xlim(timeseries_yearly[0], timeseries_yearly[-1])
ax2.set_ylim(0, 1)
ax2.set_ylabel('Probability of Bankruptcy')
ax2.set_xlabel('Year')
ax2.set_title('Risk Assessment for ROI and Balance')
ax2.text(timeseries_yearly[1], 0.8, 'Critical')
ax2.text(timeseries_yearly[years-10], 0.6, 'Substantial')
ax2.text(timeseries_yearly[years-5], 0.3, 'Moderate')
ax2.text(timeseries_yearly[years-3], 0.05, 'Safe')

ax3.plot(timeseries_yearly, critical_risk, linestyle='dashed', color='g') #label='Critical')
ax3.plot(timeseries_yearly, moderate_risk, linestyle='dashed', color='g') #label='Moderate')
ax3.plot(timeseries_yearly, substantial_risk, linestyle='dashed', color='g') #label='Substantial')
pltem(ax3, risk_assessment_pes_df.columns, risk_assessment_pes_df.loc['cdf'], label='ROI or Balance', shade=True) # ROI OR FINANCIAL BALANCE
ax3.legend()
ax3.set_xlim(timeseries_yearly[0], timeseries_yearly[-1])
ax3.set_ylim(0, 1)
ax3.set_ylabel('Probability of Bankruptcy')
ax3.set_xlabel('Year')
ax3.set_title('Risk Assessment for ROI or Balance')
ax3.text(timeseries_yearly[1], 0.8, 'Critical')
ax3.text(timeseries_yearly[years-10], 0.6, 'Substantial')
ax3.text(timeseries_yearly[years-5], 0.3, 'Moderate')
ax3.text(timeseries_yearly[years-3], 0.05, 'Safe')

ax4.plot(timeseries_yearly, critical_risk, linestyle='dashed', color='g') #label='Critical')
ax4.plot(timeseries_yearly, moderate_risk, linestyle='dashed', color='g') #label='Moderate')
ax4.plot(timeseries_yearly, substantial_risk, linestyle='dashed', color='g') #label='Substantial')
pltem(ax4, risk_assessment_trad_df.columns, risk_assessment_trad_df.loc['cdf'], label='Balance', shade=True) # JUST FINANCIAL BALANCE
ax4.legend()
ax4.set_xlim(timeseries_yearly[0], timeseries_yearly[-1])
ax4.set_ylim(0, 1)
ax4.set_ylabel('Probability of Bankruptcy')
ax4.set_xlabel('Year')
ax4.set_title('Risk Assessment for Negative Cashflow')
ax4.text(timeseries_yearly[1], 0.8, 'Critical')
ax4.text(timeseries_yearly[years-10], 0.6, 'Substantial')
ax4.text(timeseries_yearly[years-5], 0.3, 'Moderate')
ax4.text(timeseries_yearly[years-3], 0.05, 'Safe')

balance_threshold_p = [balance_threshold for i in range(years+1)]
pltem(ax5, risk_dataframe.columns, risk_balance_min_max, label='', shade=True)
ax5.plot(timeseries_yearly, balance_threshold_p, label='Threshold', color='k', linestyle='dashed')
ax5.set_xlabel('Year')
ax5.set_ylabel('Financial Balance ({})'.format(scenario.currency))
ax5.set_title('Financial Balance for Farm Company')
ax5.legend()
ax5.grid()

# # ax8.plot(percent_decline, probability_of_decline)
# ax6.set_title('Percent Financial Balance Change after {} years'.format(years))
# pltem(ax6, percent_df.columns, percent_df.loc['cdf'], label='CDF')
# ax6.set_xlabel('Percent Balance Change (%)')
# ax6.set_ylabel('Probability of Change')
# #fig2, ax8.set_xlim(-500, 500)
# ax6.set_ylim(0, 1)
# ax6.legend()
# ax6.grid()

pltem(ax7, threshold_df.columns, threshold_df.loc['cdf'], label='CDF', shade=True)
ax7.set_xlabel('Threshold Financial Balance ({})'.format(scenario.currency))
ax7.set_ylabel('Probability of Bankruptcy after {} years'.format(years))
ax7.plot()
ax7.legend()
ax7.grid()

# Gross Margin GRAPH
pltem(ax8, risk_dataframe.columns, risk_dataframe.loc['Gross Profit'], label = 'Gross Profit', shade=True)
ax8.set_xlabel('Year')
ax8.set_ylabel('Gross Profit ({})'.format(scenario.currency))
ax8.set_title('Gross Profit Chart')
ax8.legend()
ax8.grid()

# REVENUE GRAPH
pltem(ax9, risk_dataframe.columns, risk_dataframe.loc['Total Revenue'], label = 'Revenue', shade=True)
ax9.set_xlabel('Year')
ax9.set_ylabel('Revenue ({})'.format(scenario.currency))
ax9.set_title('Revenue Chart')
ax9.legend()
ax9.grid()

# Cost of Goods Sold GRAPH
pltem(ax10, risk_dataframe.columns, risk_dataframe.loc['Total COGS'], label = 'Gross Profit', shade=True)
ax10.set_xlabel('Year')
ax10.set_ylabel('Cost of Goods Sold ({})'.format(scenario.currency))
ax10.set_title('Cost of Goods Sold Chart')
ax10.legend()
ax10.grid()

# OPEX GRAPH
pltem(ax11, risk_dataframe.columns, risk_dataframe.loc['Total OPEX'], label = 'OPEX', shade=True)
ax11.set_xlabel('Year')
ax11.set_ylabel('OPEX ({})'.format(scenario.currency))
ax11.set_title('Operational Expenditure Chart')
ax11.legend()
ax11.grid()

# Net Profit GRAPH
pltem(ax12, risk_dataframe.columns, risk_dataframe.loc['Net Profit'], label = 'Net Profit', shade=True)
ax12.set_xlabel('Year')
ax12.set_ylabel('Net Profit ({})'.format(scenario.currency))
ax12.set_title('Net Profit Chart')
ax12.legend()
ax12.grid()

# Net Profit GRAPH
cumulative_yield = risk_dataframe.loc['Yield Crop 1'] + risk_dataframe.loc['Yield Crop 2']+ risk_dataframe.loc['Yield Crop 3']+ risk_dataframe.loc['Yield Crop 4']
pltem(ax13, risk_dataframe.columns, cumulative_yield, label = 'Total Yield', shade=True)
ax13.set_xlabel('Year')
ax13.set_ylabel('Total Yield {}'.format(scenario.weight_unit))
ax13.set_title('Yield Chart')
ax13.legend()
ax13.grid()
plt.show()


risk_dataframe['Cumulative Sum'] = risk_dataframe.sum(axis=1)
risk_summary['Cumulative Sum'] = risk_dataframe.sum(axis=1)

cum_profit = risk_dataframe.loc['Net Profit']['Cumulative Sum']

export_results(risk_dataframe, risk_summary, risk_dataframe, p_box)

"""FINAL STATEMENTS"""
print (scenario.start_date.strftime('The simulation computes from %d, %b, %Y'), end_date.strftime('until %d, %b, %Y'))      # format_str = "%B %d, %Y"')
#print('The farm is growing Crop1: {}, Crop2 :{}, Crop3: {} and Crop 4:{}'.format(scenario.crop_typ1, scenario.crop_typ2, scenario.crop_typ3, scenario.crop_typ4))
print('Estimated capital expenditure for full-scale farm is: {}{}'.format(scenario.currency,capex_full))
print(risk_dataframe)
print(payback_period)
print('Estimated 15 year cumulative profit is between: {}{} and {}'.format(scenario.currency,min(cum_profit), max(cum_profit)))


''''END'''