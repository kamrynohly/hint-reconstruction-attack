# CS226r Final Project
# Code written by Kamryn Ohly and Joanna Boyland
# April 23, 2023

'''
The goal of this file is to properly format all of our information about
our current noisy database.

Formats our kway-marginal queries into proper formats for the rest of the code.

Works with queries outputted by the RAP algorithm (as detailed in paper).
'''

# normalizeQueries ——
#   Inputs our list of query results (floats) and the k value of our marginals.
#   Given our value of k, calls upon the correct function to order and 
#   output the correctly bounded queries. 

def normalizeQueries(q_list, k):
    if k == 1:
         return oneMarginalQueries(q_list)
    else:
        print("not yet implemented")


# oneMarginalQueries —— 
#   Inputs our list of queries specifically for 1-way marignals.
#   Since RAP outputs the probability of an attribute and its complement,
#   we want to make sure the addition of the probability p + (1-p) = 1.
#   If it does not, then we split the difference shared by their sum, and we
#   adjust the values accordingly. Lastly, we bound it by 0 and 1.
#   Outputs only the bounded probabilities p, not their complements.

def oneMarginalQueries(queries):
    finalProbs = []
    # Splits difference of complement and non-complement if over 1 or under 0
    for i in range(0, len(queries) - 1, 2):
        if (queries[i] + queries[i+1]) > 1 or (queries[i] + queries[i+1]) < 1:
            difference = 1 - (queries[i] + queries[i+1])
            queries[i] += difference / 2
            queries[i+1] += difference / 2 

    # Bounds by 0 and 1, only keeps the probability of being true
    for i in range(1, len(queries), 2):
        if queries[i] < 0:
            queries[i] = 0
        elif queries[i] > 1:
            queries[i] = 1
        finalProbs.append(queries[i])

    return finalProbs


# twoWayMarginalQueries —— 
#   Inputs our list of queries specifically for 2-way marignals.
#   Yet to be implemented.
#   Outputs only the bounded probabilities p, not their complements.

def twoWayMarginalQueries(queries):
    print()


# threeWayMarginalQueries —— 
#   Inputs our list of queries specifically for 3-way marignals.
#   Yet to be implemented.
#   Outputs only the bounded probabilities p, not their complements.

def threeWayMarginalQueries(queries):
    print()