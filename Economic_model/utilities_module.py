# UTILITIES

# WATER CONSUMPTION CLASS
from Economic_model.scenario_module import Scenario
from Economic_model.equipment_module import LightSystem


class WaterCalculations(Scenario):
    def __init__(self):
        super().__init__()

    def water_consumption(self, no_of_racks):
        water_consumption = no_of_racks * 0.95 * 30.42 # Litres of water per tower per day (0.25 gallons) multiplied by month
        water_buffer = 1900 # Litres of water for buffer per month (500 gallons)
        water_consumption += water_buffer  # Water consumption could be used here.
        return water_consumption

    def water_cost(self, consump_per_month):
        return (consump_per_month / 1000) * self.water + self.water_standing

    # water_cost_per_day = (water_consumption_per_day / 1000) * water_price
    # water_cost_per_week = (water_consumption_per_week / 1000) * water_price
    # water_cost_per_month = (water_consumption_per_month / 1000) * water_price + water_standing_charge
    # water_cost_per_year = (water_consumption_per_year / 1000) * water_price
    # return water_cost_per_day, water_cost_per_week, water_cost_per_month, water_cost_per_year

    # else:
    #     water_consumption_per_year = grow_area * 200  # Average from Agrilyst survey - 4 Gallons per sq ft per year
    #     water_consumption_per_month = water_consumption_per_year / 12  # consumption per month
    #     water_consumption_per_week = water_consumption_per_year/52
    #     water_consumption_per_day = water_consumption_per_year/365
    #     return water_consumption_per_day, water_consumption_per_week, water_consumption_per_month, water_consumption_per_year


# ENERGY CONSUMPTION CLASS #
class EnergyCalculations(Scenario, LightSystem):
    def __init__(self):
        super().__init__

    def calc_lights_energy(lights, no_of_lights):
        lights_watts, efficiency = get_spec(lights)
        lighting_kw_usage = lights_watts * no_of_lights / 1000
        lights_kwh_per_day = lighting_kw_usage * 12  # Assuming 12 hours of light for plants
        lights_kwh_per_month = lights_kwh_per_day * 30.417  # 365 days/12 months
        lights_kwh_per_week = lights_kwh_per_day * 7
        lights_kwh_per_year = lights_kwh_per_day * 365
        return lights_kwh_per_day, lights_kwh_per_week, lights_kwh_per_month, lights_kwh_per_year

    def calc_hvac_energy(surface_area, building_type, Tin, Tout):
        """
            Heat Transfer Equation
            Notes
                -----
                    Q = U x SA x (Tin - Tout)
                    Q - ﻿Heat lost or gained due to outside temperature (kJ·h−1)
                    U - Overall heat transfer coefficient (kJ·h−1·m−2·°C−1)
                    SA - Surface Area of the space
                    Tin - ﻿Inside air set point temperature (°C)
                    Tout - ﻿Outside air temperature (°C)
        """

        if building_type == 'basement':
            U = 0.5
        else:
            U = 24  # generic heat transfer coefficient
        Q = U * surface_area * (Tin - Tout)
        hvac_kwh = Q * 0.00666667 * 24  # Conversion factor of kJ/h to kWh x 24 hours

        # Rudimentary hvac calculations - general
        hvac_kwh_per_day = hvac_kwh * 1
        hvac_kwh_per_month = hvac_kwh_per_day * 30.417  # 365 days/12 months
        hvac_kwh_per_week = hvac_kwh_per_day * 7
        hvac_kwh_per_year = hvac_kwh_per_day * 365
        return hvac_kwh_per_day, hvac_kwh_per_week, hvac_kwh_per_month, hvac_kwh_per_year

    def calc_pump_energy(grow_system, no_of_racks):
        if grow_system == 'ziprack_8':
            no_of_plumbing_kits = math.ceil(no_of_racks / 45)  # spec for plumbing kit provided by Refarmers - 45 racks
            plumbing_kit_wattage = 1800  # spec for plumbing kit provided by Refarmers
            pumps_kw_usage = no_of_plumbing_kits * plumbing_kit_wattage / 1000
            pumps_kwh_per_day = pumps_kw_usage * 24  # 24 hours on
            pumps_kwh_per_month = pumps_kwh_per_day * 30.417  # 365 days/12 months
            pumps_kwh_per_week = pumps_kwh_per_day * 7
            pumps_kwh_per_year = pumps_kwh_per_day * 365
            return pumps_kwh_per_day, pumps_kwh_per_week, pumps_kwh_per_month, pumps_kwh_per_year
        else:
            raise RuntimeError("Unknown grow_system: {}".format(grow_system))

    def calc_misc_energy(pumps_kwh_per_day):
        """
            Misc Energy Consumption
            Notes
            ------
                Energy consumption for miscellaneous elements such as: Filtration, Sensors, Internet, Office Lighting,
                Automation, Computers, etc.
        """
        misc_kwh_per_day = pumps_kwh_per_day
        return misc_kwh_per_day

    # ----------------------------------- OPEX: OVERALL ENERGY CALC (LIGHTS+HVAC+MISC) -----------------------#

    def calc_energy_consumption(hvac_kwh_per_day, lights_kwh_per_day, misc_kwh_per_day):
        """
            Energy Consumption
            Notes
            ------
                Energy consumption for different time periods
        """
        farm_kwh_per_day = hvac_kwh_per_day + lights_kwh_per_day + misc_kwh_per_day
        farm_kwh_per_week = farm_kwh_per_day * 7  # 7 days in a week
        farm_kwh_per_month = farm_kwh_per_day * 30.417  # 365 days/12 months
        farm_kwh_per_year = farm_kwh_per_day * 365
        return farm_kwh_per_day, farm_kwh_per_week, farm_kwh_per_month, farm_kwh_per_year

    def calc_energy_cost(farm_kwh_per_day, farm_kwh_per_week, farm_kwh_per_month, farm_kwh_per_year, energy_price):
        """
            Energy Costs
            Notes
            ------
                Energy cost for different time periods
        """
        energy_cost_per_day = farm_kwh_per_day * energy_price
        energy_cost_per_week = farm_kwh_per_week * energy_price  # 365 days/12 months
        energy_cost_per_month = farm_kwh_per_month * energy_price  # 365 days/12 months
        energy_cost_per_year = farm_kwh_per_year * energy_price
        return energy_cost_per_day, energy_cost_per_week, energy_cost_per_month, energy_cost_per_year

    # ---------------------------------- OPEX: RENEWABLE ENERGY REDUCTION ------------------------------------------------#

    def calc_renewable_energy_reduction(renewable, energy_cost_per_day):  # Distribution cost per delivery
        renewable_energy_reduction_per_day = energy_cost_per_day * renewable
        renewable_energy_reduction_per_week = energy_cost_per_day * 7 * renewable
        renewable_energy_reduction_per_month = energy_cost_per_day * 30.417 * renewable
        renewable_energy_reduction_per_year = energy_cost_per_day * 365 * renewable
        return renewable_energy_reduction_per_day, renewable_energy_reduction_per_week, renewable_energy_reduction_per_month, renewable_energy_reduction_per_year

    # ---------------------------------------------- OPEX: OVERALL OPEX --------------------------------------------------#


# OPERATIONS COST #
