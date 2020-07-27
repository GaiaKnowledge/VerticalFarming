# CROP CULTIVAR CLASS #


class Crop():
    def __init__(self,crop, time_to_harvest, kilos_tower, harvest_weight, gross_yield, kg_per_tower, light_time, seed_cost, temp_req): # Time to harvest in days, harvest weight at end of cycle
        self.name = crop
        self.time_to_harvest = time_to_harvest # Time to harvest in days for greenhouse
        self.kilo_tower = kilos_tower # kilos harvested per zip tower
        self.harvest_weight = harvest_weight # typical weight per crop for harvest
        self.gross_yield = gross_yield
        self.kg_per_tower = kg_per_tower
        self.light_time = light_time
        self.seed_cost = seed_cost
        self.temp_req = temp_req  # degrees celsius
        self.ppfd_req = ppfd_req # lighting intensity req