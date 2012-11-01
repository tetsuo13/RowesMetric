# UNC Greensboro, CSC 593, Fall 2012
#
# By Andrei Nicholson
# Mentored by Dr. Shan Suthaharan
#
# TODO: This should be a class.

# Make all divisions result in a float.
from __future__ import division

from RoweMetric import exposure
from RoweMetric import globals

def calculate_k3(region_area):
    """Based on noticeability of one agent in on region.

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
    """

    if region_area > 0.5:
        raise Exception('Area of region must be less than 0.5, was ' +
                        str(region_area))

    return 1 / 39

    #region_area = 1
    probability = 1.0
    number_of_agents = 1
    x = region_area / number_of_agents
    print 1 / ((1 / x) - 1)
    print 

    k3 = probability / (number_of_agents - region_area)
    print 1 / number_of_agents
    print k3
    import sys
    sys.exit()

def do_noticeability(database, region_area, top_left, bottom_right):
    """Calculate noticeability of non-deceptive and deceptive agents in region.

    """
    def calculate_noticeability(k3, p_agent):
        if p_agent == globals.NOT_APPLICABLE:
            return p_agent
        if p_agent == 0:
            return 0
        return round(k3 / (k3 + p_agent), 4)

    k3 = calculate_k3(region_area)
    p_nondeceptive, p_deceptive = exposure.probability_in_region(database,
                                                                 top_left,
                                                                 bottom_right)

    return [calculate_noticeability(k3, p_nondeceptive),
            calculate_noticeability(k3, p_deceptive)]