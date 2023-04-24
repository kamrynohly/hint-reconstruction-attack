# CS226r Final Project
# Code written by Kamryn Ohly and Joanna Boyland
# April 23, 2023

import numpy as np
from itertools import combinations_with_replacement, permutations

'''

The goal of this file is to generate all possible candidates for our specific
example given its domain.

Currently, this method is an exponential method to ensure accuracy. This
greatly restricts the size of our reconstruction.

We discuss optimizations of this step within our paper. 

'''

# generateCandidates —— 
#   Inputs the domain of the given dataset and well as the desired size
#   (number of rows) for our reconstructed table.
#   Begins by taking our domain and determining all possible combinations for
#   a singular row. Then, takes all of those combinations, and gets all possible
#   combinations of datasets with our domain and size.
#   Outputs all possible datasets (a list of lists of lists).

def generateCandidates(domain, size):
    row_combinations = parseDomain(domain)
    candidates = getAllCandidates(row_combinations, size)
    return candidates

# parseDomain —— 
#   Inputs the domain of the dataset we are currently working with. 
#   Generates the possibilities for a single row of data. For example,
#   a domain with two attributes can be [0,0], [0,1], [1,0], [1,1].
#   Outputs all possible combinations for a single row of data.

def parseDomain(domain):
    # Get number of attributes we have, aka values in a single row of data.
    attributeNum = len(domain)
    # Creates a starting point for our combinations to be created.
    start = np.zeros(attributeNum)
    start[0] = 1
    # Generates all possible combinations of values of a single row of data.
    return getAllCandidates(start, attributeNum)

# getAllCandidates —— 
#   Inputs the following:
#       domain  ——  a list of all possibilities for a single row on our domain
#       size    ——  the desired size of our reconstruction (number of rows)
#   Calculates all possible datasets that could be created by using combinatorics.
#   Outputs all possible candidate datasets.

def getAllCandidates(domain, size):
    # Store all possible permutations and combinations.
    options = []
    options += list(combinations_with_replacement(domain, size))
    options += list(permutations(domain, size))

    # Making each element a list instead of a tuple
    for i in range(0, len(options)):            
        options[i] = list(options[i])

    # Reduces copies of the same dataset / discards repetitions
    result = []
    [result.append(val) for val in options if val not in result]  
    
    return result