"""
Name: Daniel Bhatti
Date: 14 October 2024
Description: 

to run test quick: python3 main.py data/MTA_Subway_Stations_20241013.csv
"""

import argparse
import numpy as np
import pandas as pd

def main():
    args = parse_args()
    network_filename = args.network_filename
    network = pd.read_csv(network_filename)
    print(process_data(network))
    
    

def parse_args():
    """Parse command line arguments (build-graph files)."""
    parser = argparse.ArgumentParser(description='parsing command line arguments')
    parser.add_argument('network_filename', help='path to build-graph file')
    args = parser.parse_args()
    return args


def process_data(data):
    data[data['CBD'] == True]
    return data

def read_csv(filename):
    """Read .csv into graph format"""
    csv = np.loadtxt(filename, delimiter=  ',', dtype=str)
    return csv



if __name__ == "__main__":
    main()