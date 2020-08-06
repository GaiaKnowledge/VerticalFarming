import os

# from overview import get_scenario
# from overview import get_staff_list
# from overview import get_calendar
# from overview import get_gp
# from overview import calc_capex
# from overview import build_risk_assessment_counter
# from overview import calc_best_yield
# from overview import calc_adjustment_factors
# from overview import calc_adjusted_yield
# from overview import calc_waste_adjusted_yield
# from overview import calc_no_of_plants
# from overview import calc_produce_sales
# from overview import calc_vadded_sales
# from overview import calc_education_rev
# from overview import calc_tourism_rev
# from overview import calc_hospitality_rev
# from overview import calc_grants_rev
# CHANGE THIS TO DO AN EXPLICIT IMPORTS AS ABOVE
from vf_overview import *

from vf_equipment import Lights


cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory

years = 15 # Time series length !!UP TO 20!!
simulations = 20

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
#w1, w2, w3, w4 = calc_waste_adjusted_yield(scenario, adjusted_yields, years)
weight_adjusted_yields = calc_waste_adjusted_yield(scenario, adjusted_yields, years)
crop_sales, total_sales = calc_produce_sales(weight_adjusted_yields, scenario)
vadded_sales = calc_vadded_sales(scenario, years)
education_rev = calc_education_rev(scenario, years)
tourism_rev = calc_tourism_rev(scenario, years)
hospitality_rev = calc_hospitality_rev(scenario, years)
grants_rev = calc_grants_rev(years)

cogs_labour, direct_labour = calc_direct_labour(farmhand, delivery, part_time, years, months_in_a_year, scenario)
cogs_media = calc_growing_media(total_sales)
cogs_packaging = calc_packaging(scenario, years, weight_adjusted_yields)
cogs_seeds_nutrients, nutrient_consumption, total_no_of_plants = calc_nurients_and_num_plants(scenario, weight_adjusted_yields)
avg_photoperiod = calc_avg_photoperiod(scenario)
cogs_electricity, electricity_consumption = calc_electricity(scenario, growth_plan, avg_photoperiod, Spectra_Blade_Single_Sided_J, days_in_year, years)
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
financial_annual_overview = crop_and_revenue_to_df(financial_annual_overview, w1, w2, w3, w4, total_sales, vadded_sales, education_rev, tourism_rev, hospitality_rev, grants_rev)
financial_annual_overview = cogs_to_df(financial_annual_overview, cogs_labour, cogs_media, cogs_packaging, cogs_seeds_nutrients, cogs_electricity, cogs_water)
financial_annual_overview = opex_to_df(financial_annual_overview, opex_rent, opex_salaries, opex_other_costs, opex_insurance, opex_distribution)
financial_annual_overview = extra_to_df(financial_annual_overview, loan_repayments, loan_balance, scenario, depreciation)

roi = calc_roi(scenario, financial_annual_overview, years)
financial_annual_overview.loc['Return on Investment'] = roi
investment_balance, payback_period = calc_payback_period(scenario, financial_annual_overview, years)

financial_summary = build_financial_summary(financial_annual_overview, investment_balance, roi, timeseries_yearly)

# Productivity Metrics

productivity_metrics = calc_productivity_metrics(scenario, timeseries_yearly, w1, w2, w3, w4, electricity_consumption, direct_labour, water_consumption, staff_list, nutrient_consumption, total_no_of_plants)
crop_productivity_metrics = calc_crop_productivity_metrics(productivity_metrics, growth_plan, scenario)
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
     cogs_electricity, electricity_consumption = calc_improved_light_efficiency(scenario, years, growth_plan, avg_photoperiod, Spectra_Blade_Single_Sided_J, life_span, electricity_consumption, days_in_year)
     # Recomposing Dataframe
     risk_dataframe = crop_and_revenue_to_df(risk_dataframe, w1_risk, w2_risk, w3_risk, w4_risk, total_sales_risk, vadded_sales, education_rev, tourism_rev, hospitality_rev, grants_rev)
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
