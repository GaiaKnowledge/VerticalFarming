#============================================== FACTORS AND CROP YIELD ==================================================#

'''
Created on 17 Sep 2019
@author: fbdo
'''
from fbr_maincode import calc_crop_ppfd_reqs
from fbr_maincode import calc_PAR_factor
from fbr_maincode import calc_CO2_factor
from fbr_maincode import calc_failure_rate
from fbr_maincode import calc_standard_yield
from fbr_maincode import calc_plant_area
from fbr_maincode import get_temp_crop_reqs
from fbr_maincode import calc_temperature_factor
from fbr_maincode import calc_adjusted_yield

def test_adjusted_yield():
    ys = 78.5
    tm = 4.4861
    pa = 235
    parf = 1
    co2f = 1
    tf = 0.85
    fr = 0.05
    ref_adjusted_yield = 66825  # kg per year
    assert abs(calc_adjusted_yield(ys, pa, parf, co2f, tf, fr) - ref_adjusted_yield) < 1

    def calc_adjusted_yield(ys, pa, PARf, co2f, tf, fr):
        """
            Adjusted Plant Yield Equation
            Notes
            -----
                Ya = Ys x PA x PARf x co2f x Tf x (1 - Fr)
                Adjusted Plant Yield = Standard Yield x Plant Area x PAR factor
                PARf = ratio of actual PAR delivered to plant canopy compared to theoretical plant requirements. In artificial lighting
                VF the value was 1 as controlled at optimal level. Sun-fed plant level from EcoTect simulation.) x
                co2f = Increment by co2 enrichment
                Tf = Temperature factor (reflects reduction of yield caused by overheating or freezing of the growing area
                if indoor temperature is uncontrolled by hvac or other systems, value can be set for 0.9 for preliminary estimation)
                Fr = Failure rate, by default set at 5%
        """
        ya = ys * pa * PARf * co2f * tf * (1 - fr)
        return ya