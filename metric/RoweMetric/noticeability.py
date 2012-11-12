# UNC Greensboro, CSC 593, Fall 2012
#
# By Andrei Nicholson
# Mentored by Dr. Shan Suthaharan

# Make all divisions result in a float.
from __future__ import division

from RoweMetric import exposure
from RoweMetric import globals

class Noticeability():
    def __init__(self, grid, database, regions):
        self._database = database
        self._regions = regions
        self._k3 = self._calculate_k3(grid.area_of_region())

    def _calculate_k3(self, region_area):
        """Based on noticeability of one agent in one region.

        region_area     k3
        ----------- = ------
        num_agents    k3 + p

        0.5 * 0.5     k3
        --------- = ------
            1       k3 + 1

        1     k3
        - = ------
        4   k3 + 1

        4k3 = k3 + 1

        3k3 = 1

        k3 = 1/3

        Function originally returned 1/39.
        """

        if region_area > 0.5:
            raise Exception('Area of region must be less than 0.5, was ' +
                            str(region_area))

        p_agent = 1.0
        num_agents = 1
        return p_agent / (((region_area * region_area) ** -1) - (num_agents ** -1))

    def calculate(self, top_left, bottom_right):
        """Noticeability of non-deceptive and deceptive agents in region.
        """
        def calculate_noticeability(k3, p_agent):
            if p_agent == globals.NOT_APPLICABLE:
                return p_agent
            elif p_agent == 0:
                return 0
            return round(k3 / (k3 + p_agent), 4)

        p_nondeceptive, p_deceptive = exposure.probability_in_region(self._database,
                                                                     top_left,
                                                                     bottom_right)

        return [calculate_noticeability(self._k3, p_nondeceptive),
                calculate_noticeability(self._k3, p_deceptive)]
