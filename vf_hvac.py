"""
The MATLAB (2016) model executes an iterative process to simultaneously solve (Eqs. 4–7), processing the net PAR flux density,
the sur- face and aerodynamic resistances as outlined above (Eqs. 8–10).
The iterative process is based on the aforementioned equations and is performed in a continuous loop. For each set interval of Ta,
the model calculates the corresponding Ts at which the energy balance (Rnet– H–λE) is closest to zero. The model utilises a
continuous loop to ap- proach this value at the set discretisation and consequently indexes the value closest to zero.
Finally, the model lists the different variables congruent with this zero energy balance, in particular the quantity of the
sensible (H) and latent (λE) heat exchange.
REM:
https://www.engineeringtoolbox.com/relative-humidity-air-d_687.html
Relative humidity can also be expressed as the ratio of the vapor density of the air -
to the saturation vapor density at the the actual dry bulb temperature.
relative_humidity = vapor_density / saturation_vapor_density
http://hyperphysics.phy-astr.gsu.edu/hbase/Kinetic/watvap.html
saturation_vapor_density = 618 g/m-3 at 20C
https://appgeodb.nancy.inra.fr/biljou/pdf/Allen_FAO1998.pdf
http://www.fao.org/3/X0490E/x0490e0k.htm
Hi Luuk,
Thanks again for your help. I've implemented a model in Python but am struggling to get it to work - possibly because of confusion over the different units that are being used.
It’s probably easiest if I demonstrate the issue with the Latent Heat calculation and rough data taken from the paper (this won’t be exact, because I’m taking data from the graph, but I hope it will show where the problem lies.
If I take the data from table 1 (experiment 1) and take the data for a ppfd of 600, I have the following data from the paper:
Air temperature (Ta): 21C
LAI: 3.0
Aerodynamic boundary layer resistance (R_a): 100 s m-1
Stomatal resistance (R_s): 158 s m-1
I also need the following constants, for which I’ve taken standard SI values:
Heat capacity of air (Rc): 1.003 J  kg-1 C-1
Latent heat of evaporation of water (Lambda):  2264705 J kg-1
From figure 3 it looks like the transpiration rate for 600 ppfd is approximately: 0.051g m-2 s
From the FAO page on Crop evapotranspiration (http://www.fao.org/3/X0490E/x0490e0i.htm#annex%201.%20units%20and%20symbols) it looks like you multiply by 2450 to go from g m-2 s to W m-2, so that makes the transpiration rate for 600 ppfd approximately: 125 W m-2 (this seems roughly correct to me).
Equation 6 gives the latent heat exchange (and therefore the transpiration rate) as:
La_E = LAI * Lambda * ((X_sts - X_sta) / (R_s + R_a))
so rearranging gives me:
X_sts - X_sta = (La_E * (R_s + R_a) ) / (LAI * Lambda)
X_sts - X_sta = (125 * ( 158 + 100)) / (3.0 * 2264705) = 0.0047449 kg m-3
Equation 7 to calculate the vapour concentration at the surface is:
X_sts = X_sta + (Rc / Lambda) * Epsilon * (Ts - Ta)
If I rearrange to get Epsilon, I get:
Epsilon = (X_sts -  X_sta) * Lambda / ((Ts - Ta) * Rc)
If I assume that the temperature difference is of the order of a few degrees (say Ts = 23C) and Ts - Ta = 2 (again, it’s just to show an order of magnitude), then:
Epsilon = (0.0047449 * 2264705) / (2 * 1.003)
Epsilon = 5356.83
You said that Epsilon can be calculated as:
epsilon = delta / gamma
Where delta = 0.04145 * exp(0.06088*T_s) (kPa/C)
Gamma = 66.5  (Pascal/K) (gamma is a psychometric constant)
For 23C, this gives me:
0.0025
Even if I assume that this is for kPa and multiply by 1000, I only get:
2.529
So I’m out by several orders of magnitude.
I’ve tried calculating Epsilon using the data on the FAO webpage, but this also gives me a similar value to the above.
I’d be most grateful if you could help me to work out where I’m going wrong as the rest of my code seems to be working fine.
Best wishes,
Jens
"""
import logging
import math

