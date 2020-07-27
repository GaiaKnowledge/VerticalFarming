# INPUT SCENARIO CLASS #

class Scenario(object):

    def __init__(self):
        self.currency = None  # The type of currency
        self.country = None  # The country of the farm (no caps)
        self.capex = None  # The starting amount of money or loan
        self.repayment = None  # The loan repayment amount
        self.interest = None  # The loan interest rate
        self.lights = None  # The name of the lights
        self.crop = None  # The type of crop grown
        self.area = None  # The cultivation area of the farm
        self.surface = None  # The surface area of the farm interior
        self.volume = None  # The volume of the farm
        self.building = None  # The type of building for the farm facility
        self.system = None  # The type of vertical farming cultivation system
        self.co2 = None  # Does the farm have CO2 enrichment?
        self.energy = None  # What is the energy pricing for your local region?
        self.energy_standing = None
        self.renewable = None  # What percentage of your energy supply is produced in-house from a renewable supply?
        self.water = None  # What is the water pricing for your local area?
        self.water_standing = None
        self.toutdoors = None  # Average outdoor temperature
        self.crop_price = None  # Crop price per kilo
        self.farm_staff = None  # The number of staff working on the farm
        self.salaries = None  # The annual salaries of permanent employees (Management and founders)
        self.standard_wage = None  # The £/h wages for farm hands.
        self.insurance = None  # The cost of insurance premium
        self.coverage = None  # The level of coverage from insurance ( high, med or low)
        self.days = None  # The number of days you would like to run your simulation

    def __str__(self):
        """String representation"""

        return """This is the representation of a scenario with  values:
        lights : {}
        crop : {}
        """.format(self.lights, self.crop)

    def getScenario(self, input_file):
        import json

        with open(input_file) as f:
            inputs = json.load(f)
        self.currency = inputs['currency']
        self.country = inputs['country']
        self.capex = inputs["start_loan"]
        self.repayment = inputs["loan_repayment"]
        self.interest = inputs['loan_interest']
        self.lights = inputs['lights']
        self.crop = inputs['crop']
        self.area = inputs['grow_area']
        self.surface = inputs['surface_area']
        self.volume = inputs['farm_volume']
        self.building = inputs['building_type']
        self.rent = inputs['rental_costs']
        self.system = inputs['grow_system']
        self.co2 = inputs['co2_enrichment']
        self.energy = inputs['energy_price']
        self.energy_standing = inputs['energy_standing_charge']
        self.water = inputs['water_price']
        self.water_standing = inputs['water_standing_charge']
        self.renewable = inputs['ratio_of_renewable_energy_created_to_sourced']
        self.toutdoors = inputs['average_outdoor_temperature']
        self.crop_price = inputs['crop_price_per_kilo']
        self.farm_staff = inputs['number_of_farm_staff']
        self.salaries = inputs['annual_salaries_of_employees']
        self.standard_wage = inputs['standard_wage']
        self.insurance = inputs['insurance_premium']
        self.coverage = inputs['insurance_coverage']
        self.days = inputs['days_for_simulation']
