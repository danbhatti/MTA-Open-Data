"""
Name: Daniel Bhatti
Date: 14 October 2024
Description: 

to run test quick: python3 main.py data/MTA_Subway_Stations_20241013.csv
"""

import contextily as ctx
import argparse
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString; import networkx as nx; import matplotlib.pyplot as plt
import graph
import networkx as nx
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def main():
    # Load the image you want to use for the points
    image = plt.imread('images/NYCS-bull-trans-6.svg.png') # image path
    # this code is used to extract the relevant data from the .csv file, using command line arguments
    args = parse_args()
    network = pd.read_csv(args.network_filename) # file path
    filtered_network = process_data(network)
    filtered_network['marker_size'] = filtered_network['Daytime Routes'].apply(
    lambda daytime_routes: 100 if ('6' in daytime_routes) else 10)

    # this code is used to instantiate a Network object, based on the relevant data parsed above
    network = graph.Network(filtered_network)
    # here we define geometry to be plotted
    geometry = [Point(xy) for xy in zip(filtered_network["GTFS Longitude"], 
                                        filtered_network["GTFS Latitude"])]
    # here we define point geometries to be plotted
    station_points = gpd.GeoDataFrame(filtered_network, geometry=geometry, crs = {'init': 'epsg:2263'})
    # here we initialize a graph to be filled in
    G = nx.Graph()
    # here we construct a graph based on the existing adjacency matrix
    for i in range(network.adjacency_matrix.shape[0]): 
        for j in range(i, network.adjacency_matrix.shape[1]): 
            if network.adjacency_matrix[i][j] == 1: 
                G.add_edge(i,j) 
    # Create a list to store LineString geometries (for edges)
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
    
    for idx, row in station_points.iterrows():
        x, y = row.geometry.x, row.geometry.y
        if row['marker_size'] == 100:  # Replace 'your_condition' with your actual condition to select points
            # Create an OffsetImage
            im = OffsetImage(image, zoom=0.008)  # Adjust zoom for size
            ab = AnnotationBbox(im, (x, y), frameon=False)  # Create an AnnotationBbox
            ax.add_artist(ab)  # Add the image to the axes
    

    # Optionally, you can customize the limits and titles
    ax.set_title("MTA CBD Subway Network")
    ax.set_xlabel("GTFS Longitude")
    ax.set_ylabel("GTFS Latitude")
    plt.savefig('figures/testfig2.png', dpi = 1000)
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