from scipy.optimize import root_scalar

# https://www.ohio.edu/mechanical/thermo/property_tables/air/air_cp_cv.html at 300K/26.85C
HEAT_CAPACITY_OF_AIR = 1003  # J kg-1 C-1
HEAT_CAPACITY_OF_AIR_GRAMS = 1.003  # J g-1 C-1

# Need canonical reference: https://en.wikipedia.org/wiki/Latent_heat
LATENT_HEAT_WATER = 2264705  # J Kg-1
LATENT_HEAT_WATER_GRAMS = 2264.705  # J g-1

# Valye from paper
PSYCHOMETRIC_CONSTANT = 65.0  # Pa/K

IDEAL_GAS_CONSTANT = 8.3145  # J mol-1 K-1

MOLAR_MASS_H2O_GRAMS = 18.01528  # g mol-1

ZERO_DEGREES_IN_KELVIN = 273.15

PLANK_CONSTANT = 6.626 * 10 ** -34
SPEED_OF_LIGHT = 2.998 * 10 ** 8  # m s-1
AVOGADRO_NUMBER = 6.0221367 * 10 ** 23

logger = logging.getLogger()


def calc_temp_surface(*,  # Force all keyword arguments
                      temp_air,
                      ppfd,
                      relative_humidity,
                      lai,
                      vapour_resistance,
                      reflection_coefficient,
                      cultivation_area_coverage):
    logger.info("""Calculating surface temperature with:
    Air temperature: {}
    PPFD: {}
    Relative Humidity {}
    LAI: {}
    Vapour resistance: {}
    Reflection, coefficient: {}
    Cultivation Area Coverage: {}
""".format(temp_air, ppfd, relative_humidity, lai, vapour_resistance, reflection_coefficient,
           cultivation_area_coverage))

    def calc_energy_balance(temp_surface, net_radiation):
        sensible_heat_exchange = calc_sensible_heat_exchange(temp_air, temp_surface, lai, vapour_resistance)
        latent_heat_flux = calc_latent_heat_flux(temp_air, temp_surface, relative_humidity, ppfd, lai,
                                                 vapour_resistance)
        energy_balance = net_radiation - sensible_heat_exchange - latent_heat_flux
        logger.debug("TEMP, SENSIBLE, LATENT, NET, residual: %s %s %s %s %s", temp_surface, sensible_heat_exchange,
                     latent_heat_flux, net_radiation, energy_balance)
        return energy_balance

    net_radiation = calc_net_radiation(ppfd, reflection_coefficient, cultivation_area_coverage)

    limit = 10.0
    xa = temp_air - limit
    xb = temp_air + limit
    args = (net_radiation,)
    result = root_scalar(calc_energy_balance, bracket=[xa, xb], args=args)

    assert result.converged
    temp_surface = result.root
    return temp_surface


def calc_net_radiation(ppfd, reflection_coefficient, cultivation_area_coverage):
    """
    8. Submodel for net radiation
    Rnet = (1 - ρr) * Ilighting * CAC
    ρr: reflection coefficient
    Ilighting: radiation
    CAC: cultivation area cover

    NOTES
    -----
    cultivation_area_coverage = 0.9 # value from section 3.1.1 of paper
    reflection_coefficient = 0.05 # Luuk Gaamans personal communication
    """
    lighting_radiation = calc_lighting_radiation(ppfd)
    return (1 - reflection_coefficient) * lighting_radiation * cultivation_area_coverage


