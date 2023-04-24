# CS226r Final Project
# Code written by Kamryn Ohly and Joanna Boyland
# April 23, 2023

import numpy as np


# reconstruct —— 
#   Inputs the following:
#       candidates  ——  all possible datasets
#       domain      ——  domain of dataset we aim to reconstruct
#       queries     ——  list of query results properly bounded by 0 and 1
#       hint_dict   ——  empty or non-empty dictionary with accurate query
#       k           ——  type of marginals we are working with (k-way marginal)
#       invariant   ——  boolean value; if true, then there exists a customized
#                       invariant, if false, then do not call the invariant function.
#   Chooses the appropriate function depending on the k-way marginal.
#   If the adversary wants to apply invariants, can choose to do so.
#   Outputs the result of a function to determine the ideal candidate given
#   all of the info we have about our dataset.

def reconstruct(candidates, domain, queries, hint_dict, k, invariant):
    if k == 1:
        if invariant:
            valid_candidates = applyInvariants(candidates, domain)
            return reconstructDB(valid_candidates, domain, queries, hint_dict)
        else:
            return reconstructDB(candidates, domain, queries, hint_dict)
    else:
        print("not implemented yet")


# applyInvariants —— CUSTOMIZABLE
#   Inputs our candidates and domain of our dataset.
#   You decide what invariants the dataset holds.
#       Examples:
#           (1) each attribute is mutually exclusive        (CURRENTLY DONE)
#           (2) must have a certain number of 1s per row
#           (3) must add to a certain value
#           (4) must respect ... (some other condition)
#   Outputs the remaining valid candidates.

# START: YOU EDIT THIS FUNCTION

def applyInvariants(candidates, domain):
    # In our "simple" example, every attribute is mutually exclusive.
    # We will reduce our candidates by adding this exclusivity.
    c_length = len(candidates)
    ci_length = len(candidates[0])
    domain_length = len(domain)

    valid_candidates = []

    for i in range(c_length):
        isGood = True
        for j in range(ci_length):
            count = 0
            # Make sure each row only has 1 selected 
            #   (can't be a TF if you're a student, can't be a student if Prof)
            for val in range(domain_length):
                if candidates[i][j][val] == 1:
                    count += 1
            if count != 1:
                isGood = False 
                break
        if isGood:
            valid_candidates.append(candidates[i])
    
    return valid_candidates

# END: YOU EDIT THIS FUNCTION


# reconstructDB —— 
#   Inputs almost identical values as reconstruct() (see above). 
#   For one-way marginals.
#   How 
#   Outputs the best candidate.

def reconstructDB(candidates, domain, queries, hint_dict):
    domain_size = len(domain)
    c_size = len(candidates)
    ci_size = len(candidates[0])

    minValue = float('inf')
    minIndex = -1

    # Look at each possible candidate
    for i in range(len(candidates)):
        
        # Start by getting probability ratios of each value
        vals = np.zeros(domain_size)
        for k in range(domain_size):
            # Start with count of 1s in database for that attribute
            vals[k] = 0
            for j in range(ci_size):
                if candidates[i][j][k] == 1:
                    vals[k] += 1
            # Calculate probability
            vals[k] /= ci_size

        # Make our hint dictionary into list relative to our queries
        f_hint = np.arange(len(queries))
        f_hint.fill(-1)
        for key in hint_dict:
            if key < len(queries):
                f_hint[int(key)] = int(hint_dict[key])

        # Now, we want to calculate the "score" of our given candidate.
        #   A lower score indicates that the dataset is closest to our
        #   current queries values, and that it upholds our hints.
        #   We utilize our loss function to uphold our invariants / hints.
        c_score = getScore(list(vals), queries, 0, f_hint)
        if c_score < minValue:
            minValue = c_score
            minIndex = i
        
    return candidates[minIndex]

# functionName —— 
#   Inputs  
#   How 
#   Outputs 

def getScore(currProbs, queryProbs, err, hint):
    differences = 0
    for i in range(len(currProbs)):
        if hint[i] == -1:
            differences += abs(currProbs[i] - queryProbs[i])
        else:
            differences += abs(currProbs[i] - queryProbs[i]) + loss(currProbs[i], 0.1)

    return differences

# functionName —— 
#   Inputs  
#   How 
#   Outputs 

def loss(q_i, hint):
    if q_i != hint:
        return 1000
    else:
        return 0