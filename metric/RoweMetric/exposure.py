# UNC Greensboro, CSC 593, Fall 2012
#
# By Andrei Nicholson
# Mentored by Dr. Shan Suthaharan

# Make all divisions result in a float.
from __future__ import division

from RoweMetric import globals

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
                if (position.x >= top_left.x and position.x <= bottom_right.x and
                    position.y <= top_left.y and position.y >= bottom_right.y):
                    if agent['deceptive']:
                        deceptive_agents.append(agent['agentid'])
                    else:
                        nondeceptive_agents.append(agent['agentid'])

                    # No need to process anything further for this agent.
                    raise Exception
        except Exception:
            pass

    num_agents = len(deceptive_agents) + len(nondeceptive_agents)

    if len(nondeceptive_agents) == 0:
        p_nondeceptive = globals.NOT_APPLICABLE
    else:
        p_nondeceptive = len(nondeceptive_agents) / num_agents

    if len(deceptive_agents) == 0:
        p_deceptive = globals.NOT_APPLICABLE
    else:
        p_deceptive = len(deceptive_agents) / num_agents

    return [p_nondeceptive, p_deceptive]
