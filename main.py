import os
import matplotlib.pyplot as plt
import math
import pba
from math import pi

import os
import matplotlib.pyplot as plt
import math
import pba
from math import pi
import pba

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
from vf_overview import opex_to_df
from vf_overview import productivity_targets
from vf_overview import plot_radar_chart

from vf_equipment import Lights
from vf_equipment import get_lights
from vf_equipment import System

from risk import build_risk_assessment_counter
from risk import build_risk_curves
from risk import build_risk_dataframe
from risk import calc_customer_withdrawal
from risk import calc_improved_light_efficiency
from risk import calc_pathogen_outbreak
from risk import calc_repairs
from risk import calc_pest_outbreak
from risk import calc_planning_delay
from risk import calc_power_outage
from risk import competitors_risk
from risk import labour_challenges
from risk import build_counter
from risk import calc_percent_annual_decline
from risk import calc_probability_of_decline
from risk import decline_data
from risk import cdf_bankruptcy_counter
from risk import build_bankruptcy_definition
from risk import threshold_probability
from risk import probability_df
from risk import reduced_product_quality
from risk import risk_assessment
from risk import risk_assessment_probability
from risk import improved_labour_efficiency
from risk import labour_challenges

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory

years = 15 # Time series length !!UP TO 20!!
simulations = 50
p_box = "no"
repairs =[]

#Scenario
scenario = get_scenario()
light = get_lights(scenario.light_system)
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
HVAC_multiplier = 1
scenario.currency = '£'

#scenario.electricity_price = pba.norm(0.6, 0.1)

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
#grants_rev[2] = 150000 # How can we factor this into inputs for example?


cogs_labour, direct_labour = calc_direct_labour(farmhand, delivery, part_time, years, scenario)
cogs_media = calc_growing_media(scenario, total_sales, adjusted_yields)
cogs_packaging = calc_packaging(scenario, years, waste_adjusted_yields)
cogs_seeds_nutrients, nutrient_consumption, total_no_of_plants = calc_nutrients_and_num_plants(scenario,cogs_media,adjusted_yields,years)
avg_photoperiod = calc_avg_photoperiod(scenario)
cogs_electricity, electricity_consumption = calc_electricity(scenario, growth_plan, avg_photoperiod, light, years, HVAC_multiplier)
cogs_water, water_consumption = calc_water(scenario, years)

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
investment_balance, payback_period = calc_payback_period(scenario, financial_annual_overview, years, p_box)
financial_annual_overview, financial_balance = calc_financial_balance(financial_annual_overview, scenario, years, p_box)

financial_summary = build_financial_summary(financial_annual_overview, investment_balance, roi, timeseries_yearly)

# Productivity Metrics
productivity_metrics = calc_productivity_metrics(scenario, timeseries_yearly, waste_adjusted_yields, electricity_consumption, direct_labour, water_consumption, staff_list, nutrient_consumption, total_no_of_plants)
crop_productivity_metrics = calc_crop_productivity_metrics(productivity_metrics, growth_plan, scenario)
productivity_targets = productivity_targets(crop_productivity_metrics, scenario)

# Where it gets risky
critical_risk, substantial_risk, moderate_risk = build_risk_curves(years)
bankruptcy_definition, balance_threshold = build_bankruptcy_definition(years)
risk_dataframe = build_risk_dataframe(financial_annual_overview)

# Financial Overview
fig1, ax1 = plt.subplots() # Overview
fig1, ax2 = plt.subplots() # ROI
fig1, ax3 = plt.subplots() # Crop Sales
fig1, ax4 = plt.subplots() # Financial Balance
#fig1, ax5 = plt.subplots()
# fig1, a6 = plt.subplots() # Revenue Streams

# ISO RISK CURVES
fig2, ax7 = plt.subplots() # Risk Assessment Curve
fig2, ax8 = plt.subplots() # Percent Change
fig2, ax9 = plt.subplots() # Threshold Curve
fig2, ax10 = plt.subplots()  # Risk Assessment no Recovery


ax13 =plt.subplots()



