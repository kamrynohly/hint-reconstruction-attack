# CS226r Final Project
# Code written by Kamryn Ohly and Joanna Boyland
# April 23, 2023

# Public libraries
import numpy as np
import sys
import json
import csv

# Our files
from formatNoisyQueries import normalizeQueries
from generateCandidates import generateCandidates
from reconstruct import reconstruct

# main()
#   USAGE: python3 main.py size domain kVal results 
#   Takes as input the following:
#       size             the size of the database we hope to reconstruct
#       binary-domain    json file with domain of the database, must be binary
#       kVal             what marginals we are working with
#       results          csv file with noisy query results of kVal-way marginals
#   Calls upon helper functions to take our noisy query results and reconstruct
#   our database. We can enhance our reconstruction through the usage of hints,
#   which can be manually added as explained in our paper.

def main():

    # Validate our command-line argument inputs
    if len(sys.argv) != 5:
        print("USAGE: python3 main.py size domain kVal results")
        sys.exit(1)
    elif not int(sys.argv[1]):
        print("Size inputted must be integer.")
        sys.exit(1)
    elif not int(sys.argv[3]):
        print("Size inputted must be integer.")
        sys.exit(1)
    
    
    # Save our values
    size = int(sys.argv[1])
    kVal = int(sys.argv[3])


    # Get our domain and read as dictionary
    with open(sys.argv[2],"r") as domainFile:
        jsonDomain = domainFile.readlines()
    domain = json.loads(jsonDomain[0])
    domain_keys = list(domain.keys())
    print("INFO: domain is the following:", domain)
    print()


    # Get our results (our noisy queries) and read as list
    #     Occurs before queries are reformatted.
    noisy_queries = []
    with open(sys.argv[4], mode='r') as resultFile:
        queries = csv.DictReader(resultFile)
        for query in queries:
            for value in query:
                noisy_queries.append(float(query[value]))

    # Now, let's format our queries in the easiest way to use them.
    #   This change will take queries and normalize them / throw out their complements.
    #   By "normalize" we guarantee that they are between 0 and 1, as
    #   they are probabilities.
    q_values = normalizeQueries(noisy_queries, kVal)

    print("INFO: normalized noisy queries to the following:")
    if kVal == 1:
        i = 0
        for key in domain_keys:
            print(f"Attribute - {key} - is 1 with probability {q_values[i]}")
            i += 1
    else:
        print("not yet implemented")
    print()


    # Next, we want to construct all possible databases that could be created
    #   with our specific domain. We will later narrow down these candidates.
    #   WARNING: an exponential implementation is used here, can be optimized.
    candidates = generateCandidates(domain=domain, size=size)
    print(f"INFO: number of candidates created is {len(candidates)}")
    print()

    # As we now have our candidates, we can begin to reconstruct.
    #   We will be reducing the number of candidates, choosing the best 
    #   possible one. A note: if given a hint on a query's value, the results
    #   can change. To add a hint, plug in the attribute (in index form) 
    #   for which the accurate query is known, as well as the value 
    #   in the form of a probability.

    # START: YOU CHANGE THIS VALUE:

    # This is for our "simple" example, where the class must have one professor.
    hint_dict = {1: 0.1}
    invariant = True

    # This is for example 1, where we know that the 1st query is 0.7222222.
    # hint_dict = {0: 0.7222222}
    # invariant = False

    # END: YOU CHANGE THIS VALUE:

    reconstructed_db = reconstruct(candidates=candidates, 
                                   domain=domain, 
                                   queries=q_values, 
                                   hint_dict=hint_dict, 
                                   k=kVal,
                                   invariant=invariant)
    
    print("Reconstructed database:")
    print(np.array(reconstructed_db))
    


main()