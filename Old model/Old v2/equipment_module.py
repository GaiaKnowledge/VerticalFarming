# GROW SYSTEM CLASS #

from Economic_model.scenario_module import Scenario


class GrowSystem(object):
    def __init__(self, towers_per_rack, grow_system_area, no_of_lights_req, no_of_plumbing_kit):
        self.towers_per_rack = towers_per_rack
        self.grow_system_area = grow_system_area
        self.no_of_lights_req = no_of_lights_req
        self.no_of_plumbing_kit = no_of_plumbing_kit

    def calc_maintenance_cost(grow_system, no_of_racks):
        if grow_system == 'ziprack_8':
            maintenance_cost_per_month = no_of_racks * 2.50  # £2.50 worth of labour per month to maintain
            return maintenance_cost_per_month
        else:
            raise RuntimeError("Unknown grow_system: {}".format(grow_system))

# LIGHT SYSTEM CLASS #

class LightSystem():
    def __init__(self, light_name, light_wattage, light_efficiency):
        self.light_name = light_name
        self.light_wattage = light_wattage
        self.light_efficiency = light_efficiency

    def calc_no_of_lights(self, no_of_racks, no_of_lights_req): # Assumption that 24 lighting units are require to cover crop area of 1 Ziprack (30 towers)
        return (no_of_racks * no_of_lights_req)

    def calc_lights_energy(self, no_of_lights, crop_light_time):
        lighting_kw_usage = self.light_wattage * no_of_lights / 1000
        return lighting_kw_usage * crop_light_time

# FARM CALCULATIONS CLASS #


class Calculations(Scenario, GrowSystem):
    def __init__(self, crop, grow_system):
        super().__init__()
        self.crop = crop
        self.grow_system = grow_system

    def calc_no_of_racks(self):
        return math.floor(self.area / self.grow_system_area)  # 54 Zipracks per 250 sq-m (including aisles, work bench & plumbing kit)

    def calc_plant_capacity(self, no_of_racks): # Excluding propagation and only within the VFS
        no_of_towers = no_of_racks * self.grow_system.towers_per_rack  # Tight spacing with lettuce (30 towers per rack)
        yield_capacity = no_of_towers * self.crop.kg_per_tower  # 3.3kg of greens per tower
        farm_plant_capacity = yield_capacity / self.crop.harvest_weight  # Potential yield divided by harvest weight of product
        return (farm_plant_capacity, yield_capacity)

# EQUIPMENT CLASS #

class PumpCalculations(GrowSystem):  # Look at inheritance
    def __init__(self):
        super().__init__()

    def calc_no_of_plumbing_kits(self, no_of_racks):
        return (math.ceil(no_of_racks / self.no_of_plumbing_kit))

