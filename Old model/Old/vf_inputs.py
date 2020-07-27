class Scenario(object):
    
    def __init__(self):
        self.currency = None  # The type of currency
        self.country = None  # The country of the farm (no caps)
        self.capex = None  # The starting amount of money or loan
        self.repayment = None  # The loan repayment amount
        self.interest = None  # The loan interest rate
        self.lights = None   # The name of the lights
        self.crop = None  # The type of crop grown
        self.area = None  # The cultivation area of the farm
        self.surface = None  # The surface area of the farm interior
        self.volume = None  # The volume of the farm
        self.building = None  # The type of building for the farm facility
        self.system = None  # The type of vertical farming cultivation system
        self.co2 = None  # Does the farm have CO2 enrichment?
        self.energy = None  # What is the energy pricing for your local region?
        self.renewable = None  # What percentage of your energy supply is produced in-house from a renewable supply?
        self.water = None  # What is the water pricing for your local area?
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

        return """This is the represntation of a scencario with  values:
        iLights : {}
        iCrop : {}
        """.format(self.iLights, self.iCrop)

        # self.iName = "UTC"
        # self.iLocation = "Liverpool"
        # self.iLocation_type = "Urban"  # Urban, Semi-urban or rural
        # self.iFarm_type = "indoors" # Greenhouse or Indoors?
        # self.iSize = 240  # square-metres
        # self.iStaff = 0  # not sure how many staff or hours
        # self.iStart = "01/04/2019"
        # self.iType = "Indoor"
        # self.iCrop = ["Lettuce", "Basil"]
        # self.iSystem = ['ZipTowers', 21, 150]  # System type, quantity of racks, number of towers
        # self.iLights = ["Example", "water", 210, 200, 18] # Type of Light, cooling type, Qty, Wattage, Hours per day
        # self.iPlumbing =['Example', 1800, 45]  # Type of Plumbing kit, wattage, 1 system per X amount of rack units
        # self.iClimate = np.array(
        #                     [['', 'Control System', 'CO2 Injector', 'Dehumidifier', 'Inline Fans'],
        #                      ['Quantity', 0, 1, 1, 0],
        #                      ['Watts', 100, 60, 1350, 198],
        #                      ['Hours on per day', 24,16, 18, 24]]
        #                     )
        # self.iSeedling = np.array(
        #                      [['', 'Pumps', 'Lights'],
        #                       ['Quantity', 1, 9],
        #                       ['Watts', 33, 54],
        #                       ['Hours on per day', 1, 16]]
        #                     )
        #
        # self.iHVAC = np.array(
        #                  [['', 'Heating', 'Ventilation', 'AC'],
        #                   ['Watts', 0, 0, 0],
        #                   ['Hours on per day', 1, 16, 10]]
        #                  )
        #
        # self.iAnnual_rent = 23000  # outreach
        # self.iRTQ = 80
        # self.iwater_price = 3.20/1000  # United utilities £3.20 per 1000 UK litres
        # self.iwaterstandingcharge = 63.77  # United utilities £63.77 standing charge
        # self.ienergy_price = 0.125  # UK-Power 12.5p per kWH
        # self.ienergystandingcharge = 85  # £85 standing charge
        # self.itax = 0  # Council tax
        # self.iinternet = 0  # Cost of internet per month
        # self.plantindex = 4 # Plant price index is the ratio that the price of products from a VF to the average retail price from the current

