class Lights(object):
    def __init__(self, name, light_source, spectrum, PPF, input_voltage, max_power, input_power, efficiency, efficacy_spectrum, mounting_height, light_distribution, thermal_management, coverage, dimmable, dimming, life_time, dimensions, unit_weight, cable_length, warranty, led_content, certification, website, dlc):
        self.name = name
        self.light_source = light_source
        self.spectrum = spectrum
        self.PPF = PPF
        self.input_voltage = input_voltage
        self.max_power = max_power
        self.input_power = input_power
        self.efficiency = efficiency
        self.efficacy_spectrum = efficacy_spectrum
        self.mounting_height = mounting_height
        self.light_distribution = light_distribution
        self.thermal_management = thermal_management
        self.coverage = coverage
        self.dimmable = dimmable
        self.dimming = dimming
        self.life_time = life_time
        self.dimensions = dimensions
        self.unit_weight = unit_weight
        self.cable_length = cable_length
        self.led_content = led_content
        self.warranty = warranty
        self.certification = certification
        self.website = website



    def dlc_requirement(self):
        photosynthetic_photon_efficacy = '≥1.9 +5% μmol/J'
        photosynthetic_photon_efficacy2 = '≥2.1 +5% μmol/J'
        driver_lifetime = '≥50000 hours'
        fan_lifetime = '≥50000 hours'
        warranty = '≥5 years'
        power_factor1 = '≥0.9'
        power_factor2 = '≥0.10'
        total_harmonic_distortion = '≤20%'
        safety_certification = 'Appropiate horticultural lightng designation by OSHA NRTL OR SCC-recognised body'
        return

def get_lights(light_system):
    light = None
    if light_system == 'Intravision Spectra Blade Single Sided - J':
        light = Lights('Intravision Spectra Blade Single Sided - J', 'LED', 'Spectra J', 160,
               '32-37.5 (Vdc)', 120, 100, '1.6-3.4', 1.6, 0, '152 degree coverage',
               'Passive Air Cooling', 0, 0, 0, 60000, '2.39m x 112mm x 36mm', 5.5,
               '3m +-0.2m', 0, '3-year std', 0,
               'https://www.intravisiongroup.com/spectra-blades', False)
    else:
        raise RuntimeError(f"Unknown light system: {light_system}")
    return light


class System(object):
    def __init__(self, system_multiplier, dimensions, area, plant_sites, cost_per, max_trays, no_of_levels, website):
        self.system_multiplier = system_multiplier
        self.dimensions = dimensions
        self.area = area
        self.plant_sites = plant_sites
        self.cost_per = cost_per
        self.no_of_levels = no_of_levels
        self.website = website
        self.dlc = dlc

class Media(object):
    def __init__(self, type, price_per_unit):
        self.type = type
        self.price_per_unit = price_per_unit
# Media
Hemp = Media('Hemp', 0.05)
Jute = Media('Jute', 0.05)
Peat = Media('Peat', 0.05)

