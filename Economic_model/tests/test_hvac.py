#!/usr/bin/env python3
'''
Created on 25 Aug 2019
@author: jmht
'''
from Economic_model.tests.vf_hvac import calc_saturated_vapour_pressure_air
from Economic_model.tests.vf_hvac import calc_saturated_vapour_pressure_air_FAO
from Economic_model.tests.vf_hvac import calc_stomatal_resistance
from Economic_model.tests.vf_hvac import calc_net_radiation
from Economic_model.tests.vf_hvac import calc_saturated_vapour_concentration_air
from Economic_model.tests.vf_hvac import calc_vapour_concentration_air
from Economic_model.tests.vf_hvac import calc_vapour_concentration_deficit
from Economic_model.tests.vf_hvac import calc_vapour_concentration_surface
from Economic_model.tests.vf_hvac import calc_sensible_heat_exchange


def test_saturated_vapour_pressure_air():
    temp_air = 25.0
    saturated_vapour_pressure = 3158
    assert abs(calc_saturated_vapour_pressure_air(temp_air) - saturated_vapour_pressure) < 1


def test_saturated_vapour_pressure_air_FAO():
    temp_air = 25.0
    saturated_vapour_pressure = 3.1688
    assert abs(calc_saturated_vapour_pressure_air_FAO(temp_air) - saturated_vapour_pressure) < 0.001


def test_saturated_vapour_concentration_air():
    """Values taken from: https://www.engineeringtoolbox.com/relative-humidity-air-d_687.html"""
    temp_air = 20.0
    ref_concentration = 17.2  # they use 17.8 - difference due to their use of 273 rather then 273.15 for zero Kelvin
    assert abs(calc_saturated_vapour_concentration_air(temp_air) - ref_concentration) < 0.1


def test_calc_vapour_concentration_air():
    """Values taken from: https://www.engineeringtoolbox.com/relative-humidity-air-d_687.html"""
    temp_air = 20.0
    relative_humidity = 57.8
    ref_concentration = 10
    assert abs(calc_vapour_concentration_air(temp_air, relative_humidity) - ref_concentration) < 0.1


def test_vapour_concentration_deficit():
    """Data from experiment 3 from table 1 of paper"""
    temp_air = 21
    relative_humidity = 76
    vapour_concentration_deficit = 4.4
    assert abs(calc_vapour_concentration_deficit(temp_air, relative_humidity) - vapour_concentration_deficit) < 0.1


def test_stomatal_resistance():
    """Data from experiment 1(A) from table 1 of paper """
    ppfd = 140
    ref_stomatal_resistance = 289
    assert abs(calc_stomatal_resistance(ppfd) - ref_stomatal_resistance) < 1


def test_stomatal_resistance_null():
    ppfd = 0
    ref_stomatal_resistance = 450
    assert abs(calc_stomatal_resistance(ppfd) - ref_stomatal_resistance) < 1


def test_net_radiation():
    """Data from set A from table 2 of paper"""
    ppfd = 600
    reflection_coefficient = 0.05
    cultivation_area_coverage = 0.95
    net_radiation = calc_net_radiation(ppfd, reflection_coefficient, cultivation_area_coverage)
    assert abs(net_radiation - 108.3) < 0.1


def test_sensible_heat_exchange():
    # NEEDS CHECKING
    temp_air = 21.0
    temp_surface = 23.0
    lai = 3.0
    vapour_resistance = 100
    ref_value = 0.06
    assert (abs(calc_sensible_heat_exchange(temp_air, temp_surface, lai, vapour_resistance) - ref_value) < 0.01)


def test_latent_heat_flux():
    # NEEDS CHECKING
    pass


if __name__ == '__main__':
    import sys
    import pytest

    pytest.main([__file__] + sys.argv[1:])
    # pytest.main([__file__] + sys.argv[1:])
    import logging

    logging.basicConfig(level=logging.DEBUG)

    # def test_calc_vapour_concentration_surface():
    temp_air = 21.0
    temp_surface = 23.0
    relative_humidity = 73
    vapour_concentration_air = calc_vapour_concentration_air(temp_air, relative_humidity)
    print(vapour_concentration_air)
    vp_surface = calc_vapour_concentration_surface(temp_air, temp_surface, vapour_concentration_air)
    print(vp_surface)

#     temp_air = 21.0
#     temp_surface = 23.0
#     lai = 3.0
#     vapour_resistance = 100
#     relative_humidity = 73
#     ppfd = 600
#     ref_value =  42.85
#     print(calc_latent_heat_flux(temp_air, temp_surface, relative_humidity, ppfd, lai, vapour_resistance))
# assert(abs(calc_latent_heat_flux(temp_air, temp_surface, relative_humidity, ppfd, lai, vapour_resistance) - ref_value) < 0.01)

#     temp_air = 21.0
#     temp_surface = 23.0
#     lai = 3.0
#     vapour_resistance = 100
#     print(calc_sensible_heat_exchange(temp_air, temp_surface, lai, vapour_resistance))