import math
import numpy as np
import pandas as pd
import random
import collections

MONTHS_IN_YEAR = 12
DAYS_IN_YEAR = 365.25

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

def risk_assessment(roi, financial_balance, bankruptcy_definition, years, risk_counter):
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

        if roi[y] < bankruptcy_definition[y] and financial_balance[y] < 0:
            risk_counter[y] += 1
        else:
            risk_counter[y] += 0

    return risk_counter
def risk_assessment_probability(counter, years, simulations, timeseries_yearly):
    """Risk Assessment Probability of Bankruptcy out of X Simulations

        Args:
            risk_assessment_counter (list): The farm scenario
            years (int): No. of years for analysis
            simulations (int): The number of simulations for Montecarlo Analysis

        Returns:
            risk_assessment_probability (list): Timeseries of probabiltiy of simulations that go bankrupt
    """

    risk_assessment_pdf = counter

    for y in range(years+1):
        risk_assessment_pdf[y] /= simulations

    risk_assessment_cdf = np.cumsum(risk_assessment_pdf)

    assessment_df = pd.DataFrame(index=['pdf', 'cdf'], columns=timeseries_yearly)
    assessment_df.loc['pdf'] = risk_assessment_pdf
    assessment_df.loc['cdf'] = risk_assessment_cdf

    return assessment_df

# Risks
def calc_pathogen_outbreak(scenario, years, waste_adjusted_yields):
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

    # w_risks = []
    # for w in waste_adjusted_yields:
    #     w_risks.append([a * b for a, b in zip(w, pathogen_outbreak)])
    # # HACK!!! THIS NEED TO BE FIXED TO RETURN A LIST
    # w1_risk, w2_risk, w3_risk, w4_risk = w_risks

    w_risks = []
    for wyield in waste_adjusted_yields:
        this_yield = []
        for y in range(years+1):
            this_yield.append(wyield[y]*(pathogen_outbreak[y]))
        w_risks.append(this_yield)

    return w_risks

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

def calc_pest_outbreak(scenario, years, waste_adjusted_yields):
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

    # w1_risk = [a * b for a, b in zip(w1, pest_outbreak)]
    # w2_risk = [a * b for a, b in zip(w2, pest_outbreak)]
    # w3_risk = [a * b for a, b in zip(w3, pest_outbreak)]
    # w4_risk = [a * b for a, b in zip(w4, pest_outbreak)]
    #
    w_risks = []

    for wyield in waste_adjusted_yields:
        this_yield = []
        for y in range(years+1):
            this_yield.append(wyield[y]*(pest_outbreak[y]))
        w_risks.append(this_yield)

    return w_risks

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
    power_outage = np.random.choice(3, years+1, p=[p_no_outage, p_outage, p_two_outage])
    power_outage = [x * months_harvest for x in power_outage]
    assert len(power_outage) == len(w1), "jmht arrays were of unmatching sizes!"
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


def calc_improved_light_efficiency(scenario, years, gp, avg_photoperiod, lights, life_span, electricity_consumption):
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

    new_lights_consumption = (avg_photoperiod * new_wattage_requirement * gp.no_lights_full * DAYS_IN_YEAR)

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
    customer_sentiment = 0
    return customer_sentiment


def calc_percent_annual_decline(df, percent_list):
    """Annual % Change Formula
    = ((Ending Number/Beginning Number)^(1/Years Difference) - 1) x 100
    """

    balance_change = df.iloc[32, -1] - df.iloc[32, 0]
    balance_annual_percent_change = (balance_change/df.iloc[32, 0]) * 100

    rounded_percent_change = int(math.ceil(balance_annual_percent_change/50.0)) * 50

    percent_list.append(rounded_percent_change)


    # if balance_change < 0:
    #     new_balance_change = balance_change * (-1)
    #     decline = 'yes'
    # elif balance_change >= 0:
    #     new_balance_change = balance_change
    #     decline = 'no'


    return percent_list

def build_counter(thresholds):

    counter =  [0] * len(np.arange(-500, 510, thresholds))
    return counter

def calc_probability_of_decline(percent_list, simulations):   # decline_counter):
    """Probability of Decline:
    Thresholds every 10% decline """

    percent_list.sort()

    counter = collections.Counter(percent_list)
    values = counter.keys()
    freq = counter.values()

    probability = [i / simulations for i in freq]

    #data = np.array(list(dict.items()))

    data_cdf = list(np.cumsum(probability))

    percent_df = pd.DataFrame(index =['pdf', 'cdf'], columns=values)
    percent_df.loc['pdf'] = probability
    percent_df.loc['cdf'] = data_cdf


    #bins = list(np.arange(-500, 525, 25))


    #df_probability_of_change = pd.DataFrame({'percent': percent_annual_list})
    #df_probability_of_change['bins'] = pd.cut(x=['percent_list'], bins=bins)


    # Round up to ten


    #
    # rounded_percent_change = int(math.ceil(balance_annual_percent_change/50.0)) * 50
    #
    # list_loc = int(rounded_percent_change/50)
    # print(list_loc)
    #
    #
    #
    # if 0 <= rounded_percent_change <= 500:
    #     decline_counter[list_loc+25] += 1
    # elif rounded_percent_change > 500:
    #     decline_counter[-1] += 1
    # elif 0 > rounded_percent_change >= (-500):
    #     decline_counter[-list_loc] += 1
    # else:
    #     decline_counter[0] += 1

    return percent_df

