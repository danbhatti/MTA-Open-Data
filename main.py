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

    working_data.to_csv('data/CBD_MTA_Subway_Stations')
    a = working_graph.adjacency_matrix
    #print(working_graph)
    b = working_graph.dijkstra('33 St')
    print(b)


    
    geometry = [Point(xy) for xy in zip(working_data["GTFS Longitude"], 
                                        working_data["GTFS Latitude"])]
    
    station_points = gpd.GeoDataFrame(working_data, geometry=geometry, crs = {'init': 'epsg:2263'})

    G = nx.Graph()
    
    
    for j in range(working_graph.adjacency_matrix.shape[1]): 
        if working_graph.adjacency_matrix[77][j] == 1: 
            G.add_edge(77,j) 
  

    edges = []
    for edge in G.edges():
        point1 = geometry[edge[0]]
        point2 = geometry[edge[1]]
        edges.append(LineString([point1, point2]))
    # Create a GeoDataFrame for the edges
    edges_gdf = gpd.GeoDataFrame(geometry=edges, crs="EPSG:2263")
    # Plot nodes (station points) and edges (connections)
    fig, ax = plt.subplots()
    edges_gdf.plot(ax=ax, color='black', linewidth= 1, alpha=1)  # Plot edges
    station_points.plot(ax=ax, color='#0039A5', markersize=10, zorder=2)  # Plot nodes

    # Optionally, you can customize the limits and titles
    ax.set_title("MTA CBD Subway Network")
    ax.set_xlabel("GTFS Longitude")
    ax.set_ylabel("GTFS Latitude")
    plt.savefig('figures/testfig5.png', dpi = 1000)
    #plt.show()

    

def parse_args():
    """Parse command line arguments (build-graph files)."""
    parser = argparse.ArgumentParser(description='parsing command line arguments')
    parser.add_argument('network_filename', help='path to build-graph file')
    args = parser.parse_args()
    return args



def filter_data(data):
    refinement = data[data['CBD'] == True] # this filters for just stops in the CDB

    refinement = refinement[refinement['Stop Name'] != 'Lexington Av/59 St']
    refinement = refinement[refinement['Stop Name'] != '59 St']
    combined_stop1 = {'GTFS Stop ID': '', 'Station ID': '', 'Complex ID': '',
                      'Division': '', 'Line': '', 'Stop Name': 'Lexington Av/59 St -- 59 St',
                      'Borough': 'M', 'CBD': True, 'Daytime Routes': 'N R W 4 5 6',
                      'Structure': '', 'GTFS Latitude': f'{(40.76266+40.762526)/2}',
                      'GTFS Longitude': f'{(-73.967258-73.967967)/2}',
                      'North Direction Label': '', 'South Direction Label': '',
                      'ADA': '', 'ADA Northbound': '', 'ADA Southbound': '', 
                      'ADA Notes': '', 'Georeference': ''}
    refinement = refinement._append(combined_stop1, ignore_index=True)

    refinement = refinement[refinement['Stop Name'] != '59 St-Columbus Circle']
    combined_stop2 = {'GTFS Stop ID': '', 'Station ID': '', 'Complex ID': '',
                      'Division': '', 'Line': '', 'Stop Name': '59 St-Columbus Circle',
                      'Borough': 'M', 'CBD': True, 'Daytime Routes': 'A C B D 1',
                      'Structure': '', 'GTFS Latitude': f'{(40.768296+40.768247)/2}',
                      'GTFS Longitude': f'{(-73.981736-73.981929)/2}',
                      'North Direction Label': 'Uptown', 'South Direction Label': 'Downtown',
                      'ADA': '', 'ADA Northbound': '', 'ADA Southbound': '', 
                      'ADA Notes': '', 'Georeference': ''}
    refinement = refinement._append(combined_stop2, ignore_index=True)

    refinement = refinement[refinement['Stop Name'] != 'Grand Central-42 St']
    combined_stop3 = {'GTFS Stop ID': '', 'Station ID': '', 'Complex ID': '',
                      'Division': '', 'Line': '', 'Stop Name': 'Grand Central-42 St',
                      'Borough': 'M', 'CBD': True, 'Daytime Routes': '4 5 6 7 S',
                      'Structure': '', 'GTFS Latitude': f'{(40.751776+40.751431+40.752769)/3}',
                      'GTFS Longitude': f'{(-73.976848-73.976041-73.979189)/3}',
                      'North Direction Label': '', 'South Direction Label': '',
                      'ADA': '', 'ADA Northbound': '', 'ADA Southbound': '', 
                      'ADA Notes': '', 'Georeference': ''}
    refinement = refinement._append(combined_stop3, ignore_index=True)
    
    return refinement




def read_csv(filename):
    """Read .csv into graph format"""
    csv = np.loadtxt(filename, delimiter=  ',', dtype=str)
    return csv



if __name__ == "__main__":
    main()