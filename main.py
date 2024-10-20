"""
Name: Daniel Bhatti
Date: 14 October 2024
Description: 

to run test quick: python3 main.py data/MTA_Subway_Stations_and_Complexes_20241018.csv
"""

# imports 
import argparse
import numpy as np
import pandas as pd
import graph
import networkx as nx
from shapely.geometry import Point, LineString
import geopandas as gpd
import matplotlib.pyplot as plt

def main():
    # this code is used to extract the relevant data from the .csv file, using command line arguments
    args = parse_args()
    network_data = args.network_filename
    df = pd.read_csv(network_data)
    working_data = filter_data(df) # filters data based on filter_data method
    working_graph = graph.Network(working_data)
    working_data.to_csv('data/CBD_MTA_Subway_Stations')
    b = working_graph.dijkstra('33 St')
    print(b)

    
    geometry = [Point(xy) for xy in zip(working_data["Longitude"], 
                                        working_data["Latitude"])]
    
    station_points = gpd.GeoDataFrame(working_data, geometry=geometry, crs = {'init': 'epsg:2263'})
    station_points['color'] = 'blue'
    print(station_points.iloc[0,17])
    for i in range(len(station_points)):
        if b[i] == 0:
            station_points.iloc[i,17] = 'black'
        elif b[i] == 1:
            station_points.iloc[i,17] = 'green'
        elif b[i] == 2:
            station_points.iloc[i,17] = 'yellow'
        elif b[i] == 3:
            station_points.iloc[i,17] = 'red'
        


    # Plot nodes (station points) 
    fig, ax = plt.subplots()
    station_points.plot(ax=ax, marker ='o', edgecolor = 'black', color = station_points['color'])  # Plot nodes

    # Optionally, you can customize the limits and titles
    ax.set_title("MTA CBD Subway Network")
    ax.set_xlabel("GTFS Longitude")
    ax.set_ylabel("GTFS Latitude")
    plt.savefig('figures/testfig6.png', dpi = 1000)
    #plt.show()

    

def parse_args():
    """Parse command line arguments (build-graph files)."""
    parser = argparse.ArgumentParser(description='parsing command line arguments')
    parser.add_argument('network_filename', help='path to build-graph file')
    args = parser.parse_args()
    return args



def filter_data(data):
    refinement = data[data['CBD'] == True] # this filters for just stops in the CDB    
    return refinement




def read_csv(filename):
    """Read .csv into graph format"""
    csv = np.loadtxt(filename, delimiter=  ',', dtype=str)
    return csv



if __name__ == "__main__":
    main()