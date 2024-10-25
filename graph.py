"""
Name: Daniel Bhatti
Date: 10/14/24
Description: 
"""

import numpy as np
from statistics import mean

class Network:

    def __init__(self, data):
        """
        Description: Abstracts Network to an adjacency matrix with node and edges; graph is 
        represented as adjacency matrix;
        Inputs: nodes and edges, passed in as a dictionary with stations and their connections
        return:  
        """
        self.station_names = {}; self.daytime_routes = {}
        self.station_count = data.shape[0]
        for n in range(self.station_count):
            self.station_names[n] = data.iat[n,5]
            self.daytime_routes[n] = data.iat[n,10]
            
        # stations are considered adjacent if they share one or more lines between them
        self.adjacency_matrix = np.zeros((self.station_count, self.station_count), 
                                         dtype=int)
        for i in range(self.station_count):
            for j in range(self.station_count):
                if self.shares_element(self.daytime_routes[i], self.daytime_routes[j]):
                    self.adjacency_matrix[i][j] = 1


        
    def dijkstra(self, source_node):
        helper_bool_list = np.full(shape=self.station_count, fill_value=False)
        helper_dist_list = np.full(shape=self.station_count, fill_value=float('inf'))

        # matches the station name with its place in the adjacency matrix
        '''
        source_node = 0
        for i in range(self.station_count):
            if source_name == self.station_names[i]:
                source_node = i
                break
        '''

        curr_node = source_node # initializing the node traversal
        adjacency_list = self.adjacency_matrix[curr_node, :]
        helper_dist_list[curr_node] = 0 # the distance from the src node to itself is 0
        for i in range(self.station_count):
            helper_bool_list[curr_node] = True 
            for j in range(self.station_count):
                if ((helper_dist_list[curr_node] + adjacency_list[j] < 
                     helper_dist_list[j]) and adjacency_list[j] == 1):
                    helper_dist_list[j] = (helper_dist_list[curr_node] + 
                    adjacency_list[j])
            # update the current node
            min_value = float('inf')
            for k in range(self.station_count):
                # if the first neighbor hasn't been explored yet, make it the current node
                if adjacency_list[k] < min_value and helper_bool_list[k] == False:
                    min_value = adjacency_list[k]
                    curr_node = k
                    adjacency_list = self.adjacency_matrix[curr_node, :]
    
        return helper_dist_list
            
  

    
    ## taken from Google search labs Generative AI, Oct 15 2024
    def shares_element(self, str1, str2):
        str1 = str1.replace(" ", ""); str2 = str2.replace(" ", "")
        for char in str1:
            if char in str2:
                return True
        return False

     


        

        