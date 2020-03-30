

class SalesCalculations(Scenario, GrowSystem):
    def __init__(self):
        super().__init__()

    def calc_sales(ya, crop_price, sale_cycle):
        crop_sales = (ya*crop_price)/ sale_cycle
        return crop_sales  # per sales or delivery cycle

    # ---------------------------------------- OPEX: DISTRIBUTION COST ----------------------------------------------------#

    def calc_distribution_cost(sales, sale_cycle):  # Distribution cost per delivery
        distribution_cost_per_sale_cycle = sales * 0.15
        distribution_cost_per_month = distribution_cost_per_sale_cycle * (
                    30.417 / sale_cycle)  # The number of delivery (sale) cycles in a month
        return distribution_cost_per_month