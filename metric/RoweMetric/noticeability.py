# UNC Greensboro, CSC 593, Fall 2012
#
# By Andrei Nicholson
# Mentored by Dr. Shan Suthaharan

# Make all divisions result in a float.
from __future__ import division

from RoweMetric import exposure
from RoweMetric import globals

def do_noticeability(database, top_left, bottom_right):
    """Calculate noticeability of non-deceptive and deceptive agents in region.

    """
    def calculate_noticeability(p_agent):
        # TODO: Needs to be a calculation of something.
        k3 = 0.001
        if p_agent == globals.NOT_APPLICABLE:
            return p_agent
        if p_agent == 0:
            return 0
        return round(k3 / (k3 + p_agent), 4)

    p_nondeceptive, p_deceptive = exposure.probability_in_region(database,
                                                                 top_left,
                                                                 bottom_right)

    return [calculate_noticeability(p_nondeceptive),
            calculate_noticeability(p_deceptive)]