for s in range(simulations):
    risk_dataframe = build_risk_dataframe(financial_annual_overview)

         # Pathogen Outbreak
    w_risks = calc_pathogen_outbreak(scenario, years, waste_adjusted_yields)
    w_risks = calc_pest_outbreak(scenario, years, w_risks)
    #w_risks = calc_power_outage(scenario, years, w_risks)
    _, total_sales_risk = calc_produce_sales(w_risks, scenario)
    customer_withdrawal = calc_customer_withdrawal(scenario, years, total_sales_risk)
    repair = calc_repairs(scenario, years)
    labour_damage, labour_extra_cost = labour_challenges(scenario, years, total_sales_risk, cogs_labour)
    cogs_electricity, electricity_consumption = calc_improved_light_efficiency(scenario, years, growth_plan, avg_photoperiod, light, life_span, electricity_consumption)
         # Recomposing Dataframe
    risk_dataframe = crop_and_revenue_to_df(risk_dataframe, w_risks, total_sales_risk, vadded_sales, education_rev, tourism_rev, hospitality_rev, grants_rev)
    risk_dataframe.loc['Revenue - Crop Sales'] -= customer_withdrawal
         #risk_dataframe.loc['Revenue - Crop Sales'] -= labour_damage

    risk_dataframe = cogs_to_df(risk_dataframe, cogs_labour, cogs_media, cogs_packaging,
                                                cogs_seeds_nutrients, cogs_electricity, cogs_water)
    risk_dataframe.loc['COGS - Direct Labour'] += labour_extra_cost


    risk_dataframe = opex_to_df(risk_dataframe, opex_rent, opex_salaries, opex_other_costs,
                                                opex_insurance, opex_distribution)
    #risk_dataframe.loc['OPEX - Other Costs'] += repair
    risk_dataframe = extra_to_df(risk_dataframe, loan_repayments, loan_balance, scenario,
                                                 depreciation)

    risk_dataframe = calc_planning_delay(risk_dataframe, timeseries_yearly, years)

         # ROI
    roi_risk = calc_roi(scenario, risk_dataframe, years)
    risk_dataframe.loc['Return on Investment'] = roi_risk
    risk_dataframe, risk_financial_balance, _ = calc_financial_balance(risk_dataframe, scenario, years, p_box)
    risk_counter, pes_counter, trad_counter = risk_assessment(roi_risk, risk_financial_balance, bankruptcy_definition, balance_threshold, years, risk_counter, pes_counter, trad_counter, p_box)

         # Rate of Decline
    percent_list = calc_percent_annual_decline(risk_dataframe)

    # CDF Bankruptcy
    cdf_counter, cdf_pes_counter, cdf_trad_counter = cdf_bankruptcy_counter(bankruptcy_definition, cdf_counter, cdf_pes_counter, cdf_trad_counter, roi_risk, risk_financial_balance, years, balance_threshold, p_box)

    # CDF Threshold
    threshold_counter, thresholds_axis = threshold_probability(threshold_counter, roi, risk_financial_balance, bankruptcy_definition, balance_threshold)

         # COMMENT OUT IF NOT INTERESTED IN RISK PLOTS
    fig1, ax2.plot(risk_dataframe.columns, roi_risk)
    fig1, ax3.plot(risk_dataframe.columns, risk_dataframe.loc['Revenue - Crop Sales'])
    fig1, ax4.plot(risk_dataframe.columns, risk_dataframe.loc['Financial Balance'])
    #fig1, ax5. plot(risk_dataframe.columns, repair)

# FIRST PASSAGE TIME
first_passage_df = risk_assessment_probability(cdf_counter, years, simulations, timeseries_yearly, p_box)
first_passage_df = risk_assessment_probability(cdf_pes_counter, years, simulations, timeseries_yearly, p_box)
first_passage_df = risk_assessment_probability(cdf_trad_counter, years, simulations, timeseries_yearly, p_box)


# BANKRUPTCY WITH RECOVERY
risk_assessment_probability_df = risk_assessment_probability(risk_counter, years, simulations, timeseries_yearly, p_box)
risk_assessment_pes_df = risk_assessment_probability(pes_counter, years, simulations, timeseries_yearly, p_box)
risk_assessment_trad_df = risk_assessment_probability(trad_counter, years, simulations, timeseries_yearly, p_box)



percent_df = calc_probability_of_decline(percent_list, simulations)
threshold_df = probability_df(threshold_counter, simulations, thresholds_axis)

# Financial Overivew
fig1, ax1.plot(financial_annual_overview.columns, financial_annual_overview.loc['Total Revenue'], label='Revenue')
fig1, ax1.plot(financial_annual_overview.columns, financial_annual_overview.loc['Total COGS'], label='COGS')
fig1, ax1.plot(financial_annual_overview.columns, financial_annual_overview.loc['Total OPEX'], label='OPEX')
fig1, ax1.plot(financial_annual_overview.columns, financial_annual_overview.loc['Gross Profit'], label='Gross Profit')
fig1, ax1.plot(financial_annual_overview.columns, financial_annual_overview.loc['Net Profit'], label='Net Profit')
fig1, ax1.set_xlabel('Year')
fig1, ax1.set_ylabel('Finance ({})'.format(scenario.currency))
fig1, ax1.set_title('Annual Financial Overview')
fig1, ax1.legend()

# ROI
fig1, ax2.plot(financial_annual_overview.columns, roi, label = 'ROI no Risk', linewidth=4)
fig1, ax2.set_xlabel('Year')
fig1, ax2.set_ylabel('ROI (%)')
fig1, ax2.set_title('Return on Investment')
fig1, ax2.legend()

#fig2, ax7.plot(timeseries_yearly, critical_risk, linestyle='dashed', color='g') #label='Critical')
#fig2, ax7.plot(timeseries_yearly, moderate_risk, linestyle='dashed', color='g') #label='Moderate')
#fig2, ax7.plot(timeseries_yearly, substantial_risk, linestyle='dashed', color='g') #label='Substantial')
#fig2, ax7.plot(risk_assessment_probability_df.loc['pdf'], linewidth=2, color='red', label='Risk Curve')
#fig2, ax7.plot(risk_assessment_pes_df.loc['pdf'], linewidth=2, color='red', label='Risk Curve')
#fig2, ax7.plot(risk_assessment_trad_df.loc['pdf'], linewidth=2, color='red', label='Risk Curve')