def calc_lighting_radiation(ppfd):
    """Values taken from paper


    # E = hf = hc/w
    photon_energy = AVOGADRO_NUMBER * PLANK_CONSTANT * n * SPEED_OF_LIGHT  / wavelength

    PPFD measured in mol m-2 s-1

    Flux density measured in W m-2


    # https://www.researchgate.net/post/Can_I_convert_PAR_photo_active_radiation_value_of_micro_mole_M2_S_to_Solar_radiation_in_Watt_m22
    # Rule of thumb is 1 W m-2 = 4.57 umol m-2 so 140 ppfd ~= 30.6



#     import scipy.integrate
#     ppfd = 140 #umol
#     def pe(wavelength, ppfd):
#         # ppfd in umol
#         # wavelength in nm
#         n = ppfd * 10**-6 #
#         return AVOGADRO_NUMBER * PLANK_CONSTANT * SPEED_OF_LIGHT * n / (wavelength * 10**-9)
#     #r = scipy.integrate.quad(pe, 400, 700)
#     #print(pe(700))
#     #print(r)
#
# #     ppfd = 140
# #     e = 20.82
# #     w = 804.4165185104332
#     ppfd = 200
#     e = 41.0
#     #w = 555
#     #e = AVOGADRO_NUMBER * PLANK_CONSTANT * SPEED_OF_LIGHT * ppfd * 10**-6  / (w * 10**-9)
#    # print(e)
#
#     w = AVOGADRO_NUMBER * PLANK_CONSTANT * SPEED_OF_LIGHT * ppfd * 10**-6 / (e * 10**-9)
#
#     print(w)

    """
    # Guess from paper
    if ppfd == 140:
        lighting_radiation = 28
    elif ppfd == 200:
        lighting_radiation = 41
    elif ppfd == 300:
        lighting_radiation = 59
    elif ppfd == 400:
        lighting_radiation = 79.6
    elif ppfd == 450:
        lighting_radiation = 90.8
    elif ppfd == 600:
        lighting_radiation = 120
    else:
        assert False
    return lighting_radiation


def calc_sensible_heat_exchange(temp_air, temp_surface, lai, vapour_resistance):
    """
    5. Sensible heat exchange H
    H = LAI * ρa * cp * (Ts - Ta / ra)
    LAI: Leaf Area Index
    ρa: Density of air
    cp: Specific heat of air
    Ts: temperature at the transpiring surface
    Ta: temperature of surrounding air
    ra: aerodynamic resistance to heat

    results are in:
    J g-1 * T * m-1 s
    """
    # return lai * HEAT_CAPACITY_OF_AIR_GRAMS * ((temp_surface - temp_air) / vapour_resistance)
    return lai * HEAT_CAPACITY_OF_AIR * ((temp_surface - temp_air) / vapour_resistance)


def calc_latent_heat_flux(temp_air, temp_surface, relative_humidity, ppfd, lai, vapour_resistance):
    """

    6. Latent Heat Flux λE - I think this is the evapotranspiration rate
    λE = LAI * λ * (χs - χa) / (rs + ra)
    LAI: Leaf Area Index
    λ: latent heat of the evaporation of water - J g-1
    χs: vapour concentration at the transpiring surface - g m-3
    χa:  vapour concentration in surrounding air - g m-3
    rs: surface (or stomatal) resistance - s m-1
    ra: aerodynamic resistance to vapour transfer - s m-1

    results are in:
    J g-1 * g m-3 / s m-1
    J m-2 s-1
    """
    use_concentration = False
    if use_concentration:
        vapour_concentration_air = calc_vapour_concentration_air(temp_air, relative_humidity)
        logger.debug('vapour concentration air: {}'.format(vapour_concentration_air))
        vapour_concentration_surface = calc_vapour_concentration_surface(temp_air, temp_surface,
                                                                         vapour_concentration_air)
        logger.debug('vapour concentration surface: {}'.format(vapour_concentration_surface))
    else:
        vapour_pressure_air = calc_vapour_pressure_air(temp_air, relative_humidity)
        logger.debug('vapour pressure air: {}'.format(vapour_pressure_air))
        vapour_pressure_surface = calc_vapour_pressure_surface(temp_air, temp_surface, vapour_pressure_air)
        logger.debug('vapour pressure surface: {}'.format(vapour_pressure_surface))

    stomatal_resistance = calc_stomatal_resistance(ppfd)

    if use_concentration:
        return lai * LATENT_HEAT_WATER * ((vapour_concentration_surface - vapour_concentration_air) / (
                    stomatal_resistance + vapour_resistance))
    else:
        return lai * LATENT_HEAT_WATER * (
                    (vapour_pressure_surface - vapour_pressure_air) / (stomatal_resistance + vapour_resistance))


