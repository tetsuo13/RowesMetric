# Exposure of deceptive agent D is E = (1 / T) \sum_{t = 0}^{T - 1} s(t) \sum_{i = 0}^{N} v(i,t)n(i,t) (eq. 2)
#
# v(i,t) = visibility at time t from non-deceptive agent i
# p(x,y) = probability, agent at the location (x,y)
# q(s,h) = probability, speed and heading
# p(x,y)q(s,h) = joint probability, particular location with a particular velocity vector
# s(t) = k_1 / (k_1 + p(x,y)q(s,h)) (eq. 3) (scale of 0 to 1)
# n(i,t) = noticeability at time t by agent i (scale of 0 to 1)
# n(i,t) = k_3 / (k_3 + p(x,y))

# Look through positions_seen for other (x,y) locations (with buffer?). The
# return value of the proabability functions is
#
#    (how many times this (x,y) has been observed before) / (total positions)
#

# Make all divisions result in a float.
from __future__ import division

import math

k1 = 0.5
k2 = 0.5
k3 = 0.5

# Number of decimal places to round up to. The lower the number, the greater the
# radius distance used.
probability_position_fuzziness = 2

database = []

# TODO: This isn't needed anymore since agents are examined after the fact.
# numpy.random.normal(0, 0.01, 10)
position = [[-0.01348549, -0.01467225],
            [-0.00189697,  0.00013569],
            [-0.00701047, -0.00664975],
            [-0.00081589, -0.00820052],
            [0.01753263,  -0.00199792]]

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


# TODO Database setup would already be prepared in another file.
class Agent:
    def __init__(self):
        self.deceptive = False
        self.positions = []
        self.speed = []
        self.heading = []

def setup_database(database):
    # a = numpy.random.normal(0, 0.1, 100)
    # for x, y in zip(a[0::2], a[1::2]):
    #     print '                  [' + str(x) + ', ' + str(y) + '],'
    positions_seen = [
                  [-0.102098628079, 0.110380981553],
                  [0.018495508781, -0.0801123647528],
                  [0.147101106791, -0.0303106724728],
                  [0.0676519321694, -0.00480810026339],
                  [0.103104419449, -0.00043651770435],
                  [-0.149469855549, -0.0420311089685],
                  [0.0171384435492, -0.0975112455155],
                  [-0.160411038513, 0.194925599953],
                  [-0.16242176424, 0.144707501756],
                  [-0.00775144755656, -0.098695925373],
                  [0.00807577498014, -0.177658284725],
                  [-0.0335387416831, 0.121143074622],
                  [0.104670920682, -0.0699832571838],
                  [0.140720459516, -0.0608093543972],
                  [-0.0590386467093, -0.294562834951],
                  [0.0633177469597, -0.0742621998989],
                  [-0.0819459093389, 0.19077437448],
                  [0.140322480578, -0.0219890476701],
                  [-0.154280743353, -0.136695486856],
                  [-0.0173559690594, -0.0235483900248],
                  [-0.0403699777297, -0.11194360469],
                  [0.142442627996, -0.0123096446595],
                  [0.0881228361698, -0.238560377364],
                  [-0.0755489354367, -0.0424385663405],
                  [0.0445971195997, -0.0788612047126],
                  [0.00964036842383, 0.0861473752564],
                  [0.0287306237761, -0.00113821264517],
                  [0.0630724719901, -0.101145751863],
                  [0.159730079399, -0.177854146832],
                  [0.134841882905, -0.0165206486406],
                  [-0.133394815106, 0.0428460491285],
                  [0.00643928765595, -0.249228556957],
                  [0.0237013005348, 0.0978624503835],
                  [-0.220722889458, -0.00256225516929],
                  [-0.0324835161762, 0.0481835642114],
                  [0.100773933052, 0.0782765748984],
                  [-0.0473111141612, -0.146515301474],
                  [-0.065837993008, -0.0550025964186],
                  [-0.0832449662036, 0.104557449817],
                  [0.0958485841677, 0.173231614786],
                  [0.0825917439165, -0.0497821545913],
                  [-0.0834994835729, 0.0262309138613],
                  [-0.0553815376055, -0.0507607084724],
                  [-0.162541911531, -0.117906331355],
                  [0.0437939539569, 0.0352065314434],
                  [-0.237848589751, 0.175802152767],
                  [-0.00745319489838, -0.00657056367522],
                  [-0.0254129370397, 0.113091498392],
                  [-0.105432324507, -0.0246565384319],
                  [0.106552115162, 0.0782577449698]
    ]

    num_agents = 2

    positions = []
    speed = []
    heading = []

    for i, p in enumerate(positions_seen):
        p_2 = get_second_operand(i, positions_seen)

        positions.append(p)
        speed.append(calculate_speed(p, p_2))
        heading.append(calculate_heading(p, p_2))

        if (i + 1) % (len(positions_seen) / num_agents) == 0:
            agent = Agent()
            agent.positions = positions
            agent.speed = speed
            agent.heading = heading

            database.append(agent)

            positions = []
            speed = []
            heading = []

# p(x,y)
def probability_at_location(needle_agent, x, y):
    x = round(x, probability_position_fuzziness)
    y = round(y, probability_position_fuzziness)
    encountered = 0
    total_positions = 0

    for i, agent in enumerate(database):
        # Skip examining current agent since it'll be a 100% probability match.
        if i == needle_agent:
            continue

        for p in agent.positions:
            total_positions += 1

            if (round(p[0], probability_position_fuzziness) == x or
                round(p[1], probability_position_fuzziness) == x or
                round(p[0], probability_position_fuzziness) == y or
                round(p[1], probability_position_fuzziness) == y):
                encountered += 1

    #print 'probability_at_location(' + str(x) + ', ' + str(y) + '): ' + str(encountered) + ', ' + str(encountered / len(positions_seen))

    return encountered / total_positions

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
def noticeability(agent_num, position):
    x, y = position[0], position[1]
    return k3 / (k3 + probability_at_location(agent_num, x, y))


setup_database(database)

# Find largest time interval recorded.
T = max([len(x.positions) for x in database])

# Number of agents.
N = len(database)

print 'Time'.ljust(7), '|',
for i in range(1, N + 1):
    print ('Path ' + str(i)).ljust(7), '|',
print

for t in range(0, T):
    print str(t).ljust(7), '|',

    for i in range(0, N):
        print str(round(noticeability(i, database[i].positions[t]), 4)).ljust(7), '|',

    print