#fig2, ax7.set_xlim(timeseries_yearly[0], timeseries_yearly[-1])
#fig2, ax7.set_ylim(0, 1)
#fig2, ax7.set_ylabel('Probabiltiy of Bankruptcy')
#fig2, ax7.set_xlabel('Year')
#fig2, ax7.set_title('Risk Assessment')
#fig2, ax7.text(timeseries_yearly[1], 0.8, 'Critical')
#fig2, ax7.text(timeseries_yearly[years-10], 0.6, 'Substantial')
#fig2, ax7.text(timeseries_yearly[years-5], 0.3, 'Moderate')
#fig2, ax7.text(timeseries_yearly[years-3], 0.05, 'Safe')

fig1, ax3.plot(financial_annual_overview.columns, financial_annual_overview.loc['Revenue - Crop Sales'], label='Crop Sales no Risk', linewidth=4)
fig1, ax3.set_xlabel('Year')
fig1, ax3.set_ylabel('Sales ({})'.format(scenario.currency))
fig1, ax3.set_title('Crop Sales')
fig1, ax3.legend()

ax13 = plot_radar_chart(productivity_targets, ax13)

fig1, ax4.plot(financial_annual_overview.columns, financial_annual_overview.loc['Financial Balance'])
fig1, ax4.set_xlabel('Year')
fig1, ax4.set_ylabel('Financial Balance')

# ax8.plot(percent_decline, probability_of_decline)
fig2, ax8.set_title('Percent Financial Balance Change after {} years'.format(years))
fig2, ax8.plot(percent_df.columns, percent_df.loc['pdf'], linewidth=2, color='red', label='PDF')
fig2, ax8.plot(percent_df.columns, percent_df.loc['cdf'], linewidth=2, color='blue', label='CDF')
fig2, ax8.set_xlabel('Percent Balance Change (%)')
fig2, ax8.set_ylabel('Probability of Change')
#fig2, ax8.set_xlim(-500, 500)
fig2, ax8.set_ylim(0, 1)
fig2, ax8.legend()

fig2, ax9.plot(threshold_df.columns, threshold_df.loc['pdf'], linewidth=2, color='red', label='PDF')
fig2, ax9.plot(threshold_df.columns, threshold_df.loc['cdf'], linewidth=2, color='blue', label='CDF')
fig2, ax9.set_xlabel('Threshold Financial Balance ({})'.format(scenario.currency))
fig2, ax9.set_ylabel('Probability of Bankruptcy after {} years'.format(years))
fig2, ax9.plot()
fig2, ax9.legend()

fig2, ax10.set_title('First Passage Time Risk')
fig2, ax10.set_xlabel('Year')
fig2, ax10.set_ylabel('CDF Probability of Bankruptcy')
fig2, ax10.set_xlim(timeseries_yearly[0], timeseries_yearly[-1])
fig2, ax10.set_ylim(0, 1)
fig2, ax10.plot(timeseries_yearly, critical_risk, linestyle='dashed', color='g') #label='Critical')
fig2, ax10.plot(timeseries_yearly, moderate_risk, linestyle='dashed', color='g') #label='Moderate')
fig2, ax10.plot(timeseries_yearly, substantial_risk, linestyle='dashed', color='g') #label='Substantial')
fig2, ax10.plot(first_passage_df.loc['cdf'], linewidth=4, color='red', label='cdf')
fig2, ax10.plot(first_passage_df.loc['pdf'], linewidth=2, color='blue', label='pdf')
fig2, ax10.text(timeseries_yearly[1], 0.8, 'Critical')
fig2, ax10.text(timeseries_yearly[years-10], 0.6, 'Substantial')
fig2, ax10.text(timeseries_yearly[years-5], 0.3, 'Moderate')
fig2, ax10.text(timeseries_yearly[years-3], 0.05, 'Safe')
fig2, ax10.legend()


#ax10.set_xlim(timeseries_yearly[0], timeseries_yearly[-1])
financial_annual_overview['Cumulative Sum'] = financial_annual_overview.sum(axis=1)
cum_profit = financial_annual_overview.loc['Net Profit']['Cumulative Sum']
export_results(financial_annual_overview, financial_summary, risk_dataframe, p_box)
plt.show()

print (scenario.start_date.strftime('The simulation computes from %d, %b, %Y'), end_date.strftime('until %d, %b, %Y'))      # format_str = "%B %d, %Y"')
#print('The farm is growing Crop1: {}, Crop2 :{}, Crop3: {} and Crop 4:{}'.format(scenario.crop_typ1, scenario.crop_typ2, scenario.crop_typ3, scenario.crop_typ4))
print('Estimated capital expenditure for full-scale farm is: {}{}'.format(scenario.currency,scenario.capex_full))
print(financial_annual_overview)
print(payback_period)
print(risk_dataframe)
print('Estimated 15 year cumulative profit is: {}{}'.format(scenario.currency,cum_profit))
