"""
Name: Daniel Bhatti
Date: 10/14/24
Description: 
"""

import numpy as np
import heapq

class Network:

    def __init__(self, data):
        """
        Description: Abstracts Network to an adjacency matrix with node and edges; graph is represented as adjacency matrix;
        Inputs: nodes and edges, passed in as a dictionary with stations and their connections
        return:  
        """
        self.station_names = {}; self.daytime_routes = {}
        station_count = data.shape[0]
        for n in range(station_count):
            self.station_names[n] = data.iat[n,5]
            self.daytime_routes[n] = data.iat[n,8]
            
        # stations are considered adjacent if they share one or more lines between them
        self.adjacency_matrix = np.zeros((station_count, station_count), dtype=int)
        for i in range(station_count):
            for j in range(station_count):
                if self.shares_element(self.daytime_routes[i], self.daytime_routes[j]):
                    self.adjacency_matrix[i][j] = 1

        # distance matrix to do djistras algorithm
        self.distance_matrix = np.full((station_count, station_count), 100, dtype=int)
        for k in range(station_count):
            if self.adjacency_matrix[0][k] == 1: # always evaluates to false :(
                self.distance_matrix[0][k] == 1
            else:
                self.distance_matrix[0][k] == 100
        self.distance_matrix[0][0] = 0

        ind_explored = np.full(station_count, False)
        ind_explored[0] = True

        while False in ind_explored:
            min_value = min(self.distance_matrix[0])
            print('p')





    
    ## taken from Google search labs Generative AI, Oct 15 2024
    def shares_element(self, str1, str2):
        str1 = str1.replace(" ", ""); str2 = str2.replace(" ", "")
        for char in str1:
            if char in str2:
                return True
        return False

     


        

        