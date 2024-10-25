"""
Name: Daniel Bhatti
Date: 14 October 2024
Description: 

to run test quick: python3 main.py data/MTA_Subway_Stations_and_Complexes_20241018.csv
"""

# imports 
import argparse
import folium
import numpy as np
import pandas as pd
import graph
import requests


def main():
    # this code is used to extract the relevant data from the .csv file, using command line arguments
    # example of making an API request using the app token
    # https://data.seattle.gov/resource/kzjm-xkqj.json?$$app_token=APP_TOKEN
    results = requests.get('https://data.ny.gov/resource/5f5g-n3cz.json?$$app_token=5cNQYqwwGoXLCZfec7e7kJXEk').json()
    results_df = pd.DataFrame.from_records(results)
    results_graph = graph.Network(results_df)
    shortest_paths = results_graph.dijkstra('33 St')
    plot_interactive_map(results_df, shortest_paths)



def plot_interactive_map(working_data, shortest_paths):
    # create a base map centered around NYC
    map_center = [40.776676, -73.971321]
    subway_map = folium.Map(location=map_center, zoom_start=12)

    for i in range(len(shortest_paths)):
        station_color = get_station_color(shortest_paths[i])
        folium.CircleMarker(
            location=(working_data.iloc[i,12], working_data.iloc[i,13]),
            radius=6,
            color=station_color,
            fill=True,
            fill_opacity=0.7,
            #tooltip=f"Display Name: {working_data.iloc[i,4]}"
        ).add_to(subway_map)
        ''''
        folium.Marker(
            location=(working_data.iloc[i,12], working_data.iloc[i,13]),
            popup=f"Display Name: {working_data.iloc[i,4]}",
            icon=folium.Icon(color="blue"),
        ).add_to(subway_map).add_child(folium.ClickForMarker())
        '''
    # save the map as an HTML file
    subway_map.save('subway_map.html')
        


def get_station_color(distance):
    if distance == 0:
        return 'black'
    elif distance == 1:
        return 'green'
    elif distance == 2:
        return 'yellow'
    elif distance == 3:
        return 'red'
    return '#0039A6'  # Default color

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