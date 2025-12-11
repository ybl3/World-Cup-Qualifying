############ CONMEBOL (South America) Specific Functions #############

import random
from config import data
from utils import play_group

# Gets CONMEBOL teams, returns a list
def get_conmebol_teams():
    conmebol = []
    # Reads in all CONMEBOL teams
    for row in data:
        if data[row]['Confederation'] == "CONMEBOL":
            conmebol.append(row)
    return conmebol

# Simulates entire process of CONMEBOL qualifying
# Takes in the 10 teams as a list, returns a list of the 6 qualified teams and a string of the playoff team
# Consists of just one round: a round robin of all 10 teams in CONMEBOL, each team plays eachother home and away
# Top 6 teams qualify directly, the 7th placed team proceeds to the inter-confederation playoffs
def conmebol_qualifying(teams, verbose=False):
    ### First Round - Group Stage ###
    # All competing teams play a round robin group stage, top 6 teams qualify, 7th place goes to playoffs
    if verbose:
        print("- CONMEBOL Qualifying -")
    result = play_group(teams, verbose) # Simulate the group, results in dictionary
    keys = list(result.keys()) # getting a list out of the keys (will stay in order)
    qualified = keys[:6] # Top 6 teams
    playoff = keys[6] # 7th placed team
    if verbose:
        print(qualified, "qualify to World Cup")
        print(playoff, "advances to the inter-continental playoffs")
    return qualified, playoff

# Simulates the process of Conmebol qualifying k times
# Takes in a list of the conmebol teams and an integer k
# Returns dictionary of each team and how many times they qualified
def sim_conmebol_qualifying(teams, k, focus=None, verbose=False):
    conmebol = {}
    for team in teams:
        conmebol[team] = 0
    for i in range(k):
        if verbose:
           print("###### Sim", i, "######")
        q, p = conmebol_qualifying(teams, verbose)
        for t in q:
            conmebol[t] += 1
        # as we are only simulating conmebol, we will not know results of the intercontinental playoff
        # to predict them, a random number is used. Conmebol should make it most of the time, so the probability is high
        if random.random() > 0.23:  
            conmebol[p] += 1
        # if focus in q:
        #     print(q)
    conmebol = {k: v for k, v in sorted(conmebol.items(), key=lambda item: item[1], reverse=True)} 
    return conmebol
