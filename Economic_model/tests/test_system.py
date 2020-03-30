# ============================================== SYSTEM AND EXPECTED YIELDS #================================== #


'''
Created on 17 Sep 2019
@author: fbdo
'''
from Economic_model.fbr_maincode import calc_no_of_racks
from Economic_model.fbr_maincode import calc_harvest_weight
from Economic_model.fbr_maincode import get_gross_yield
from Economic_model.fbr_maincode import calc_plant_capacity
from Economic_model.fbr_maincode import calc_no_of_lights
from Economic_model.fbr_maincode import get_temp_crop_reqs


def test_no_of_racks_ziprack8():
    grow_system = 'ziprack_8'
    grow_area = 251
    ref_no_of_racks = 54
    assert abs(calc_no_of_racks(grow_system, grow_area) - ref_no_of_racks) == 0

def test_harvest_weight():
    crop = 'lettuce'
    harvest_weight = 0.5
    assert abs(calc_harvest_weight(crop) - harvest_weight) == 0


def test_gross_yield():
    """Values taken from: Developing an Economic Estimation Tool for Vertical Farms (Shao et al, 2017)"""
    crop = 'lettuce'
    ref_gross_yield = 78.5  # They state 78.5 kg per m^2 per year is possible in a vertical farm
    assert abs(get_gross_yield(crop) - ref_gross_yield) == 0


def test_plant_capacity():
    """Values taken from: https://www.engineeringtoolbox.com/relative-humidity-air-d_687.html"""
    crop = 'lettuce'
    grow_system = 'ziprack_8'
    no_of_racks = 54

    plant_capacity_yield, plant_capacity_number = calc_plant_capacity(crop, grow_system, no_of_racks)
    ref_plant_capacity_yield = 5346
    ref_plant_capacity_number = xxxx
    assert abs(plant_capacity_yield - ref_plant_capacity_yield) < 0.1


def test_no_of_lights():
    """Data from experiment 1(A) from table 1 of paper """
    grow_system = 'ziprack_8'
    no_of_racks = 54
    ref_no_of_lights = 1296
    assert abs(calc_no_of_lights(grow_system, no_of_racks) - ref_no_of_lights) == 0


def test_temp_crop_reqs():
    crop = 'lettuce'
    ref_temp_crop_reqs = 23.9  # Degrees celsius
    assert abs(get_temp_crop_reqs(crop) - ref_temp_crop_reqs) == 0

test_no_of_racks_ziprack8()