def calc_vapour_pressure_air(temp_air, relative_humidity):
    """
    jmht added - seems to get different results from below
    From: http://www.fao.org/3/X0490E/x0490e0k.htm
    saturated_vapour_pressure = 0.6108 * math.exp((17.27 * temp_air) / (temp_air + 237.3))
    Luuk Gaamans personal communication:
        Vapour concentration in the air = Relative humidity * saturated vapour concentration at air temperature (g m-3)
        Additional information:
        https://www.engineeringtoolbox.com/water-vapor-saturation-pressure-air-d_689.html
        https://www.engineeringtoolbox.com/relative-humidity-air-d_687.html
    """
    saturated_vapour_pressure = calc_saturated_vapour_pressure_air(temp_air)
    return saturated_vapour_pressure * (relative_humidity / 100)


def calc_vapour_concentration_air(temp_air, relative_humidity):
    """
    Luuk Gaamans personal communication:
        Vapour concentration in the air = Relative humidity * saturated vapour concentration at air temperature (g m-3)
        Additional information:
        https://www.engineeringtoolbox.com/water-vapor-saturation-pressure-air-d_689.html
        https://www.engineeringtoolbox.com/relative-humidity-air-d_687.html
    """
    return calc_saturated_vapour_concentration_air(temp_air) * (relative_humidity / 100)


def calc_saturated_vapour_concentration_air(temp_air):
    """saturated_vapour_concentration_air in g m-3 from temperature in degrees Celsius"""
    saturated_vapour_pressure = calc_saturated_vapour_pressure_air(temp_air)
    return vapour_concentration_from_pressure(saturated_vapour_pressure, temp_air)


def calc_saturated_vapour_pressure_air(temp_air):
    """Saturated vapour pressure of air in Pascals given air temperature in Degrees Celsius
    From: https://www.engineeringtoolbox.com/water-vapor-saturation-pressure-air-d_689.html
    """
    temp_air_k = temp_air + ZERO_DEGREES_IN_KELVIN
    return math.exp(77.345 + (0.0057 * temp_air_k) - (7235 / temp_air_k)) / temp_air_k ** 8.2


def calc_saturated_vapour_pressure_air_FAO(temp_air):
    """Saturated vapour pressure of air at temp_air in kPa

    From: http://www.fao.org/3/X0490E/x0490e0k.htm
    """
    return 0.611 * math.exp((17.27 * temp_air) / (temp_air + 237.3))


def calc_vapour_pressure_surface(temp_air, temp_surface, vapour_pressure_air):
    """
    7. Relation of χs to χa
    χs = χa + (ρa * cp) / λ * ε * (Ts - Ta)
    λ: latent heat of the evaporation of water
    ρa: Density of air
    cp: Specific heat of air
    χs: vapour concentration at the transpiring surface
    χa:  vapour concentration in surrounding air
    ε: vapour concentration (slope of the saturation function curve)

    """
    epsilon = calc_epsilon(temp_air) * 1000
    return vapour_pressure_air + (HEAT_CAPACITY_OF_AIR / LATENT_HEAT_WATER) * \
           epsilon * (temp_surface - temp_air)


def calc_vapour_concentration_surface(temp_air, temp_surface, vapour_concentration_air):
    """
    7. Relation of χs to χa
    χs = χa + (ρa * cp) / λ * ε * (Ts - Ta)
    λ: latent heat of the evaporation of water
    ρa: Density of air
    cp: Specific heat of air
    χs: vapour concentration at the transpiring surface
    χa:  vapour concentration in surrounding air
    ε: vapour concentration (slope of the saturation function curve)
    """
    epsilon = calc_epsilon(temp_air)
    return vapour_concentration_air + (HEAT_CAPACITY_OF_AIR / LATENT_HEAT_WATER) * \
           epsilon * (temp_surface - temp_air)


def calc_epsilon(temp_air):
    """
    Unitless but for kPa - so need to make sure everything else matches

    epsilon relates the vapour_pressure to concentration. Explanation from Luuk:
        The simplest way to calculate it is epsilon = delta / gamma
        Where delta = 0.04145 * exp(0.06088*T_s) (kPa/C)
        Gamma = 66.5  (Pascal/K) (gamma is a psychometric constant)
    """
    delta = 0.04145 * math.exp(0.06088 * temp_air)
    return delta / PSYCHOMETRIC_CONSTANT


