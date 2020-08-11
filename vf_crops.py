from dataclasses import dataclass

class Crops(object):
    def __init__(self, plant, ppfd, par, photoperiod, harvest_cycle, dry_mass, dm_fm, nft, drip,
                 aeroponic, ebb_flow, dwc, bucket, slab, soil, water_dm, fm_kg, water_use,
                 spacing, height, root_depth, light_use, harvest_index, seed_cost, germination_rate, category):
        self.plant = plant
        self.ppfd_req = ppfd
        self.par_req = par
        self.photoperiod = photoperiod
        self.harvest_cycle = harvest_cycle
        self.dry_mass = dry_mass
        self.dm_fm = dm_fm
        self.nft= nft # Max annual yield kg/m2/year
        self.drip_tower = drip # Max annual yield kg/m2/year
        self.aeroponic = aeroponic # Max annual yield kg/m2/year
        self.ebb_flow = ebb_flow # Max annual yield kg/m2/year
        self.dwc = dwc # Max annual yield kg/m2/year
        self.bucket = bucket # Max annual yield kg/m2/year
        self.slab = slab # Max annual yield kg/m2/year
        self.soil = soil # Max annual yield kg/m2/year
        self.water_dm = water_dm
        self.fm_per_kg = fm_kg
        self.water_use = water_use
        self.spacing = spacing
        self.height_of_shoot = height
        self.root_depth = root_depth
        self.light_use_efficiency = light_use
        self.harvest_index = harvest_index
        self.seed_cost = seed_cost
        self.germination_rate = germination_rate
        self.category = category

    def get_crops(self):
        # Crop Catalogue
        # amaranth = Crops('Amaranth	0	0	16	30	0	0	5.613483085		5.831416169	5.450147015	5.450147015	-	-	2.72484602	0	0	0	0	0	0	0	0	0
        # arugula = Crops('Arugula', 'n/a', 'n/a', 16, 'n/a', 0, 5.6134831, 0, 5.8314162, 5.450147, 5.450147, 0, 0, 2.724846, 'n/a', 'n/a', 'n/a', 'n/a','n/a','n/a','n/a','n/a','n/a','n/a', 'leafy green')
        # basil_dwarf = Crops('Basil - Dwarf	0	0	14	42	0	0	-	7.039285714	-	-	-	-	-	-	0	0	0	0	0	0	0	0	0
        basil_lemon = Crops('Basil - Lemon', 'n/a',	'n/a',	14,	42,	'n/a', 'n/a', 'n/a', 13.067,	'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'herbs')
        # basil_thai = Crops('basil - Thai	0	0	14	42	0	0	20.3055398		21.09401169	19.71407214	19.71407214	-	-	9.85703607	0	0	0	0	0	0	0	0	0
        # basil_sweet = Crops('basil - Sweet	0	0	14	42	0	0	-	5.495857143	-	-	-	-	-	-	0	0	0	0	0	0	0	0	0
        basil_genovese = Crops('Basil - Genovese',	0,	0,	14,	42,	0,	0,	34.33833756,	9.802857143,	35.67186965,	33.33830224,	33.33830224, 0,	0,	16.66892363,	0,	0,	0,	0,	0,	0,	0,	0,	0, 'herbs')
        # bok_choy = Crops('bok-Choy	295	17	16	49	0.03	0.08	46.91385	17.53042857	48.7355704	45.5475597	45.5475597	-	-	22.77377985	402	0.4	2173	0.2	0.3	0.1	0.0109	0.67	67.6
        # broccoli = Crops('broccoli	250	10.8	12	64	0.085	0.09	-	-	5.10254602	4.769049254	4.769049254	4.769049254	4.769049254	2.384524627	198	0.9	458	0.5	0.5	0.4	0.0065	0.33	25.7
        # cabbage = Crops('cabbage	0	0	16	30	0	0	-	-	7.952055224	7.432018657	7.432018657	7.432018657	7.432018657	3.715781841	0	0	0	0	0	0	0	0	0
        # cai_xin = Crops('cai iin	0	0	16	30	0	0	84.20452114		87.47442736	81.75175025	81.75175025	-	-	40.87587512	0	0	0	0	0	0	0	0	0
        # carrot = Crops('carrot	0	0	16	30	0	0	-	-	19.45291642	18.180351	-	4.087496517	-	9.08994801	0	0	0	0	0	0	0	0	0
        # cauliflower = Crops('cauliflower	0	0	16	30	0	0	-	-	4.373675871	4.087496517	4.087496517	4.087496517	4.087496517	2.043748259	0	0	0	0	0	0	0	0	0
        # chard_swiss = Crops('chard Swiss	0	0	16	30	0	0	29.32041692		30.45967463	28.46733856	28.46733856	-	-	14.23344179	0	0	0	0	0	0	0	0	0
        # chives = Crops('chives	0	0	16	30	0	0	5.655795771		5.875548756	5.491094776	5.491094776	-	-	2.7453199	0	0	0	0	0	0	0	0	0
        # chinese_leaf = Crops('chinese Leaf	295	17	12	85	0.084	0.07	-	-	-	-	-	-	-	-	480	1.2	2681	0.3	0.3	0.1	0.0129	0.8	79.8
        # choy_sum = Crops('choy Sum	0	0	16	30	0	0	30.93239378		32.13352811	30.03108806	30.03108806	-	-	15.01554403	0	0	0	0	0	0	0	0	0
        # cilantro = Crops('cilantro	0	0	16	30	0	0	29.12068284	20.81542857	30.251751	28.2726092	28.2726092	-	-	14.13607711	0	0	0	0	0	0	0	0	0
        # cucumber = Crops('cucumber	250	16.2	18	58	0.331	0.045	-	-	-	-	-	17.31453333	17.31453333	8.657266667	172	7.4	618	0.8	1.5	0.3	0.0136	0.2	80.4
        # dill = Crops('dill	0	0	16	30	0	0	3.708957214		3.853184328	3.601128109	3.601128109	-	-	1.800336567	0	0	0	0	0	0	0	0	0
        # eggplant = Crops('eggplant	250	10.8	12	81	0.108	0.08	-	-	-	-	-	-	-	-	198	1.3	459	0.5	0.6	0.1	0.0073	0.33	29
        # escarole = Crops('escarole	0	0	16	30	0	0	157.8836478	-	164.0148925	153.2852142	153.2852142	-	-	76.6423796	0	0	0	0	0	0	0	0	0
        # fennel = Crops('fennel	0	0	16	30	0	0	13.35260995	-	13.87082662	12.96360622	12.96360622	-	-	6.481575622	0	0	0	0	0	0	0	0	0
        # gai_choi = Crops('gai Choi	0	0	16	30	0	0	14.43499577	-	14.99552512	14.01459876	14.01459876	-	-	7.007071891	0	0	0	0	0	0	0	0	0
        # gailan = Crops('gailan	0	0	16	30	0	0	5.638506716	-	5.857804726	5.474260697	5.474260697	-	-	2.737130348	0	0	0	0	0	0	0	0	0
        # kale = Crops('kale	0	0	16	30	0	0	15.2848893	-	15.87863184	14.83992363	14.83992363	-	-	7.419734328	0	0	0	0	0	0	0	0	0
        # leeks = Crops('Leeks	0	0	16	30	0	0	22.86886965	-	23.75698109	22.20278607	-	-	-	11.10139303	0	0	0	0	0	0	0	0	0
        lettuce_fu_mix = Crops('Lettuce (Farm Urban Mix)',	0,	0,	16,	35,	0,	0,	0,	33,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 'leafy greens')
        # lettuce_heads = Crops('lettuce - heads	0	0	16	35	0	0	30.42282164	23.47	31.60393706	29.5365301	29.5365301	-	-	14.76849254	0	0	0	0	0	0	0	0	0
        # lettuce_butterhead = Crops('lettuce (butterhead)	295	17	16	30	0.007	0.048	-	14.2058	-	-	-	-	-	-	402	0.1	1515	0.2	0.2	0.2	0.0127	0.67	78.5
        # lettuce_iceberg = Crops('lettuce (iceberg)	250	14.4	16	73	0.018	0.04	-	-	-	-	-	-	-	-	402	0.5	565	0.3	0.2	0.2	0.0108	0.67	56.6
        # lettuce_little_gem = Crops('lettuce (little-gem)	0	0	16	35	0	0	-	13.1546	-	-	-	-	-	-	0	0	0	0	0	0	0	0	0
        # lettuce_loose_leaf = Crops('lettuce (loose leaf)	0	0	16	35	0	0	-	12.775	-	-	-	-	-	-	0	0	0	0	0	0	0	0	0
        # lettuce_romaine = Crops('lettuce Romaine	0	0	16	35	0	0	21.29602065	-	22.12316542	20.67588955	20.67588955	-	-	10.33794478	0	0	0	0	0	0	0	0	0
        # mesclun = Crops('mesclun	0	0	16	30	0	0	37.42397886	-	38.87762438	36.33431343	36.33431343	-	-	18.16715672	0	0	0	0	0	0	0	0	0
        # mg_arugula = Crops('microgreens - Arugula	0	0	16	30	0	0	49.81022164	-	51.74477587	48.35976095	48.35976095	-	-	24.17965299	0	0	0	0	0	0	0	0	0
        # mg_broccoli = Crops('microgreens - Broccoli	0	0	16	30	0	0	25.47132736	-	26.46044328	24.72926294	24.72926294	-	-	12.36485896	0	0	0	0	0	0	0	0	0
        # mg_bbb = Crops('microgreens - Bull's Blood Beet	0	0	16	30	0	0	16.98103657	-	17.64029552	16.48602363	16.48602363	-	-	8.243239303	0	0	0	0	0	0	0	0	0
        # mg_buttercrunch_lettuce = Crops('microgreens - Buttercrunch Lettuce	0	0	16	30	0	0	29.11021841	-	30.24037662	28.26214478	28.26214478	-	-	14.13107239	0	0	0	0	0	0	0	0	0
        # mg_carrot = Crops('microgreens - Carrot	0	0	16	30	0	0	13.58464726	-	14.11241841	13.18881891	13.18881891	-	-	6.594409453	0	0	0	0	0	0	0	0	0
        # mg_daikon_radish = Crops('microgreens - Daikon Radish	0	0	16	30	0	0	136.1030786	-	141.3885246	132.1388803	132.1388803	-	-	66.06921269	0	0	0	0	0	0	0	0	0
        # mg_dbcsk = Crops('microgreens - Dwarf Blue Curled Skotch kale	0	0	16	30	0	0	26.24842488	-	27.26802413	25.48406667	25.48406667	-	-	12.74203333	0	0	0	0	0	0	0	0	0
        # mg_kale = Crops('microgreens - Kale	0	0	16	30	0	0	33.96161816	-	35.28059104	32.97250224	32.97250224	-	-	16.48647861	0	0	0	0	0	0	0	0	0
        # mg_lacinato_kale = Crops('microgreens - Lacinato Kale	0	0	16	30	0	0	34.02576965	-	35.34701741	33.03483383	33.03483383	-	-	16.51741692	0	0	0	0	0	0	0	0	0
        # mg_mizuna = Crops('microgreens - Mizuna	0	0	16	30	0	0	32.60579229	-	33.87198806	31.65580423	31.65580423	-	-	15.8281296	0	0	0	0	0	0	0	0	0
        # mg_mustard = Crops('microgreens - Mustard	0	0	16	30	0	0	38.81347289	-	40.32080547	37.6828597	37.6828597	-	-	18.84142985	0	0	0	0	0	0	0	0	0
        # mg_mustard_greens = Crops('microgreens - Mustard greens	0	0	16	30	0	0	45.36738955	-	47.12950821	44.04614179	44.04614179	-	-	22.0230709	0	0	0	0	0	0	0	0	0
        # mg_parsley = Crops('microgreens - Parsley	0	0	16	30	0	0	13.58464726	-	14.11241841	13.18881891	13.18881891	-	-	6.594409453	0	0	0	0	0	0	0	0	0
        # mg_peashoots = Crops('microgreens - Peashoots	0	0	16	30	0	0	74.70327562	-	77.60465199	72.52758458	72.52758458	-	-	36.26379229	0	0	0	0	0	0	0	0	0
        # mg_radish = Crops('microgreens - Radish	0	0	16	30	0	0	73.15545025	-	75.99631493	71.02480174	71.02480174	-	-	35.51217338	0	0	0	0	0	0	0	0	0
        # mg_red_acre_cabbage = Crops('microgreens - Red acre cabbage	0	0	16	30	0	0	40.83083259	-	42.4164209	39.64152761	39.64152761	-	-	19.82099129	0	0	0	0	0	0	0	0	0
        # mg_red_russian_kale = Crops('microgreens - Red Russian Kale	0	0	16	30	0	0	45.36784453	-	47.12950821	44.04614179	44.04614179	-	-	22.0230709	0	0	0	0	0	0	0	0	0
        # mg_red_velvet_lettuce = Crops('microgreens - Red Velvet Lettuce	0	0	16	30	0	0	31.1093791	-	32.31733806	30.20306866	30.20306866	-	-	15.10153433	0	0	0	0	0	0	0	0	0
        # mg_scallion = Crops('microgreens - Scallion	0	0	16	30	0	0	14.94320299	-	15.52329627	14.50779179	14.50779179	-	-	7.254123383	0	0	0	0	0	0	0	0	0
        # mg_sorrel = Crops('microgreens - Sorrell	0	0	16	30	0	0	58.83237836	-	61.11680846	57.11848706	57.11848706	-	-	28.55924353	0	0	0	0	0	0	0	0	0
        # mg_swiss_chard = Crops('microgreens - Swiss Chard	0	0	16	30	0	0	34.02576965	-	35.34701741	33.03483383	33.03483383	-	-	16.51741692	0	0	0	0	0	0	0	0	0
        # mg_tatsoi = Crops('microgreens - Tatsoi	0	0	16	30	0	0	33.57215945	-	34.87566318	32.59441791	32.59441791	-	-	16.29720896	0	0	0	0	0	0	0	0	0
        # mg_watercress = Crops('microgreens - Watercress	0	0	16	30	0	0	27.16929453	-	28.22438184	26.37809279	26.37809279	-	-	13.18881891	0	0	0	0	0	0	0	0	0
        # mustard_greens = Crops('mustard Greens	0	0	16	30	0	0	56.13619577	29.70057143	58.31643657	54.50101517	54.50101517	-	-	27.25073507	0	0	0	0	0	0	0	0	0
        none = Crops('none',	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 'n/a')
        # oregano = Crops('oregano	0	0	16	30	0	0		0.292							0	0	0	0	0	0	0	0	0
        # papaya_hawaiian = Crops('papaya - Hawaiian	0	0	16	30	0	0	-	-	-	-	-	1.619711443	-	9.08994801	0	0	0	0	0	0	0	0	0
        # papaya_maradol = Crops('papaya - Maradol	0	0	16	30	0	0	-	-	-	-	-	1.716166169	-	0.858083085	0	0	0	0	0	0	0	0	0
        # parsley = Crops('parsley	0	0	16	30	0	0	14.03416269	3.587428571	14.57922289	13.62559502	13.62559502	-		6.812797512	0	0	0	0	0	0	0	0	0
        # pepperbell = Crops('pepperbell	0	0	16	30	0	0	-	-	-	-	-	42.28629801	42.28629801	21.143149	0	0	0	0	0	0	0	0	0
        # peppermint = Crops('peppermint	0	0	16	30	0	0	30.93148383		32.13261816	30.03063308	30.03063308	-	-	15.01508905	0	0	0	0	0	0	0	0	0
        # raspberry = Crops('raspberry	0	0	16	30	0	0	-	-	-	-	-	0.572813682	0.572813682	0.286179353	0	0	0	0	0	0	0	0	0
        # rosemary = Crops('rosemary	0	0	16	30	0	0	-	-	-	-	-	6.386940796	-	3.193470398	0	0	0	0	0	0	0	0	0
        # sage = Crops('sage	0	0	16	30	0	0	32.47885423	-	33.74004527	31.53296095	31.53296095	-	-	15.76625299	0	0	0	0	0	0	0	0	0
        # salad_mix_baby_greens = Crops('salad Mix - Baby Greens	0	0	16	30	0	0	35.08540672	-	36.44760224	34.06353259	34.06353259	-	-	17.03153881	0	0	0	0	0	0	0	0	0
        # scallion = Crops('scallion	0	0	16	30	0	0	5.017010697	-	5.212195025	4.870963682	4.870963682	-	-	2.435481841	0	0	0	0	0	0	0	0	0
        # shallot = Crops('shallot	0	0	16	30	0	0	-	-	9.884789552	9.2382699	-	-	-	4.618907463	0	0	0	0	0	0	0	0	0
        # sorrel_green = Crops('sorrel -Green	0	0	16	30	0	0	15.82903955	-	16.44371095	15.36814975	15.36814975	-	-	7.684074876	0	0	0	0	0	0	0	0	0
        # spearmint = Crops('spearmint	0	0	16	30	0	0	42.10248806	-	43.73721368	40.87587512	40.87587512	-	-	20.43793756	0	0	0	0	0	0	0	0	0
        # spinach = Crops('spinach	295	17	16	30	0.002	0.08	22.81700249	-	23.70329403	22.15273881	22.15273881	-	-	11.0763694	402	0	337	0.2	0.1	0.2	0.0017	0.67	10.5
        # spring_onion = Crops('spring Onion	0	0	16	30	0	0	-	-	8.747351741	8.174993035	-	-	-	4.087496517	0	0	0	0	0	0	0	0	0
        # stevia = Crops('stevia	0	0	16	30	0	0	6.315054726	-	6.560741294	6.131244776	6.131244776	-	-	3.065622388	0	0	0	0	0	0	0	0	0
        # strawberry = Crops('strawberry	255	11	12	85	0.042	0.08	7.348303234	-	7.633572637	7.134464925	-	-	-	3.567004975	198	0.5	382	0.3	0.2	0.2	0.006	0.33	24.1
        # sweet_pepper = Crops('sweet Pepper	250	10.8	12	68	0.101	0.1	-	-	-	-	-	-	-	-	150	1	876	0.3	0.8	0.2	0.0148	0.25	58.4
        # tarragon = Crops('tarragon	0	0	16	30	0	0	8.33878408	-	8.662271393	8.095827363	8.095827363	-	-	4.047913682	0	0	0	0	0	0	0	0	0
        # thyme = Crops('thyme	0	0	16	30	0	0	-	-	-	18.3941893	-	-	-	9.197322139	0	0	0	0	0	0	0	0	0
        # tomato_cherry = Crops('tomato - Cherry	0	0	16	30	0	0	-	-	-	-	-	57.32140597	57.32140597	28.66070299	0	0	0	0	0	0	0	0	0
        # tomato_salad = Crops('tomatoes Salad	313	13.5	12	75	0.291	0.06	-	-	-	-	-	62.60548706	62.60548706	31.30274353	300	4.9	2036	0.5	1.2	0.2	0.0242	0.5	113.1
        # turnips = Crops('turnips	0	0	16	30	0	0	-	-	11.43625473	10.68827562	-	-	-	5.344137811	0	0	0	0	0	0	0	0	0
        # watercress = Crops('watercress	0	0	16	30	0	0	12.97725547	-	13.48546269	12.60326592	12.60326592	-	-	6.301860448	0	0	0	0	0	0	0	0	0
        # watermelon_mini = Crops('watermelon - mini	350	15.1	12	85	0.96	0.08	-	-	-	-	-	4.504708706	4.504708706	2.252126866	198	12	549	1.2	0.6	0.3	0.0063	0.33	34.7
        # watermelon_standard = Crops('watermelon - standard	0	0	12	85	0	0	-	-	-	-	-	7.770065174	7.770065174	3.885032587	0	0	0	0	0	0	0	0	0
        return


@dataclass(init=False)
class CropParameters:
    type: str
    percent: float
    system: str
    harvest_weight: float
    product_weight: float
    customer_percent: float
    price1: float
    price2: float

    def __init__(self):
        pass


def get_crop(crop_type):
    crop = None
    if crop_type == 'Basil - Lemon':
        crop = Crops('Basil - Lemon', 'n/a',	'n/a',	14,	42,	'n/a', 'n/a', 'n/a', 13.067,	'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a', 0.03, 0.97, 'herbs')
    elif crop_type == 'Lettuce (Farm Urban Mix)':
        crop = Crops('Lettuce (Farm Urban Mix)',	0,	0,	16,	35,	0,	0,	0,	33,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0.03, 0.97, 'leafy greens')
    elif crop_type == 'Basil - Genovese':
        crop = Crops('Basil - Genovese',	0,	0,	14,	42,	0,	0,	34.33833756,	9.802857143,	35.67186965,	33.33830224,	33.33830224, 0,	0,	16.66892363,	0,	0,	0,	0,	0,	0,	0,	0,	0.03, 0.97, 'herbs')
    elif crop_type == 'None':
        crop = Crops('none',	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 1, 'n/a')
    else:
        raise RuntimeError(f"Unknown crop: {crop_type}")
    return crop
