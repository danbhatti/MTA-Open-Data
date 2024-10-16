"""
Name: Daniel Bhatti
Date: 14 October 2024
Description: 

to run test quick: python3 main.py data/MTA_Subway_Stations_20241013.csv
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

    geometry = [Point(xy) for xy in zip(working_data["GTFS Longitude"], 
                                        working_data["GTFS Latitude"])]
    
    station_points = gpd.GeoDataFrame(working_data, geometry=geometry, crs = {'init': 'epsg:2263'})

    G = nx.Graph()
    
    for i in range(working_graph.adjacency_matrix.shape[0]): 
        for j in range(i, working_graph.adjacency_matrix.shape[1]): 
            if working_graph.adjacency_matrix[i][j] == 1: 
                G.add_edge(i,j) 
  

    edges = []
    for edge in G.edges():
        point1 = geometry[edge[0]]
        point2 = geometry[edge[1]]
        edges.append(LineString([point1, point2]))
    # Create a GeoDataFrame for the edges
    edges_gdf = gpd.GeoDataFrame(geometry=edges, crs="EPSG:2263")
    # Plot nodes (station points) and edges (connections)
    fig, ax = plt.subplots()
    edges_gdf.plot(ax=ax, color='black', linewidth= 0.3, alpha=0.3)  # Plot edges
    station_points.plot(ax=ax, color='#0039A5', markersize=10, zorder=2)  # Plot nodes

    # Optionally, you can customize the limits and titles
    ax.set_title("MTA CBD Subway Network")
    ax.set_xlabel("GTFS Longitude")
    ax.set_ylabel("GTFS Latitude")
    plt.savefig('figures/testfig3.png', dpi = 1000)
    plt.show()

    print(working_graph.adjacency_matrix)
    print(working_graph.distance_matrix)

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