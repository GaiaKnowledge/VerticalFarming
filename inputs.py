
class Scenario(object):
    """Scenario Class holds objects of a farm scenario which is the basis for model computations
        """
    def __init__(self):
        # Location
        self.currency = None  # The type of currency
        self.country = None  # The country of the farm (no caps)
        self.start_date = None # day/month/year

        # Assumptions
        self.facility_size_pilot = None
        self.percent_production_area_pilot = None
        self.growing_area_pilot = None
        self.growing_levels_pilot = None
        self.stacked_growing_area_pilot = None
        self.weight_unit = None
        self.growing_area_mulitplier = None
        self.no_lights_pilot = None
        self.packaging_cost_pilot = None
        self.packaging_cost_full = None
        self.other_costs_pilot = None

        # Characteristics
        self.farm_type = None
        self.business_model = None
        self.grower_exp = None
        self.automation_level = None
        self.climate_control = None
        self.lighting_control = None
        self.nutrient_control = None
        self.system_type = None
        self.system_quantity = None
        self.light_system = None
        self.growing_media = None
        self.ceiling_height = None
        self.insultation_level = None
        self.roof_type = None
        self.co2_enrichment = None
        self.structure_type = None
        self.water_price = None
        self.electricity_price = None
        self.labour_improvement = None
        self.percentage_renewable_energy = None
        self.biosecurity_level = None

        # Company Info
        self.loan_amount = None
        self.tax_rate = None
        self.loan_interest = None
        self.loan_tenure = None
        self.loan_type = None

        # Crop and System Selection 1
        self.crop_typ1 = None
        self.crop1_percent = None
        self.crop1_system = None
        self.crop1_harvest_weight = None
        self.crop1_product_weight = None
        self.crop1_customer_percent = None
        self.crop1_price1 = None
        self.crop1_price2 = None

        # Crop and System Selection 2

        self.crop_typ2 = None
        self.crop2_percent = None
        self.crop2_system = None
        self.crop2_harvest_weight = None
        self.crop2_product_weight = None
        self.crop2_customer_percent = None
        self.crop2_price1 = None
        self.crop2_price2 = None

        # Crop and System Selection 3

        self.crop_typ3 = None
        self.crop3_percent = None
        self.crop3_system = None
        self.crop3_harvest_weight = None
        self.crop3_product_weight = None
        self.crop3_customer_percent = None
        self.crop3_price1 = None
        self.crop3_price2 = None

        # Crop and System Selection 4
        self.crop_typ4 = None
        self.crop4_percent = None
        self.crop4_system = None
        self.crop4_harvest_weight = None
        self.crop4_product_weight = None
        self.crop4_customer_percent = None
        self.crop4_price1 = None
        self.crop4_price2 = None

# Growth Multiplier
        self.vadded_products_multiplier = None
        self.education_multiplier = None
        self.tourism_multiplier = None
        self.hospitality_multiplier = None

# Estimated Revenue
        self.vadded_avg_revenue_y1 = None
        self.education_avg_revenue_y1 = None
        self.tourism_avg_revenue_y1 = None
        self.hospitality_avg_revenue_y1 = None

# Estimated OpEx
        self.monthly_rent_y1 = None
        self.monthly_distribution_y1 = None
        self.monthly_rent_y2 = None
        self.monthly_distribution_y2 = None

# Staff
        self.delivery_msalary = None
        self.farmhand_msalary = None
        self.parttime_wage = None

        self.ceo_msalary = None
        self.hgrower_msalary = None
        self.marketer_msalary = None
        self.scientist_msalary = None
        self.salesperson_msalary = None
        self.manager_msalary = None
        self.admin_msalary = None

# Staff Headcount - Pilot
        self.ceo_count_y1 = None
        self.hgrower_count_y1 = None
        self.marketer_count_y1 = None
        self.scientist_count_y1 = None
        self.salesperson_count_y1 = None
        self.manager_count_y1 = None
        self.delivery_count_y1 = None
        self.farmhand_count_y1 = None
        self.admin_count_y1 = None
        self.parttime_count_y1 = None

# Staff Headcount - Full-Scale
        self.ceo_count_y2 = None
        self.hgrower_count_y2 = None
        self.marketer_count_y2 = None
        self.scientist_count_y2 = None
        self.salesperson_count_y2 = None
        self.manager_count_y2 = None
        self.delivery_count_y2 = None
        self.farmhand_count_y2 = None
        self.admin_count_y2 = None
        self.parttime_count_y2 = None

        self.insurance_pilot = None
        self.insurance_full = None

        self.capex_pilot = None
        self.capex_full = None
        self.capex_lights = None
        self.capex_facilities = None
        self.capex_building = None

        self.target_productivity_space = None
        self.target_productivity_energy = None
        self.target_productivity_labour = None
        self.target_productivity_water = None
        self.target_productivity_nutrients = None
        self.target_productivity_volume = None
        self.target_productivity_plants = None
        self.target_productivity_labour = None
        self.target_productivity_CO2_emit = None
        self.target_productivity_CO2_miti = None
        self.target_productivity_CO2_net = None


    def __str__(self):
        """String representation"""

        return """This is the represntation of a scencario with  values:
        iLights : {}
        iCrop : {}
        """.format(self.iLights, self.iCrop)

class Growthplan(object):

    def __init__(self):
        # Location
        self.upgrade_year = None

        # Assumptions
        self.facility_size_full = None
        self.percent_production_area_full = None
        self.growing_area_full = None
        self.growing_levels_full = None
        self.no_lights_full = None
        self.packaging_cost_full = None
        self.other_costs_full = None
        self.growing_area_full = None
        self.stacked_growing_area_full = None


class Staff(object):
    """Staff Class holds objects as members of staff that have their corresponding attributes

        Args:
            job_role (str): The job title
            name (str): The name of the employee
            salary (int): The annual salary
            count_pilot (float): The number of this type of job role on the pilot farm
            count_pilot (float): The number of this type of job role on the full-scale farm
            category (str) = category of work
            wage (float) = hourly wage if applicable
            hours (float) = expected hours of work
            cost_pilot (float)= cost of this job role on the pilot farm
            cost_full (float) = cost of this job role on the full-scale farm
        """

    def __init__(self, name, job_role, salary, count_pilot, count_full, category, wage, hours):

        # Role
        self.job_role = job_role
        self.name = name
        self.salary = salary
        self.count_pilot = count_pilot
        self.count_full = count_full
        self.category = category
        self.wage = wage
        self.hours = hours
        self.cost_pilot = salary * count_pilot
        self.cost_full = salary * count_full