def calc_epsilon_FAO(temp_air):
    """
    From: http://www.fao.org/3/X0490E/x0490e0k.htm
    Disagrees by order of magnitude with above
    """
    x = temp_air + 237.2
    return (2504 * math.exp((17.27 * temp_air) / x)) / math.pow(x, 2)


def vapour_concentration_from_pressure(vapour_pressure, temperature):
    """Calculate concentration in g m-3 from pressure in Pascals for Water

    Ideal Gas Law:
    PV = nRT => n/V = P/RT

    Multiply by molar mass to get concentration in g m-3
    """
    return vapour_pressure / (IDEAL_GAS_CONSTANT * (temperature + ZERO_DEGREES_IN_KELVIN)) * MOLAR_MASS_H2O_GRAMS


def calc_stomatal_resistance(ppfd):
    return 60 * (1500 + ppfd) / (200 + ppfd)


def calc_vapour_concentration_deficit(temp_air, relative_humidity):
    """https://en.wikipedia.org/wiki/Vapour-pressure_deficit"""
    svc = calc_saturated_vapour_concentration_air(temp_air)
    return svc * (1 - relative_humidity / 100)


def energydensity_to_evapotranspiration(energy_density):
    """

    Data from: http://www.fao.org/3/X0490E/x0490e0i.htm#annex%201.%20units%20and%20symbols

    Calculation:
    1 mm day-1 = 2.45 MJ m-2 day-1 # From FAO

    1mm over a 1 m-2 area = 1 * 1 * 1 10**6 = 1 * 10**6 m-3
    1 * 10**6 m-3 = 1 * 10**3 g = 1000g

    1000g day-1 = 1000 / (24 * 60 * 60) = 0.01157 g s-1


    2.45 MJ m-2 day-1 = 2.45 * 10**6 J m-2 day-1

    2.45 * 10**6 J m-2 day-1 = (2.45 * 10**6) / (24 * 60 * 60) = 28.356 W m-2

    so:
    28.356 W m-2 = 0.01157 g s-1

    so:
    1 W m-2 = 0.01157 / 28.356 = 0.000408 g s-1


    Full calculation:
    # Convert both results to J and per second
    (2.45 * 10**6) / (24 * 60 * 60)  = 1000 / (24 * 60 * 60)

    everything cancels
    1 W m-2 = 1 / (2.45 * 10**3) = 1 / 2450 = 0.00040816326530612246
    """
    return energy_density / 2450


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # variables
    temp_air = 21  # degrees celsius
    ppfd = 600  # umol m-2
    relative_humidity = 73  # %
    lai = 3  # no units
    vapour_resistance = 100  # s m-1
    reflection_coefficient = 0.05
    cultivation_area_coverage = 1.0

    temp_surface = calc_temp_surface(temp_air=temp_air,
                                     ppfd=ppfd,
                                     relative_humidity=relative_humidity,
                                     lai=lai,
                                     vapour_resistance=vapour_resistance,
                                     reflection_coefficient=reflection_coefficient,
                                     cultivation_area_coverage=cultivation_area_coverage)
    logger.info("Calculated surface temperature of: {}".format(temp_surface))

    net_radiation = calc_net_radiation(ppfd, reflection_coefficient, cultivation_area_coverage)
    sensible_heat_exchange = calc_sensible_heat_exchange(temp_air, temp_surface, lai, vapour_resistance)
    latent_heat_flux = calc_latent_heat_flux(temp_air, temp_surface, relative_humidity, ppfd, lai, vapour_resistance)

    print("VAPOUR CONCENTRATION DEFICIT ", calc_vapour_concentration_deficit(temp_air, relative_humidity))
    print("SURFACE TEMPERATURE ", temp_surface)
    print("NET RADIATION: ", net_radiation)
    print("SENSIBLE HEAT EXCHANGE ", sensible_heat_exchange)
    print("LATENT HEAT FLUX ", latent_heat_flux)
    print("EVAPOTRANSPIRATION ", energydensity_to_evapotranspiration(latent_heat_flux))
