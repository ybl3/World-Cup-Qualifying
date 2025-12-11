########## UEFA (Europe) Specific Functions ############

import random
from utils import play_match, sort_teams_by_ranking, split_pots, group_draw, play_group_stage, get_place, get_group
from main import data

# Gets UEFA teams and sorts them into pots
# Returns a list of all the UEFA teams, as well as a list of the pots
def get_uefa_teams():
    uefa = []
    # Reads in all UEFA teams
    for row in data:
        if data[row]['Confederation'] == "UEFA":
            uefa.append(row)
    uefa = sort_teams_by_ranking(uefa) # sorting teams by ranking to be split into pots
    pots = split_pots(uefa, 12) # splitting those teams into 4 equal main pots (12 teams each), and a 5th pot of remaining teams (6 teams)
    return uefa, pots

# Simulate the 2nd round of UEFA Qualifying (the playoffs)
# Takes in the teams competing, returns the result of the playoffs as a list
# Takes all the runners up, splits them into 4 paths of 3 teams, where each path winner qualifies
# The best 4 performing runners up get byes
# The remaining 8 teams get seeded into 2 pots based on ranking, and they play eachother
# Team A plays the winner of Team B vs Team C
def uefa_playoff(teams, verbose=False):
    byes = teams[:4]
    pots = teams[4:]
    pots = sort_teams_by_ranking(pots)
    pot1 = pots[:4]
    pot2 = pots[4:]
    if verbose:
        print(byes, pot1, pot2)
    # Random draw to make each path (Index 0 is path 1, Index 1 is path 2 ...)
    random.shuffle(byes)
    random.shuffle(pot1)
    random.shuffle(pot2)
    paths = []
    i = 0
    for i in range(len(byes)): # Going through each path
        # Match 1
        t1 = data[pot1[i]]["Rating"]
        t2 = data[pot2[i]]["Rating"]
        m = play_match(t1, t2, 0) # First match of path i, matches are neutral so no home advantage
        wmatch1 = pot1[i] # winner of match 1, advances to final match
        lmatch1 = pot2[i] # loser of match 1, eliminated
        pens = "" # whether the match went to penalties or not
        if m == "t1": # team 1 wins
            pass
        elif m == "t2": # team 2 wins
            wmatch1 = pot2[i]
            lmatch1 = pot1[i]
        else: # draw, to be settled by a penalty shootout, randomly decided with 50/50 chance
            teams = [pot1[i], pot2[i]]
            random.shuffle(teams)
            wmatch1 = teams[0]
            lmatch1 = teams[1]
            pens = "on penalties"
        if verbose:
            print(wmatch1, "defeats", lmatch1, pens)
        # Match 2
        t1 = data[byes[i]]["Rating"]
        t2 = data[wmatch1]["Rating"]
        m = play_match(t1, t2, 0) #  Bye team vs winner of match1, matches are neutral so no home advantage
        wmatch2 = byes[i] # winner of match 2, qualifies to world cup
        lmatch2 = wmatch1 # loser of match 2, eliminated
        pens = "" # whether the match went to penalties
        if m == "t1": # team 1 wins
            pass
        elif m == "t2": # team 2 wins
            wmatch2 = wmatch1
            lmatch2 = byes[i]
        else: # draw, to be settled by a penalty shootout, randomly decided with 50/50 chance
            teams = [byes[i], wmatch1]
            random.shuffle(teams)
            wmatch2 = teams[0]
            lmatch2 = teams[1]
            pens = "on penalties"
        paths.append([wmatch2, lmatch2, lmatch1])
        if verbose:
            print(wmatch2, "defeats", lmatch2, pens)
            print(wmatch2, "qualifies")
    return paths



# Simulates the entire process of UEFA qualifying
# Takes in a list of lists as the pots and returns a list of the 16 qualified teams
# 54 teams each compete for 16 final places
# The first round consists of 12 groups of 4 or 5 times, each group winner qualifies directly
# The runners up of each group then compete in a playoff stage to determine the final 4 qualifiers
def uefa_qualifying(pots, verbose=False):
    ### First Round - Group Stage ###
    # 12 groups of 4-5 teams play a round robin group stage, top team qualifies, 2nd place goes to the next round
    if verbose:
        print("- 1st Round UEFA Qualifying -")
    groups = group_draw(pots, 12) # conducts a random draw to form the 12 groups based on the pots
    results = play_group_stage(groups, verbose) # simulates the entire group stage
    if verbose:
        g = ord('A')
        for r in results:
            print(f"Group {chr(g)}", r)
            g += 1
    first = get_place(results, 1) # gets the first placed teams of each group (directly qualified)
    qualified = list(first.keys())
    ### Second Round - Playoffs ###
    second = list(get_place(results, 2).keys()) # gets the runners up of each group which will contest the playoffs
    if verbose:
        print(qualified, "qualify to World Cup")
        print(second, "advance to playoffs")
        print(" - UEFA Qualifying Playoffs -")
    playoffs = uefa_playoff(second, verbose) # Simulates the entire playoff process
    for p in playoffs: # Each playoff winner qualifies
        qualified.append(p[0])
    if verbose:
        print(qualified[12:], "qualify to World Cup")
    return qualified, results, playoffs

# Simulates the process of uefa qualifying k times
# Takes in list of uefa teams and a list of lists of the pots and an integer k
# Returns dictionary of each uefa team and how many times they qualified
def sim_uefa_qualifying(teams, pots, k, focus=None, verbose=False):
    uefa = {}
    v = verbose
    if focus != None:
        verbose = False
    for team in teams:
        uefa[team] = 0
    for i in range(k):
        if verbose and not focus is None:
            print("###### Sim", i, "######")
        qualified, res, po = uefa_qualifying(pots, verbose)
        if focus in qualified:
            y = get_place(res, 2)
            g = get_group(res, focus)
            if v and (focus in list(y.keys())):
                for p in po:
                    if focus in p:
                        print(g, "Playoff:", p)
            elif v:
                print(g)
        for q in qualified:
            uefa[q] += 1
    uefa = {k: v for k, v in sorted(uefa.items(), key=lambda item: item[1], reverse=True)} 
    return uefa