def decline_data(decline_counter, simulations):

    probability_percent_decline = [i / simulations for i in decline_counter]

    pdf_data = probability_percent_decline
    cdf_data = np.cumsum(pdf_data)

    columns = np.arange(-500, 510, 50)


    decline_dataframe = pd.DataFrame(index=['pdf', 'cdf'], columns=columns)
    decline_dataframe.loc['pdf'] = pdf_data
    decline_dataframe.loc['cdf'] = cdf_data

    return decline_dataframe

def cdf_bankruptcy_counter(bankruptcy_definition, cdf_counter, roi, financial_balance, years, timeseries_yearly):
    """Risk Assessment Cumulative Distributon Function of Bankruptcy out of X Simulations for Y Years

        Args:
             risk_assessment_counter (list): The farm scenario
             years (int): No. of years for analysis
             simulations (int): The number of simulations for Montecarlo Analysis

        Returns:
             cdf_bankruptcy(list): Timeseries of probabiltiy of simulations that go bankrupt
     """

    for y in range(years + 1):
        if roi[y] < bankruptcy_definition[y] and financial_balance[y] < 0:
            cdf_counter[y] += 1
            break
        else:
            cdf_counter[y] += 0

    return cdf_counter


    # def build_risk_dataframe(financial_annual_overview):
    #     """Build risk dataframe
    #
    #         Notes:
    #             Copies financial_annual_overview
    #         Args:
    #             financial_annual_overview (dataframe): An annual overview of financial data
    #
    #         Returns:
    #             risk_dataframe (dataframe): An instance of a annual overview of financial data with a simulation of risk
    #     """
    #
    #     risk_dataframe = financial_annual_overview.copy()
    #     return risk_dataframe
    #
    # # ROI Risk Assessment Curves
    # def build_risk_curves(years):
    #     """Creating lines/curves for risk thresholds on risk assessment graph for critical, moderate, substantial and safe zones
    #
    #         Notes:
    #             Safe zone is categorised as under moderate risk
    #         Args:
    #             years (int): No. of years for analysis
    #
    #         Returns:
    #             critical_risk (list):
    #             moderate_risk (list):
    #             substantial_risk (list):
    #
    #         TO DO:
    #             Allow flexibility of risk threshold definitions which are currently fixed
    #
    #     """
    #
    #     crit_def_prob = 0.50
    #     crit_def_years = 3
    #     sub_def_prob = 0.25
    #     sub_def_years = 5
    #     mod_def_prob = 0.1
    #     mod_def_years = 10
    #
    #     critical_risk = []
    #     substantial_risk = []
    #     moderate_risk = []
    #
    #     for y in range(years + 1):
    #         critical_risk.append(y * crit_def_prob / crit_def_years)
    #         substantial_risk.append(y * sub_def_prob / sub_def_years)
    #         moderate_risk.append(y * mod_def_prob / mod_def_years)
    #
    #     return critical_risk, substantial_risk, moderate_risk
    #
    # def build_bankruptcy_definition(years):
    #     """Build a bankruptcy definition
    #
    #         Notes:
    #             This function is set according to a line of best fit from Year 0 at -10% ROI to 10% ROI by Year 7.
    #
    #         Args:
    #             years (int): No. of years for analysis
    #
    #         Returns:
    #             Bankruptcy definition (list): A timeseries of the bankruptcy threshold graph
    #
    #         TO DO:
    #         Allow flexibility of bankruptcy definition by allowing input of two data points rather than assuming (-10%, 0) and (10%, 7)
    #
    #     """
    #
    #     bankruptcy_definition = []
    #     for y in range(years + 1):
    #         # Threshold for bankruptcy
    #         if y <= 7:
    #             bankruptcy_definition.append(y * 2.8571 - 10)  # Year 0 - below 10% ROI, Year 7 - 10% ROI
    #         elif y > 7:
    #             bankruptcy_definition.append(10)
    #
    #     return bankruptcy_definition
    #
    #     return bankruptcy_definition
    #
    # def build_risk_assessment_counter(years):
    #     """Build a risk counter
    #
    #         Args:
    #             years (int): No. of years for analysis
    #
    #         Returns:
    #             risk_counter (list): An empty list for keeping track of bankruptcy events
    #     """
    #
    #     risk_counter = []
    #     for y in range(years + 1):
    #         risk_counter.append(0)
    #     return risk_counter
    #
    # def risk_assessment(roi, financial_balance, bankruptcy_definition, years, risk_counter):
    #     """Risk Assessment of Bankruptcy Calculation
    #
    #         Args:
    #             roi (list): The farm scenario
    #             bankruptcy_definition (list): The threshold line of bankruptcy
    #             years (int): No. of years for analysis
    #             risk_counter (list): Waste-adjusted yield for crop 1
    #             # Investment balance (list)
    #
    #         Returns:
    #             risk_counter (list): A counter for each year that tallies up the number of times that the ROI falls under the bankruptcy threshold
    #
    #         TO DO:
    #         Include investment balance < 0 as a necessary requisite for bankruptcy
    #     """
    #
    #     for y in range(years + 1):
    #
    #         if roi[y] < bankruptcy_definition[y] and financial_balance[y] < 0:
    #             risk_counter[y] += 1
    #         else:
    #             risk_counter[y] += 0
    #
    #     return risk_counter
    #
    # def risk_assessment_probability(risk_assessment_counter, years, simulations):
    #     """Risk Assessment Probability of Bankruptcy out of X Simulations
    #
    #         Args:
    #             risk_assessment_counter (list): The farm scenario
    #             years (int): No. of years for analysis
    #             simulations (int): The number of simulations for Montecarlo Analysis
    #
    #         Returns:
    #             risk_assessment_probability (list): Timeseries of probabiltiy of simulations that go bankrupt
    #     """
    #
    #     risk_assessment_probability = risk_assessment_counter
    #
    #     for y in range(years + 1):
    #         risk_assessment_probability[y] /= simulations
    #
    #     return risk_assessment_probability

