"""
Name: Daniel Bhatti
Date: 10/14/24
Description: 
"""

import numpy as np

class Network:

    def __init__(self, data):
        """
        Description: Abstracts Network to an adjacency matrix with node and edges; graph is represented as adjacency matrix;
        Inputs: nodes and edges, passed in as a dictionary with stations and their connections
        return:  
        """
        self.stations = {}; self.lines = {}
        for n in range(data.shape[0]):
            self.stations[n] = data.iat[n,5]
            self.lines[n] = data.iat[n,8]
            
        # stations are considered adjacent if they share one or more lines between them
        self.adjacency_matrix = np.zeros((len(self.stations), len(self.stations)))
        for i in range(len(self.stations)):
            for j in range(len(self.stations)):
                if self.shares_element(self.lines[i], self.lines[j]):
                    self.adjacency_matrix[i][j] = 1


    def min_spanning_tree(self, node_a, node_b):
        pass

    ## taken from Google search labs Generative AI, Oct 15 2024
    def shares_element(self, str1, str2):
        for char in str1:
            if char in str2:
                return True
        return False

     


        

        