"""
Name: Daniel Bhatti
Date: 14 October 2024
Description: 

to run test quick: python3 main.py data/MTA_Subway_Stations_20241013.csv
"""

import argparse
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point; import networkx as nx; import matplotlib.pyplot as plt
import graph
import networkx as nx

def main():
    args = parse_args()
    network_filename = args.network_filename
    network = pd.read_csv(network_filename)
    filtered_network = process_data(network)
    print(filtered_network)
    

    network = graph.Network(filtered_network)

    print(network.stations)
    print(network.lines)
    print(network.adjacency_matrix)

    # copied for demonstration
    """
    geometry = [Point(xy) for xy in zip(filtered_network["GTFS Longitude"], 
                                        filtered_network["GTFS Latitude"])]

    station_points = gpd.GeoDataFrame(filtered_network, geometry=geometry, crs = {'init': 'epsg:2263'})
    station_points.plot()
    plt.show()
    """
    # copied for demonstration
    G = nx.Graph()

    for i in range(network.adjacency_matrix.shape[0]): 
        for j in range(network.adjacency_matrix.shape[1]): 
            if network.adjacency_matrix[i][j] == 1: 
                G.add_edge(i,j) 

    nx.draw( G ) 
    plt.show()      



def parse_args():
    """Parse command line arguments (build-graph files)."""
    parser = argparse.ArgumentParser(description='parsing command line arguments')
    parser.add_argument('network_filename', help='path to build-graph file')
    args = parser.parse_args()
    return args



def process_data(data):
    refinement = data[data['CBD'] == True]
    #refinement = refinement[refinement['Daytime Routes'].str.contains('6')]
    return refinement



def read_csv(filename):
    """Read .csv into graph format"""
    csv = np.loadtxt(filename, delimiter=  ',', dtype=str)
    return csv



if __name__ == "__main__":
    main()