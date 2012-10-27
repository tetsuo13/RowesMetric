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
k3 = 0.25

# Radius to map around a position. Other agent position's are then checked to be
# within bounds.
probability_position_radius = 0.05

database = []

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
def probability_at_location(current_agent, x, y):
    """Calculate the probability of other agents being at a location.

    The probability is done by using a radius search around the given position
    against all available positions for all other agents. Final result is how
    many other agents are within the radius.
    """

    def within_radius(center_x, center_y, radius, x, y):
        """Whether a point is within a circle.
        """
        square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
        return square_dist <= radius ** 2

    # Number of times another agent was found within this radius.
    encountered = 0

    for i, agent in enumerate(database['agents']):
        # Skip examining current agent since it'll be a 100% probability match.
        if agent['agentid'] == current_agent['agentid']:
            continue

        for position in agent['positions']:
            if within_radius(x, y, probability_position_radius, position[0],
                             position[1]):
                encountered += 1

    try:
        return 1 / encountered
    except ZeroDivisionError:
        return 1

# q(s,h)
def probability_speed_and_heading(i):
    position_2 = get_second_operand(i, position)

    heading = calculate_heading(position[i], position_2)
    distance = calculate_speed(position[i], position_2)

# s(t)
def suspiciousness(t):
    x, y = t[0], t[1]
    return k1 / (k1 + probability_at_location(x, y) * probability_speed_and_heading(t))

# n(i,t)
#def noticeability(agent_num, position):
def noticeability(database, top_left, bottom_right):
    """Calculate noticeability of non-deceptive agents in rectangle.
    """
    # Find the agents who have paths crossing into this region.
    # Note if any of those agents are deceptive.
    # If deceptive, use inverse probability.
    # Return noticeability.
    x, y = agent['positions'][t][0], agent['positions'][t][1]
    return k3 / (k3 + probability_at_location(agent, x, y))

class Grid:
    num_divisions = 7

    def __init__(self, database):
        self.find_bounding_box(database)
        self.find_division_points()

    def find_bounding_box(self, database):
        top_left = [min([position[0] for agent in database['agents'] for position in agent['positions']]),
                    max([position[1] for agent in database['agents'] for position in agent['positions']])]
        bottom_right = [max([position[0] for agent in database['agents'] for position in agent['positions']]),
                        min([position[1] for agent in database['agents'] for position in agent['positions']])]
        self.bounding_box = [top_left, bottom_right]

    def find_division_points(self):
        self.divide = [abs(self.bounding_box[1][0] - self.bounding_box[0][0]) / self.num_divisions,
                       abs(self.bounding_box[1][1] - self.bounding_box[0][1]) / self.num_divisions]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Requires path to data file'
        sys.exit()

    database = setup_database(sys.argv[1])

    grid = Grid(database)
    #print grid.bounding_box
    #print grid.divide

    top_left = grid.bounding_box[0]
    bottom_right = [grid.bounding_box[0][0] + grid.divide[0], grid.bounding_box[0][1] - grid.divide[1]]
    print top_left
    print bottom_right
    sys.exit()
    print noticeability(database, top_left, bottom_right)

    for i in range(0, grid.num_divisions + 1):
        print grid.bounding_box[0][0] + (i * grid.divide[0])

    sys.exit()

    # Find largest time interval recorded.
    T = max([len(agent['positions']) for agent in database['agents']])

    # Number of agents.
    N = len(database['agents'])

    for t in range(0, 25):
        print t, noticeability(agent, t)

    sys.exit()


    print 'Time'.ljust(7), '|',
    for i in range(1, N + 1):
        print ('Path ' + str(i)).ljust(7), '|',
    print

    for t in range(0, T):
        print str(t).ljust(7), '|',

        for i in range(0, N):
            print str(round(noticeability(i, database[i].positions[t]), 4)).ljust(7), '|',

        print
