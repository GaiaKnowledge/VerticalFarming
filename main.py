import os
import matplotlib.pyplot as plt
import pba
from math import pi

from vf_overview import build_bankruptcy_definition
from vf_overview import build_dataframe
from vf_overview import build_financial_summary
from vf_overview import build_risk_assessment_counter
from vf_overview import build_risk_curves
from vf_overview import build_risk_dataframe
from vf_overview import calc_adjusted_yield
from vf_overview import calc_adjustment_factors
from vf_overview import calc_avg_photoperiod
from vf_overview import calc_best_yield
from vf_overview import calc_capex
from vf_overview import calc_customer_withdrawal
from vf_overview import calc_crop_productivity_metrics
from vf_overview import calc_depreciation
from vf_overview import calc_direct_labour
from vf_overview import calc_distribution
from vf_overview import calc_education_rev
from vf_overview import calc_electricity
from vf_overview import calc_grants_rev
from vf_overview import calc_growing_media
from vf_overview import calc_hospitality_rev
from vf_overview import calc_improved_light_efficiency
from vf_overview import calc_insurance
from vf_overview import calc_loan_repayments
from vf_overview import calc_nutrients_and_num_plants
from vf_overview import calc_other_costs
from vf_overview import calc_packaging
from vf_overview import calc_pathogen_outbreak
from vf_overview import calc_payback_period
from vf_overview import calc_pest_outbreak
from vf_overview import calc_planning_delay
from vf_overview import calc_power_outage
from vf_overview import calc_produce_sales
from vf_overview import calc_productivity_metrics
from vf_overview import calc_rent
from vf_overview import calc_repairs
from vf_overview import calc_roi
from vf_overview import calc_financial_balance
from vf_overview import calc_salaries
from vf_overview import calc_tourism_rev
from vf_overview import calc_vadded_sales
from vf_overview import calc_waste_adjusted_yield
from vf_overview import calc_water
from vf_overview import cogs_to_df
from vf_overview import competitors_risk
from vf_overview import crop_and_revenue_to_df
from vf_overview import export_results
from vf_overview import extra_to_df
from vf_overview import get_calendar
from vf_overview import get_gp
from vf_overview import get_scenario
from vf_overview import get_staff_list
from vf_overview import improved_labour_efficiency
from vf_overview import labour_challenges
from vf_overview import opex_to_df
from vf_overview import productivity_targets
from vf_overview import reduced_product_quality
from vf_overview import risk_assessment
from vf_overview import risk_assessment_probability
from vf_equipment import Lights
from vf_overview import plot_radar_chart


cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory

years = 15 # Time series length !!UP TO 20!!
simulations = 10

#Equipment
Spectra_Blade_Single_Sided_J = Lights('Intravision Spectra Blade Single Sided - J', 'LED', 'Spectra J', 160,
                                      '32-37.5 (Vdc)', 120, 100, '1.6-3.4', 1.6, 0, '152 degree coverage',
                                      'Passive Air Cooling', 0, 0, 0, 60000, '2.39m x 112mm x 36mm', 5.5,
                                      '3m +-0.2m', 0, '3-year std', 0,
                                      'https://www.intravisiongroup.com/spectra-blades', False)



scenario = get_scenario()
ceo, headgrower, marketer, scientist, sales_person, manager, delivery, farmhand, admin, part_time = get_staff_list(scenario)
end_date, timeseries_monthly, timeseries_yearly = get_calendar(scenario.start_date, years)
growth_plan = get_gp(scenario)
staff_list = get_staff_list(scenario)
capex_pilot, capex_full = calc_capex(scenario, growth_plan)
risk_counter = build_risk_assessment_counter(years)

#scenario.electricity_price = pba.norm(0.6, 0.1)

# byield_crop1, byield_crop2, byield_crop3, byield_crop4 = calc_best_yield(scenario, growth_plan, lettuce_fu_mix, basil_lemon, basil_genovese, none, years)
crop_yields = calc_best_yield(scenario, growth_plan, years)
light_factor, temp_factor, nutrient_factor, co2_factor = calc_adjustment_factors(scenario)
adjusted_yields = calc_adjusted_yield(crop_yields, light_factor, temp_factor, nutrient_factor, co2_factor)
waste_adjusted_yields = calc_waste_adjusted_yield(scenario, adjusted_yields, years)
crop_sales, total_sales = calc_produce_sales(waste_adjusted_yields, scenario)
vadded_sales = calc_vadded_sales(scenario, years)
education_rev = calc_education_rev(scenario, years)
tourism_rev = calc_tourism_rev(scenario, years)
hospitality_rev = calc_hospitality_rev(scenario, years)
grants_rev = calc_grants_rev(years)
grants_rev[1] = 89000 # How can we factor this into inputs for example?


