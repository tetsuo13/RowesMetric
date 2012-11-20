# UNC Greensboro, CSC 593, Fall 2012
#
# By Andrei Nicholson
# Mentored by Dr. Shan Suthaharan

from RoweMetric import point

import json

def setup_database(data_file_path):
    data_file = open(data_file_path).read()
    return convert_data(json.loads(data_file))

def convert_data(data):
    """Modifications to JSON file as loaded by Python
    """
    result = swap_position_arrays_for_points(data)
    return result

def swap_position_arrays_for_points(data):
    for i in xrange(len(data['agents'])):
        old_positions = data['agents'][i]['positions']
        data['agents'][i]['positions'] = []

        for position in old_positions:
            data['agents'][i]['positions'].append(point.Point(position[0],
                                                              position[1]))
    return data
