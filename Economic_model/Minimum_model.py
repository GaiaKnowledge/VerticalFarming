import numpy as np
import math
import matplotlib.pyplot as plt

YEARLY_TO_MONTHLY_31 = 11.77
DAYS_IN_MONTH = 31
DAYS_IN_YEAR = 365

# Days

days = 1825   # Days of simulation
days_timeseries =[]  #  Creation of a timeseries for days
for i in range(days+1):
    days_timeseries.append(i)

# Years

years = math.floor(days / 365)  #  Years of Simulation
years_series = []  # Creation of timeseries for years
for i in range(years + 1):
    years_series.append(i)

# User Inputs

yield_required = 9000 #Annual yield (kg)

# Capital Expenditure

def calc_capex(yield_required):
    capex = 20*yield_required
    return capex

# Cost of Goods Sold

def calc_cogs(yield_required): # seeds_cost + nutrients_cost + co2_cost + (labour_cost * 50) + packaging_cost + media_cost
    cogs_annual = yield_required*10
    return cogs_annual

def calc_cogs_time_series(days, cogs_annual):
    """
        Cost of Goods Sold Formula
        Notes
        -----
            Can adjust for days/weekly/monthly/annually in the future - ASSUMED: CONSUMABLES PURCHASED MONTHLY
    """
    cogs_time_series = []
    for i in range(days):
        if i % DAYS_IN_MONTH == 0:
            cogs_time_series.append(cogs_annual / YEARLY_TO_MONTHLY_31)
        else:
            cogs_time_series.append(0)
    return cogs_time_series

# Operational expenditure

# Utilities
def calc_utilities(yield_required):  # Energy and Water
    utilities_annual = yield_required*3
    return utilities_annual

# Labour
def calc_labour(yield_required):
    """
            Labour Costs Formaula
            Notes
            ------
                Direct farm labour cost = Number of staff working full-time x wages x 30 hours
                Generalisation if statement on farm labour required if unknown
    """

    farm_hours = yield_required*1.2
    labour_cost = farm_hours * 7 # wage
    return labour_cost

# OpEx Time series
def calc_opex_time_series(days, labour_cost, utilities):
    """
    Can adjust for days/weekly/monthly/annually in the future - ASSUMED: CONSUMABLES PURCHASED QUARTERLY
    Operations = Bill Growth Lights + Bill Environmental Control + Bill Misc Energy + Water Bill + Salary Cost + Maintenance Cost +
    Distribution cost - Reduction from Renewable Energy

    """
    opex_time_series = []
    for i in range(days):
        opex = 0
        if i % DAYS_IN_MONTH == 0:
            opex += (labour_cost / YEARLY_TO_MONTHLY_31) + (utilities / YEARLY_TO_MONTHLY_31)
        if i % DAYS_IN_YEAR == 0:
            opex += 0
        opex_time_series.append(opex)
    return opex_time_series


# Expected Yield

def calc_expected_yield(yield_required):
    expected_yield = yield_required
    return expected_yield

# Sales

def calc_sales(expected_yield):  # per year
    sales = expected_yield*10 # £10 per kilo
    return sales


def calc_revenue_time_series(days, sales):
    revenue_time_series = []
    for i in range(days):
        revenue = 0
        if i % 4 == 0:
            revenue += (sales/365)*4  # sales across 365 days of the year
        revenue_time_series.append(0)
    return revenue_time_series

# Profit
def calc_profit_time_series(opex_time_series, cogs_time_series, revenue_time_series):
    opex = np.asarray(opex_time_series)
    cogs = np.asarray(cogs_time_series)
    revenue = np.asarray(revenue_time_series)
    profit_time_series = revenue - cogs - opex
    return profit_time_series

# Loan
def calc_loan_repayment(capex, days):
    # Pay back over 5 years (no interest)
    monthly_loan_repayment = (capex/YEARLY_TO_MONTHLY_31)*5
    loan_time_series = []
    for i in range(days):
        repayment = 0
        if i % DAYS_IN_MONTH == 0:
            repayment = monthly_loan_repayment
        loan_time_series.append(repayment)
    return loan_time_series

# Tax
def calc_tax(days, profit_time_series):
    """Returns tas as saily series"""
    tax_time_series = []
    for i in range(days):
        if i % 365 == 0:
            tax_time_series.append(profit_time_series[364]*0.2)  # sales across 365 days of the year
        else:
            tax_time_series.append(0)
        tax = np.asarray(tax_time_series)
    return tax


# Post-tax profit
def calc_post_profit(profit_time_series, loan_repayments, tax):
    post_profit_time_series = profit_time_series - loan_repayments - tax
    return post_profit_time_series

# Return on Investment - Annually
def calc_roi(post_profit_time_series, capex):
    post_profit = np.cumsum(post_profit_time_series)
    profit_series = [0]

    # for i in range(days):
    #     if i % 365 == 0:
    #        profit_series.append(post_profit[days] - post_profit[days-365])  # year 2

    profit_series.append(post_profit[365]) # years 1
    profit_series.append(post_profit[730]-post_profit[365]) # year 2
    # profit_series.append(post_profit[1095] - post_profit[730])  # year 3
    # profit_series.append(post_profit[1460] - post_profit[1095])  # year 4
    # profit_series.append(post_profit[1825] - post_profit[1460])  # year 5
    profit = np.asarray(profit_series)
    roi = (profit/capex) * 100
    return roi

#Script
capex = calc_capex(yield_required)
cogs_annual = calc_cogs(yield_required)
cogs_time_series = calc_cogs_time_series(days, cogs_annual)
utilities = calc_utilities(yield_required)
labour = calc_labour(yield_required)
opex_time_series = calc_opex_time_series(days, labour, utilities)
expected_yield = calc_expected_yield(yield_required)
sales = calc_sales(expected_yield)
revenue_time_series = calc_revenue_time_series(days, sales)
profit_time_series = calc_profit_time_series(opex_time_series, cogs_time_series, revenue_time_series)
loan_time_series = calc_loan_repayment(capex, days)
tax_time_series = calc_tax(days, profit_time_series)
post_profit_time_series = calc_post_profit(profit_time_series, loan_time_series, tax_time_series)
roi = calc_roi(post_profit_time_series, capex)

#Plot

plt.plot(years_series, roi)
plt.xlabel('Years')
plt.ylabel('Annual ROI')
plt.show()