# Lights
#RAZR3 = Lights('Fluence RAZR3 PhysioSpec LED, W+R', 'LED', 'White, Red', 200, 0, 160, 0, 0, 2.2, 0, 0, 0, 0, 50000, 0, 0, 0, 0, 0, 0, 'https://fluence.science/products/razr-series/', 'No')
SPYDR2x = Lights('Fluence SPYDR2x 40", W+R (6-fixture array)', 'LED', 'White, Red',	852,	0,	160,	0,	2.4,	0,	0,	0,	0,	0,	0,	0,	50000,	0,	0,	0,	0,	5,	0,	'https://fluence.science/products/spydr-series/', 'No')
SPYDR2i = Lights('Fluence SPYDR2i 40", W+R (6-fixture array)', 'LED'	'White, Red',	1593,	0,	160,	0,	2.5,	0,	0,	0,	0,	0,	0,	0,	50000,	0,	0,	0,	0,	6,	0, 0,	'https://fluence.science/products/spydr-series/', 'No')
#Folio_Novia = Lights('Folio Novia', LED	FOLIO - early to vegetative	320	Autosensing 100-277 VAC	0	320W	2.4	0	15cm above canopy	Passive/Active	2m x 1m		Yes	1-10V	50000	0	0	0	None	5-year limited	C.E. RoHS compliant	www.liberty-produce.com	NO)
#Ariza_Lynk_GEHL48HPKB1 = Lights('GE Current Ariza Lynk GEHL48HPKB1, R+W', LED	White, Red	81	0	160	0	2.5	0	0	0	0	0	0	0	50000	0	0	0	0	0	0	https://products.gecurrent.com/eu/horticulture-led-grow-lights?src=homepage-tile-eu	NO)
#Ariza Lynk GEHL48HPKB1, R+W = Lights('GE Current Ariza Lynk GEHL48HPKB1, R+W', LED	Red, Blue	91	0	160	0	2.8	0	0	0	0	0	0	0	50000	0	0	0	0	0	0	https://products.gecurrent.com/eu/horticulture-led-grow-lights?src=homepage-tile-eu	NO)
#Illumitex = Lights('Illumitex', 			0	0	0	0	0	0	0	0	0	0	0	0	50000	0	0	0	0	0	0	https://illumitex.com/	)
Spectra_Blade_Single_Sided_B = Lights('Intravision Spectra Blade Single Sided - B', 'LED',	'Spectra B',	250,	'32-37.5 (Vdc)', 120,	100,	'1.6-3.2',	2.5,	0,	'150 degree coverage',	'Passive Air Cooling',	0,	0,	0,	60000,	'2.39m x 112mm x 36mm',	3.5,    '3m +-0.2m', 0,		'3-year std',   0,	'https://www.intravisiongroup.com/spectra-blades', 'No')
Spectra_Blade_Single_Sided_G = Lights('Intravision Spectra Blade Single Sided - G', 'LED',	'Spectra G',	220,	'32-37.5 (Vdc)', 120,	100,	'1.6-3.3',	2.2,	0,	'151 degree coverage',	'Passive Air Cooling',	0,	0,	0,	60000,	'2.39m x 112mm x 36mm',	4.5,	'3m +-0.2m', 0,		'3-year std',	0,	'https://www.intravisiongroup.com/spectra-blades', 'No')
Spectra_Blade_Single_Sided_J = Lights('Intravision Spectra Blade Single Sided - J', 'LED',	'Spectra J',	160,	'32-37.5 (Vdc)', 120,	100,	'1.6-3.4',	1.6,	0,	'152 degree coverage',	'Passive Air Cooling',	0,	0,	0,	60000,	'2.39m x 112mm x 36mm',	5.5,	'3m +-0.2m', 0,		'3-year std',	0,	'https://www.intravisiongroup.com/spectra-blades', 'No')
Spectra_Blade_Double_Sided_B = Lights('Intravision Spectra Blade Double Sided - B', 'LED',	'Spectra B',	375,	'64-75 (Vdc)', 160,	150,	'1.6-3.2',	2.5,	0,	'300 degree coverage',	'Passive Air Cooling',	0,	0,	0,	60000,	'2.39m x 112mm x 36mm',	5.3,	'3m +-0.2m', 0,		'3-year stf',	0,	'https://www.intravisiongroup.com/spectra-blades', 'No')
Spectra_Blade_Double_Sided_G = Lights('Intravision Spectra Blade Double Sided - G', 'LED',	'Spectra G',	330,	'64-75 (Vdc)', 160,	150,	'1.6-3.3',	2.2,	0,	'301 degree coverage',	'Passive Air Cooling',	0,	0,	0,	60000,	'2.39m x 112mm x 36mm',	6.3,	'3m +-0.2m', 0,		'3-year stf',	0,	'https://www.intravisiongroup.com/spectra-blades', 'No')
Spectra_Blade_Double_Sided_J = Lights('Intravision Spectra Blade Double Sided - J', 'LED',	'Spectra J',	240,	'64-75 (Vdc)', 160,	150,	'1.6-3.4',	1.6,	0,	'302 degree coverage',	'Passive Air Cooling',	0,	0,	0,	60000,	'2.39m x 112mm x 36mm',	7.3,	'3m +-0.2m', 0,		'3-year stf',	0,	'https://www.intravisiongroup.com/spectra-blades', 'No')
#Barlight_hybrid_spec_8_fixture = Lights('Lumigrow Barlight, hybrid spec. W+R+B (8-fixture array)', LED	White, Red Blue,	1712	0	160	0	2.5	0	0	0	0	0	0	0	50000	0	0	0	0	0	0	https://www.lumigrow.com/	NO)
#PhotonMAX_Horticulture_LED_LI200UBPBX = Lights('MaxiLite PhotonMAX Horticulture LED LI200UBPBX, W+B+R', LED	White, Red Blue,	491	0	160	0	2.4	0	0	0	0	0	0	0	50000	0	0	0	0	5 years	0	https://www.maxlite.com/products/led-solutions/list/	YES)
#PhotonMAX_Horticulture_LED_LI200UFSRX = Lights('MaxiLite PhotonMAX Horticulture LED LI200UFSRX, R+W', LED	Red, White	533	0	160	0	2.7	0	0	0	0	0	0	0	50000	0	0	0	0	5 years	0	https://www.maxlite.com/products/led-solutions/list/	YES)
#GreenPower_LED_Production_Module = Lights('Philips GreenPower LED Production Module 3.0, R+Blow', LED	Red, Low Blue	210	0	160	0	3	0	0	0	0	0	0	0	50000	0	0	0	0	0	0	https://www.lighting.philips.co.uk/products/horticulture/products/greenpower-led-production-module	NO)
#GreenPower_LED_Production_Module = Lights('Philips GreenPower LED Production Module 3.0, R+Blow+FR', LED	Red, Low Blue, FR	210	0	160	0	3	0	0	0	0	0	0	0	50000	0	0	0	0	0	0	https://www.lighting.philips.co.uk/products/horticulture/products/greenpower-led-production-module	NO)
#GreenPower_LED_Production_Module = Lights('Philips GreenPower LED Production Module 3.0, R+Bhigh', LED	Red, High Blue	210	0	160	0	2.8	0	0	0	0	0	0	0	50000	0	0	0	0	0	0	https://www.lighting.philips.co.uk/products/horticulture/products/greenpower-led-production-module	NO)
#GreenPower_LED_Production_Module = Lights('Philips GreenPower LED Production Module 3.0, R+Wlow', LED	Red, Low White	210	0	160	0	2.7	0	0	0	0	0	0	0	50000	0	0	0	0	0	0	https://www.lighting.philips.co.uk/products/horticulture/products/greenpower-led-production-module	NO)
