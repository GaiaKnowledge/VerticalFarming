from Economic_model.scenario_module import Scenario
from Economic_model.equipment_module import GrowSystem
from Economic_model.equipment_module import LightSystem


class YieldFactors(Scenario, GrowSystem, LightSystem):
    def __init__(self):
        super().__init__()

    def calc_PAR_factor(ppfd_lights, crop_ppfd_reqs):
        parf = ppfd_lights / crop_ppfd_reqs
        return parf

    def calc_co2_factor(co2_enrichment):
        if co2_enrichment:
            co2f = 1
        else:
            co2f = 0.9
        return co2f

    def calc_failure_rate():
        """30% in year 1, 20% year 2, 10% year 3, 5% onwards."""
        fr = gauss(0.05, 0.02)
        return fr

    def calc_standard_yield(crop):  # Standard yield per year
        """ Taken from table from Shao Economic Estimation Tool (2017)"""
        if crop == 'lettuce':
            return 78.5  # kg/m2/year
        else:
            raise RuntimeError("Unknown crop: {}".format(crop))

    def calc_plant_area(grow_area, grow_system, no_of_racks):
        """ Plant area calculated using space taken by Racks - formula from Refarmers spreadsheet 2018"""
        if grow_system == 'ziprack_8':
            pa = (no_of_racks * 4.300986) + 3.0612
        else:
            pa = grow_area
        return pa

    def calc_temperature_factor(hvac_control):
        """
            Temperature Factor Equation
            Notes:
            --------
                The reduction in yield caused by over heating or freezing of the grow area, especially if the farm is uncontrolled by hvac or other systems
                If no hvac control, preliminary value set to 0.85. This should be assessed depending on climate, crop reqs and level of hvac control
                High:
                Med:
                Low:
        """

        if hvac_control == "high":  # If advanced hvac control then temperature factor is 1
            tf = 1
        else:
            tf = 0.85
        return tf

    def calc_system_multiplier(grow_system):
        """
        System Multiplier
        Notes
        -----
            Standard yield isn't 100% accurate and doesn't consider high density vertical farming systems. The estimated yield
            from ZipGrow Ziprack_8 is 66,825 kg/year for 235m2 plant area. Adjusted yield without multiplier is  18447.5 kg/year
            66,825/18447.5 kg = 3.622442065320504
        """
        if grow_system == 'ziprack_8':
            system_multiplier = 3.622442065320504
        else:
            raise RuntimeError("Unknown grow system {}".format(grow_system))
        return system_multiplier

    # ---------------------------------------------- ADJUSTED YIELD ---------------------------------------------------- #

    def calc_adjusted_yield(ys, pa, parf, co2f, tf, fr, system_multiplier):
        """
            Adjusted Plant Yield Equation
            Notes
            -----
                Ya = Ys x PA x parf x co2f x Tf x (1 - Fr)
                Adjusted Plant Yield = Standard Yield x Plant Area x PAR factor
                parf = ratio of actual PAR delivered to plant canopy compared to theoretical plant requirements. In artificial lighting
                VF the value was 1 as controlled at optimal level. Sun-fed plant level from EcoTect simulation.) x
                co2f = Increment by co2 enrichment
                Tf = Temperature factor (reflects reduction of yield caused by overheating or freezing of the growing area
                if indoor temperature is uncontrolled by hvac or other systems, value can be set for 0.9 for preliminary estimation)
                Fr = Failure rate, by default set 30% year 1, 20% year 2, 10% year 3 and 5% onwards
                Sm = System multiplier (best case scenario x system multiplier)
        """
        ya = ys * pa * parf * co2f * tf * (1 - fr) * system_multiplier
        return ya