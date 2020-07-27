class Growthplan(object):

    def __init__(self):
        # Location
        self.upgrade_year = None

        # Assumptions
        self.facility_size_full = None
        self.percent_production_area_full = None
        self.growing_area_full = None
        self.stacked_growing_area_full = None
        self.no_lights_full = None
        self.packaging_cost_full = None
        self.other_costs_full = None
        self.stacked_growing_area_full = None


        # Calculations

        self.growing_area_full = self.facility_size_full * self.percent_production_area_full