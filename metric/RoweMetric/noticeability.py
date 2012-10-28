# UNC Greensboro, CSC 593, Fall 2012
#
# By Andrei Nicholson
# Mentored by Dr. Shan Suthaharan

NOT_APPLICABLE = '--'

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

def do_noticeability(database, top_left, bottom_right):
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