# class Risks(object, scenario):
#
#     def pathogen_outbreak(self):
#         """Pathogen outbreak
#             Reduced yield for a given month
#             Max: 100% reduced yield
#             Minimum: 5%
#             AVG: 15%
#             Std Dev: 4
#             Frequency: 1x a year
#             Cause: Low grower experience/low humditiy control increase risk of disease
#         """
#         if scenario.biosecurity_level = 'High':
#
#         elif scenario.biosecurity_level = 'Medium':
#
#         elif scenario.biosecurity_level = 'Low':
#
#
#     def repairs(self):
#         """Repairs
#             After 12-18 months
#             Max: 20% of equipment
#             Minimum: 0.2% of equipment
#             AVG: 1%
#             Std Dev: 4
#             Frequency: 2x a year
#             Typical case: high automation, higher repair costs
#         """
#         scenario.capex
#
#     def customer_withdrawal(self, total_sales):
#         """Customer Withdrawl
#            Reduced Revenue
#            Max: 30% Revenue
#            Min: 1% revenue
#            AVG: 5%
#            Std Dev: 8
#            Frequency: 1x every 2 years
#            Typical case: To retail business model
#         """
#         total_sales
#
#     def labour_challenges(self):
#         """Labour Challenges
#             High labour costs, reduced yield
#             Max: 50% more labour costs
#             Minimum: 5% more labour reduced yield
#             AVG: 15%
#             Std Dev: 5
#             Frequency: Continous after 6 months
#             Cause: Low automation, high no. of tiers
#         """
#
#     def reduced_product_quality(self):
#         """Reduced Product Quality
#             reduced yield
#             Max: 20% price reduction
#             Minimum: 5%
#             AVG: 15%
#             Std Dev: 3
#             Frequency: 2x a year
#             Cause: First year, low grower experience, no climate control
#         """
#     def pest_outbreak(self):
#         """Pest Outbreak
#             reduced yield
#             Max: 100% reduced yield/month
#             Minimum: 0
#             AVG: 10%
#             Std Dev: 4
#             Frequency: 1x a year
#             Cause: Poor insulation, no IPM, low humidity control
#         """
#         if
#
#     def competitors(self):
#         """Competitor
#             reduced revenue
#             Max: 25% revenue
#             Minimum: 0
#             AVG: 5%
#             Std Dev: 4
#             Frequency: Low
#             Cause: Crop/business model dependant
#         """
#
#
#
#
#
#     def electrical_blackout(self):
#         """Competitor
#             reduced yield
#             Max: 100% reduced yield
#             Minimum: 0
#             AVG: 75%
#             Std Dev: 2
#             Frequency: Low
#             Cause: Aeroponics  without back-up system
#         """
# # Risks
#
# # Opportunities
#
#     def improved_labour_efficiency(self):
#         """Improved labour efficency
#             Reduction in hours
#             Max: 60% reduction in COGS - direct labour
#             Minimum: 0
#             AVG: 30%
#             Std Dev: 2
#             Frequency: over 6 years
#             Cause: further capex introduction of automation and manufacturing principles
#         """
#
#
#
#     def improved_light_efficiency(self):
#         """Improved light efficiency
#             Reduced wattage per hour of lighting systems
#             Max: 50% reduction in COGS - direct labour
#             Minimum: 10
#             AVG: 30% # 30% efficiency improvement
#             Std Dev: 3
#             Frequency: After LEDs depreciate
#             Cause: After LEDs depreciated update better lights
#         """