cogs_labour, direct_labour = calc_direct_labour(farmhand, delivery, part_time, years, scenario)
cogs_media = calc_growing_media(total_sales)
cogs_packaging = calc_packaging(scenario, years, waste_adjusted_yields)
cogs_seeds_nutrients, nutrient_consumption, total_no_of_plants = calc_nutrients_and_num_plants(scenario, waste_adjusted_yields)
avg_photoperiod = calc_avg_photoperiod(scenario)
cogs_electricity, electricity_consumption = calc_electricity(scenario, growth_plan, avg_photoperiod, Spectra_Blade_Single_Sided_J, years)
cogs_water, water_consumption = calc_water(scenario, years)

opex_rent = calc_rent(scenario, years)
opex_salaries = calc_salaries(ceo, scientist, marketer, admin, manager, headgrower, sales_person, years)
opex_other_costs = calc_other_costs(scenario, opex_salaries, years)
opex_insurance = calc_insurance(scenario, years)
opex_distribution = calc_distribution(scenario, years)

loan_repayments, loan_balance = calc_loan_repayments(scenario, years)
depreciation, life_span = calc_depreciation(scenario, Spectra_Blade_Single_Sided_J, avg_photoperiod, years)
# Constructing Financial Overview Data Frame
financial_annual_overview, financial_monthly_overview = build_dataframe(timeseries_yearly, timeseries_monthly)
financial_annual_overview = crop_and_revenue_to_df(financial_annual_overview, waste_adjusted_yields, total_sales, vadded_sales, education_rev, tourism_rev, hospitality_rev, grants_rev)
financial_annual_overview = cogs_to_df(financial_annual_overview, cogs_labour, cogs_media, cogs_packaging, cogs_seeds_nutrients, cogs_electricity, cogs_water)
financial_annual_overview = opex_to_df(financial_annual_overview, opex_rent, opex_salaries, opex_other_costs, opex_insurance, opex_distribution)
financial_annual_overview = extra_to_df(financial_annual_overview, loan_repayments, loan_balance, scenario, depreciation)

roi = calc_roi(scenario, financial_annual_overview, years)
financial_annual_overview.loc['Return on Investment'] = roi
investment_balance, payback_period = calc_payback_period(scenario, financial_annual_overview, years)
financial_annual_overview, financial_balance = calc_financial_balance(financial_annual_overview, scenario, years)

financial_summary = build_financial_summary(financial_annual_overview, investment_balance, roi, timeseries_yearly)

# Productivity Metrics
productivity_metrics = calc_productivity_metrics(scenario, timeseries_yearly, waste_adjusted_yields, electricity_consumption, direct_labour, water_consumption, staff_list, nutrient_consumption, total_no_of_plants)
crop_productivity_metrics = calc_crop_productivity_metrics(productivity_metrics, growth_plan, scenario)
productivity_targets = productivity_targets(crop_productivity_metrics, scenario)
print(crop_productivity_metrics)

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
     w_risks = calc_pathogen_outbreak(scenario, years, waste_adjusted_yields)
     w_risks = calc_pest_outbreak(scenario, years, w_risks)
     #w_risks = calc_power_outage(scenario, years, w_risks)
     _, total_sales_risk = calc_produce_sales(w_risks, scenario)
     customer_withdrawal = calc_customer_withdrawal(scenario, years, total_sales_risk)
     repair = calc_repairs(scenario, years)
     labour_damage, labour_extra_cost = labour_challenges(scenario, years, total_sales_risk, cogs_labour)
     cogs_electricity, electricity_consumption = calc_improved_light_efficiency(scenario, years, growth_plan, avg_photoperiod, Spectra_Blade_Single_Sided_J, life_span, electricity_consumption)
     # Recomposing Dataframe
     risk_dataframe = crop_and_revenue_to_df(risk_dataframe, w_risks, total_sales_risk, vadded_sales, education_rev, tourism_rev, hospitality_rev, grants_rev)
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
     risk_dataframe, risk_financial_balance = calc_financial_balance(risk_dataframe, scenario, years)
     risk_counter = risk_assessment(roi_risk, risk_financial_balance, bankruptcy_definition, years, risk_counter)

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

ax6 = plot_radar_chart(productivity_targets, ax6)

plt.show()

print (scenario.start_date.strftime('The simulation computes from %d, %b, %Y'), end_date.strftime('until %d, %b, %Y'))      # format_str = "%B %d, %Y"')
#print('The farm is growing Crop1: {}, Crop2 :{}, Crop3: {} and Crop 4:{}'.format(scenario.crop_typ1, scenario.crop_typ2, scenario.crop_typ3, scenario.crop_typ4))
print('Estimated capital expenditure for full-scale farm is: £{}'.format(capex_full))
print(financial_annual_overview)
print(payback_period)