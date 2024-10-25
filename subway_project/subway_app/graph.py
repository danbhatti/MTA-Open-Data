"""
Name: Daniel Bhatti
Date: 10/14/24
Description: This class represents a graph as an adjacency matrix 
and has useful methods for analysis, such as dijistra's algorithm
"""

import numpy as np
import folium 

class Network:

    def __init__(self, data):
        """
        This constructor represents a Network as an adjacency 
        matrix 
        """
        # This code block reads in data from the 
        # MTA_Subway_Stations_and_Complexes file
        self.station_names = {}; self.daytime_routes = {}
        self.station_count = data.shape[0]
        for n in range(self.station_count):
            self.station_names[n] = data.iat[n,5]
            self.daytime_routes[n] = data.iat[n,10]
        self.graph = self.build_graph(data)

    def build_graph(self):
        """
        This code block is used to construct the adjacency matrix
        stations are considered adjacent if they share one or 
        more lines between them
        """
        self.adjacency_matrix = np.zeros((self.station_count, 
                                          self.station_count), 
                                          dtype=int)
        for i in range(self.station_count):
            for j in range(self.station_count):
                if shares_element(self.daytime_routes[i], 
                                       self.daytime_routes[j]):
                    self.adjacency_matrix[i][j] = 1


        
    def dijkstra(self, source_name):
        """
        This method, given a source node's name, runs dijkstra's 
        algorithm on the adjacency matrix from that node and returns 
        the shortest paths in the form of a list
        """
        # these initialized values will help us with dijkstras
        source_node = 0
        helper_bool_list = np.full(shape=self.station_count, 
                                   fill_value=False)
        shortest_paths = np.full(shape=self.station_count, 
                                   fill_value=float('inf'))
        # matches the station name with its place in the adjacency 
        # matrix
        for i in range(self.station_count):
            if source_name == self.station_names[i]:
                source_node = i
                break
        # this code block computes djikstra's on all of the nodes 
        # in the graph
        curr_node = source_node # initializing the node traversal
        adjacency_list = self.adjacency_matrix[curr_node, :]
        shortest_paths[curr_node] = 0 # the distance from the src 
        #node to itself is 0
        for i in range(self.station_count):
            helper_bool_list[curr_node] = True 
            for j in range(self.station_count):
                if ((shortest_paths[curr_node] + adjacency_list[j] < 
                     shortest_paths[j]) and 
                    adjacency_list[j] == 1):
                    shortest_paths[j] = (shortest_paths[curr_node] + 
                                           adjacency_list[j])
            # update the current node
            min_value = float('inf')
            for k in range(self.station_count):
                # if the first neighbor hasn't been explored yet, 
                # make it the current node
                if (adjacency_list[k] < min_value and 
                    helper_bool_list[k] == False):
                    min_value = adjacency_list[k]
                    curr_node = k
                    adjacency_list = self.adjacency_matrix[curr_node, :]
        # return shortest paths to each node
        return shortest_paths
                


    def plot_interactive_map(self, shortest_paths):
        # Create a base map centered around NYC
        map_center = [self.data['Latitude'].mean(), 
                      self.data['Longitude'].mean()]
        subway_map = folium.Map(location=map_center, zoom_start=12)

        for i in range(len(shortest_paths)):
            station_color = get_station_color(shortest_paths[i])
            folium.CircleMarker(
                location=(self.data.iloc[i,12], self.data.iloc[i,13]),
                radius=6,
                color=station_color,
                fill=True,
                fill_opacity=0.7,
                #tooltip=f"Display Name: {working_data.iloc[i,4]}"
            ).add_to(subway_map)
            folium.Marker(
                location=(self.data.iloc[i,12], self.data.iloc[i,13]),
                popup=f"Display Name: {self.data.iloc[i,4]}",
                icon=folium.Icon(color="blue"),
            ).add_to(subway_map).add_child(folium.ClickForMarker())


### HELPER METHODS

def filter_data(data):
    '''
    this helper method filters for just stops in the CDB
    '''
    return data[data['CBD'] == True]     
   


def load_station_data(filename):
    '''
    this helper method converts data from csv format and filters
    '''
    df = np.loadtxt(filename, delimiter=  ',', dtype=str)
    return filter_data(df)

    
    
def shares_element(self, str1, str2):
    '''
    taken from Google search labs Generative AI, Oct 15 2024
    '''
    str1 = str1.replace(" ", ""); str2 = str2.replace(" ", "")
    for char in str1:
        if char in str2:
            return True
    return False
    
def get_station_color(distance):
    '''
    this helper method colors the points based on their distance
    from the source node based on dijistra's algorithm
    '''
    if distance == 0:
        return 'black'
    elif distance == 1:
        return 'green'
    elif distance == 2:
        return 'yellow'
    elif distance == 3:
        return 'red'
    return '#0039A6'  # Default color

     


        

        