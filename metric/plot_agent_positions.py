# UNC Greensboro, CSC 593, Fall 2012
#
# By Andrei Nicholson
# Mentored by Dr. Shan Suthaharan
#
# TODO:
# - A Noticeability object is being created multiple times for heatmaps.

import matplotlib.cm as cm
import matplotlib.pyplot as pyplot
import sys

from RoweMetric.database import setup_database
from RoweMetric import globals, grid, noticeability, point

class OutputType:
    AGENT_POSITIONS = 1
    GRID_OVERLAY = 2
    GRID_WITH_RESULTS = 3
    HEATMAP = 4

def draw_grid_overlay(grid, show_noticeability):
    grid_alpha = 0.5

    left_most = grid.bounding_box[0].x
    right_most = grid.bounding_box[0].x + (grid.num_divisions * grid.divide.x)
    top_most = grid.bounding_box[0].y
    bottom_most = grid.bounding_box[0].y - (grid.num_divisions * grid.divide.y)

    for i in range(0, grid.num_divisions + 1):
        pyplot.plot([left_most, right_most],
                    [grid.bounding_box[0].y - (i * grid.divide.y),
                     grid.bounding_box[0].y - (i * grid.divide.y)],
                    'r--', alpha=grid_alpha)
        pyplot.plot([grid.bounding_box[0].x + (i * grid.divide.x),
                     grid.bounding_box[0].x + (i * grid.divide.x)],
                    [top_most, bottom_most],
                    'r--', alpha=grid_alpha)

    if show_noticeability:
        draw_noticeability_in_grid(database, grid)

def noticeability_for_regions(grid, database):
    area_of_region = grid.area_of_region()
    regions = grid.calculate_regions(database)
    n = noticeability.Noticeability(grid, database, regions)
    n_regions = []
    for region in regions:
        n_regions.append(n.calculate(region[0], region[1]))
    return n_regions

def draw_noticeability_in_grid(database, grid):
    n = noticeability_for_regions(grid, database)
    n_i = 0

    for x in range(0, grid.num_divisions):
        for y in range(0, grid.num_divisions):
            if (n[n_i][0] == globals.NOT_APPLICABLE and
                n[n_i][1] == globals.NOT_APPLICABLE):
                n_i += 1
                continue

            pyplot.text(grid.bounding_box[0].x + (x * grid.divide.x) + 0.025,
                        grid.bounding_box[0].y - (y * grid.divide.y) - 0.35,
                        str(n[n_i][0]) + '\n' + str(n[n_i][1]))
            n_i += 1

def plot_agent_positions(database, restrict_to_agents, output_type):
    if output_type == OutputType.GRID_OVERLAY:
        agent_alpha = 0.3
    else:
        agent_alpha = 1.0

    for agent in database['agents']:
        if (len(restrict_to_agents) > 0 and
            not agent['agentid'] in restrict_to_agents):
            continue
        pyplot.plot([position.x for position in agent['positions']],
                    [position.y for position in agent['positions']],
                    label=str(agent['agentid']),
                    alpha=agent_alpha)

def draw_plot(database, grid):
    # Agent IDs to plot. Left blank all agents will be plotted.
    restrict_to_agents = []

    if (output_type == OutputType.AGENT_POSITIONS or
        output_type == OutputType.GRID_OVERLAY):
        plot_agent_positions(database, restrict_to_agents, output_type)

    if output_type != OutputType.AGENT_POSITIONS:
        draw_grid_overlay(grid, (output_type == OutputType.GRID_WITH_RESULTS))
    else:
        pyplot.legend()

    pyplot.ylabel('y')
    pyplot.xlabel('x')
    pyplot.title('Agent positions')
    pyplot.show()

def draw_heatmap(database, grid):
    """Heatmap for noticeability.

    See: http://matplotlib.org/examples/pylab_examples/hexbin_demo.html
    """
    n = noticeability_for_regions(grid, database)

    # Replace all NOT_APPLICABLE with zero.
    # TODO: There's GOT to be a cleaner way!
    for i,x in enumerate(n):
        if n[i][0] == globals.NOT_APPLICABLE:
            n[i][0] = 0
        if n[i][1] == globals.NOT_APPLICABLE:
            n[i][1] = 0

    # Create a two-dimensional array to hold values for non-deceptive agent's
    # noticeability. Rearrange for a {(0,0),(0,1),(0,2)...} layout instead of
    # the region (top-to-bottom, left-to-right).
    #
    # TODO: This is upside down.
    data = []
    n_obj = noticeability.Noticeability(grid, database,
                                        grid.calculate_regions(database))

    for y in range(0, grid.num_divisions):
        row = []
        for x in range(0, grid.num_divisions):
            top_left = point.Point(grid.bounding_box[0].x + (x * grid.divide.x),
                                   grid.bounding_box[0].y - (y * grid.divide.y))
            bottom_right = point.Point(grid.bounding_box[0].x + ((x + 1) * grid.divide.x),
                                       grid.bounding_box[0].y - ((y + 1) * grid.divide.y))
            n = n_obj.calculate(top_left, bottom_right)
            if n[0] == globals.NOT_APPLICABLE:
                n[0] = 0
            if n[1] == globals.NOT_APPLICABLE:
                n[1] = 0

            row.append(n[1])
        data.append(row)

    # Swap color map for either BuGn or OrRd.

    fig = pyplot.figure()
    ax1 = fig.add_subplot(111)
    cmap = cm.get_cmap('OrRd', 10)
    ax1.imshow(data, interpolation='nearest', cmap=cmap)
    pyplot.show()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Requires path to data file'
        sys.exit()

    output_type = OutputType.HEATMAP

    database = setup_database(sys.argv[1])
    grid = grid.Grid(database)

    if output_type == OutputType.HEATMAP:
        draw_heatmap(database, grid)
    else:
        draw_plot(database, grid)