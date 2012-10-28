# UNC Greensboro, CSC 593, Fall 2012
#
# By Andrei Nicholson
# Mentored by Dr. Shan Suthaharan

import json

def setup_database(data_file_path):
    data_file = open(data_file_path).read()
    return json.loads(data_file)