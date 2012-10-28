# Exposure of deceptive agent D is E = (1 / T) \sum_{t = 0}^{T - 1} s(t) \sum_{i = 0}^{N} v(i,t)n(i,t) (eq. 2)
#
# v(i,t) = visibility at time t from non-deceptive agent i
# p(x,y) = probability, agent at the location (x,y)
# q(s,h) = probability, speed and heading
# p(x,y)q(s,h) = joint probability, particular location with a particular velocity vector
# s(t) = k_1 / (k_1 + p(x,y)q(s,h)) (eq. 3) (scale of 0 to 1)
# n(i,t) = noticeability at time t by agent i (scale of 0 to 1)
# n(i,t) = k_3 / (k_3 + p(x,y))

# numpy.random.normal(0, 0.01, 10)

# Look through positions_seen for other (x,y) locations (with buffer?). The
# return value of the proabability functions is
#
#    (how many times this (x,y) has been observed before) / (total positions)
#


#If n(x,y) is 1, p(x,y) = 0

# Make all divisions result in a float.
from __future__ import division

import json 
import math
import sys

k1 = 0.5
k2 = 0.5

database = []

NOT_APPLICABLE = '--'

def calculate_speed(position_1, position_2):
    """
    Distance in meters per second.
    TODO: Distance will need to be measured in whatever Kinect uses.
    """
    x1, y1 = position_1[0], position_1[1]
    x2, y2 = position_2[0], position_2[1]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def calculate_heading(position_1, position_2):
    x1, y1 = position_1[0], position_1[1]
    x2, y2 = position_2[0], position_2[1]

    delta_x = x2 - x1
    delta_y = y2 - y1

    return math.degrees(math.atan2(delta_y, delta_x))

def get_second_operand(i, list):
    """
    TODO: What is the heading if it's the last position?
    """

    # Grab the next item in the list.
    j = i + 1

    # If the next item is past the last, get the previous item instead.
    if i == len(list) - 1:
        j = i - 1

    return [list[j][0], list[j][1]]

def setup_database(data_file_path):
    data_file = open(data_file_path).read()
    return json.loads(data_file)

# p(x,y)
def probability_in_region(database, top_left, bottom_right):
    """Calculate the probability of observing an ordinary agent in a region.

    Returns two probability values for region: ordinary agent, deceptive agent.
    """
    deceptive_agents = []
    nondeceptive_agents = []

    # Find the agents who have paths crossing into this region.
    for agent in database['agents']:
        try:
            for position in agent['positions']:
                if (position[0] >= top_left[0] and position[0] <= bottom_right[0] and
                    position[1] <= top_left[1] and position[1] >= bottom_right[1]):
                    if agent['deceptive']:
                        deceptive_agents.append(agent['agentid'])
                    else:
                        nondeceptive_agents.append(agent['agentid'])

                    # No need to process anything further for this agent.
                    raise Exception
        except Exception:
            pass

    num_agents = len(deceptive_agents) + len(nondeceptive_agents)

    if num_agents == 0:
        return NOT_APPLICABLE, NOT_APPLICABLE

    if len(nondeceptive_agents) == 0:
        p_nondeceptive = NOT_APPLICABLE
    else:
        p_nondeceptive = len(nondeceptive_agents) / num_agents

    if len(deceptive_agents) == 0:
        p_deceptive = NOT_APPLICABLE
    else:
        p_deceptive = len(deceptive_agents) / num_agents

    return [p_nondeceptive, p_deceptive]

# q(s,h)
def probability_speed_and_heading(i):
    position_2 = get_second_operand(i, position)

    heading = calculate_heading(position[i], position_2)
    distance = calculate_speed(position[i], position_2)

# s(t)
def suspiciousness(t):
    x, y = t[0], t[1]
    return k1 / (k1 + probability_in_region(x, y) * probability_speed_and_heading(t))

def noticeability(database, top_left, bottom_right):
    """Calculate noticeability of non-deceptive and deceptive agents in region.
    """
    def calculate_noticeability(p_agent):
        k3 = 1
        if p_agent == NOT_APPLICABLE:
            return p_agent
        if p_agent == 0:
            return 0
        return k3 / (k3 + p_agent)

    p_nondeceptive, p_deceptive = probability_in_region(database, top_left,
                                                        bottom_right)

    return [calculate_noticeability(p_nondeceptive),
            calculate_noticeability(p_deceptive)]

class Grid:
    # TODO: Calculating this number is another project in itself.
    num_divisions = 7

    def __init__(self, database):
        self._find_bounding_box(database)
        self._find_division_points()

    def _find_bounding_box(self, database):
        top_left = [min([position[0] for agent in database['agents'] for position in agent['positions']]),
                    max([position[1] for agent in database['agents'] for position in agent['positions']])]
        bottom_right = [max([position[0] for agent in database['agents'] for position in agent['positions']]),
                        min([position[1] for agent in database['agents'] for position in agent['positions']])]
        self.bounding_box = [top_left, bottom_right]

    def _find_division_points(self):
        self.divide = [abs(self.bounding_box[1][0] - self.bounding_box[0][0]) / self.num_divisions,
                       abs(self.bounding_box[1][1] - self.bounding_box[0][1]) / self.num_divisions]

    def calculate_regions(self, database):
        """Calculate top-left and bottom-right coordinates for each region.

        Start at top-left-most region and work down rows, start at the top for each
        new column.
        """
        regions = []
        for x in range(0, self.num_divisions):
            for y in range(0, self.num_divisions):
                top_left = [self.bounding_box[0][0] + (x * self.divide[0]),
                            self.bounding_box[0][1] - (y * self.divide[1])]
                bottom_right = [self.bounding_box[0][0] + ((x + 1) * self.divide[0]),
                                self.bounding_box[0][1] - ((y + 1) * self.divide[1])]
                regions.append([top_left, bottom_right])
        return regions

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Requires path to data file'
        sys.exit()

    # Only process regions in this list. Leave empty to process all regions.
    restrict_to_regions = [38]

    # Read in database of agents from Kinect.
    database = setup_database(sys.argv[1])

    # Set up bounding box around agent positions.
    grid = Grid(database)

    # Prepare all regions within bounding box.
    regions = grid.calculate_regions(database)

    print 'n(region) = [non-deceptive, deceptive]'
    print

    if len(restrict_to_regions) > 0:
        for region_num in restrict_to_regions:
            print 'Region', str(region_num),
            print noticeability(database, regions[region_num][0],
                                regions[region_num][1])
    else:
        for i, region in enumerate(regions):
            print 'Region', str(i),
            print noticeability(database, region[0], region[1])