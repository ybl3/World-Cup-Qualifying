import random
import numpy as np
import math
from config import data


############ Generic Functions ###############

# Randomly shuffles a dictionary
def shuffled_dict(d:dict):
    return {k: d[k] for k in random.sample(list(d.keys()), len(d))}

# Sort teams by Fifa ranking
# takes in list of teams, outputs the list sorted by Fifa ranking (ascending)
def sort_teams_by_ranking(teams):
    rankings = {}
    for team in teams:
        rankings[team] = int(data[team]['Ranking'])
    rankings = {k: v for k, v in sorted(rankings.items(), key=lambda item: item[1])}
    return list(rankings.keys())

# Gets the particular group the focus is in from a list of groups (dictionaries)
def get_group(groups, focus):
    g = {}
    for group in groups:
        if focus in list(group.keys()):
            return group
    return g

# Simulate a penalty shootout, 50/50 chance for either team, returns the winner
def penalty_shootout(team1, team2):
    teams = [team1, team2]
    random.shuffle(teams)
    return teams[0]

# Simulate a match played between team 1 (home team) and team 2 (away team)
# Takes in the numeral rating of team 1 and team 2 and a home field advantage score
# Returns the simulated result of the match ("t1" = team1 wins, "d" = draw, "t2" = team2 wins)
# Uses random numbers and probabilities to determine result, the better rating combined with home advantage will have a better chance of winning
# The larger the difference between team ratings, the larger the chance of the better team winning (logarithmic not linear though)
# A number i is randomly generated between 0 and 1, c1 and c2 are numbers such that 0 < c1 < c2 < 1
# 0 < i < c1 -> team 1 wins     c1 < i < c2 -> draw     c2 < i < 1 -> team2 wins
def play_match(team1, team2, h=0):
    # h = 0 # No home field advantage for now
    i = random.random() # randomly generate number that will be used to determine results later
    # Initial probabilities are set. If the teams have equal rating, these probabilities will be used.
    # This gives an equal chance of winning to each team. Draws are less likely, so the probabilities aren't exactly each 1/3
    c1 = 0.37 # initial probability of team 1 winning (0 to 0.37)
    c2 = 0.63 # initial probability of team 2 winning (0.63 to 1)
    d = 0.56 # draw initial probability, this determines the chances between the better team drawing or losing
    h = float(h)/10 # converts home advantage score to a decimal less than 1
    lnum = 100.0001 # used later
    t1 = min(float(team1) + h, 99) # home advantage makes the home team a little better
    t2 = float(team2)
    ar = np.array((t1, t2))
    best = np.argmax(ar) # determining which team has the better rating
    diff = ar[best] - ar[abs(1 - best)] # determining the difference between ratings
    # Teams with higher differences have an even better chance than winning than teams closer (it is not linear)
    # To deal with this, a multiplier r is used on the differences based on how large the differences are
    # Also, it is easier to beat a worse team, regardless of difference between rating
    r = 1.4 # initial multiplier, used if very large (>= 50) differences against the weakest teams
    if diff < 10:
        r = 0.1
    elif diff < 20 and ar[abs(1 - best)] < 12:
        r = 0.9
    elif diff < 20:
        r = 0.3
    elif diff < 30 and ar[abs(1 - best)] < 25:
        r = 1.1
    elif diff < 30:
        r = 0.45
    elif diff < 50 and ar[abs(1 - best)] < 30:
        r = 1.1
    elif diff < 50:
        r = 0.75
    elif ar[abs(1 - best)] > 35:
        r = 1.1
    mult = min(r * diff, 99.5)
    # Determining probabilities of each result
    if team1 == team2: # If the ratings are equal, use initial probabilities
        pass
    elif best == 0: # if team 1 is the better team
        c1 = max(0.33, math.log(diff + 1, lnum))
        c1 = c1 + mult/100 * (1 - c1)
        c2 = c1 + d * (1 - c1)
    else: # if team 2 is the better team
        c2 = max(0.33, math.log(diff + 1, lnum))
        c2 = 1 - (c2 + mult/100 * (1 - c2))
        c1 = c2 - d * c2
    res = "d"
    if i < c1: # team 1 wins
        res = "t1"
    elif i < c2: # draw
        res = "d"
    else: # team 2 wins
        res = "t2"
    return res


# Splits teams into pots of n teams
# Takes in a list of ordered teams and a number of teams per pot n (= # groups)
# Returns the pots as a list of lists (eg: pots = [pot1, pot2...], pot1 = [team1, team2...])
# If the teams can't be split exactly into pots of n teams, remainder teams will be assigned to the last pot
def split_pots(teams, n):
    pots = []
    j = 0 # number of teams in current pot to be used later in loop 
    current = [] # current pot to be used later in loop (initially 1st pot then 2nd pot and so on)
    for team in teams: # for each team
        current.append(team) # add to current pot
        j += 1 # increment number of teams in pot
        if j >= n: # if max number of teams per pot has been reached
            pots.append(current) # add pot to list of pots and reset current pot
            j = 0
            current = []
    if len(current) > 0: # in the case of remainder teams, add that last pot as well
        pots.append(current)
    return pots


# Conducts a group stage draw by randomly making n groups seeded by the pots
# Takes in each pot (list of lists eg: pots = [pot1, pot2...], pot1 = [team1, team2...]) and the number of groups n
# Returns the resultant n groups (lists of lists eg: groups = [group1, group2 ...], group1 = [team1, team2...])
# Each pot should have exactly n teams, though the last pot may have less teams than the rest
# Each group contains exactly one team from each pot, though it may contain no teams from the last pot if it has less teams
# The random draw is conducted by randomly shuffling each pot, then each group i consists of the ith team in pot1 and pot2 and so on
# k = len(pots), The groups will each contain at least k - 1 teams, and the remaining kth pot teams will be assigned to the first groups
def group_draw(pots, n):
    k = len(pots) # number of pots
    groups = [] # the final groups
    current = [] # the current group (the ith group later on)
    for i in range(k): # randomly shuffling each pot
        random.shuffle(pots[i])
    for i in range(n): # for each group 
        for j in range(k): # for each pot
            try: # take ith team in the jth pot and place it in the ith group. In the case of the pot not having i teams, then skip
                current.append(pots[j][i])
            except:
                pass
        groups.append(current) # after going through every pot, append the current (ith) group to the list of groups
        current = [] # and reset the current group for the next loop (i + 1)th group
    return groups

# Simulates a round robin group (all teams play eachother home and away (2 matches between each team))
# Takes in a list of the teams and returns an ordered dictionary of the teams and their points obtained
def play_group(teams, verbose=False):
    verbose = False
    table = {}
    if verbose: 
        print(teams)
    for t in teams: # initializing results table dictionary
        table[t] = 0
    # Looping through each pair of teams i (home) and j (away)
    for i in teams: # for each team in the group (home team)
        for j in teams: # for each other team in the group (away team)
            if i == j: # teams do not play themselves
                continue
            if verbose:
                print(i, "vs", j)
            r1 = data[i]['Rating'] # Rating of team i
            r2 = data[j]['Rating'] # Rating of team j
            h = int(data[i]['Home']) # home field advantage (team i is the home team)
            result = play_match(r1, r2, h) # simulate match between team i and team j
            # A win results in 3 points for the winning team, a draw results in 1 point for each team
            if result == 't1': # if the home team (team i) wins
                if verbose:
                    print(i, "wins")
                table[i] += 3
            elif result == 't2': # if the away team (team j) wins
                if verbose:
                    print(j, "wins")
                table[j] += 3
            else: # if it is a draw
                if verbose:
                    print("draw")
                table[i] += 1
                table[j] += 1
    final_table = {}
    ### The teams are to be sorted by points obtained. In the case of ties, teams are sorted by goal differential ###
    ### Since goals are not a part of this simulation, ties will be randomly decided ###
    table = shuffled_dict(table) # shuffle dictionary in case of ties (later sorting breaks ties by initial order)
    final_table = {k: v for k, v in sorted(table.items(), key=lambda item: item[1], reverse=True)} # sort teams by points
    if verbose:
        print(final_table)
    return final_table

# Simulates a simple group (all teams play eachother once)
# Takes in a list of the teams and returns an ordered dictionary of the teams and their points obtained
def play_group_once(teams, verbose=False):
    verbose = False
    table = {}
    if verbose:
        print(teams)
    for t in teams: # initializing results table dictionary
        table[t] = 0
    # Looping through each pair of teams i and j
    k = len(teams)
    for i in range(k): # for each team in the group
        for j in range(i+1, k): # for each other team in the group
            team1 = teams[i]
            team2 = teams[j]
            if verbose:
                print(team1, "vs", team2)
            r1 = data[team1]['Rating'] # Rating of team i
            r2 = data[team2]['Rating'] # Rating of team j
            h = 0 # Matches are neutral so no home field advantage
            result = play_match(r1, r2, h) # simulate match between team i and team j
            # A win results in 3 points for the winning team, a draw results in 1 point for each team
            if result == 't1': # if the home team (team i) wins
                if verbose:
                    print(team1, "wins")
                table[team1] += 3
            elif result == 't2': # if the away team (team j) wins
                if verbose:
                    print(team2, "wins")
                table[team2] += 3
            else: # if it is a draw
                if verbose:
                    print("draw")
                table[team1] += 1
                table[team2] += 1
    final_table = {}
    ### The teams are to be sorted by points obtained. In the case of ties, teams are sorted by goal differential ###
    ### Since goals are not a part of this simulation, ties will be randomly decided ###
    table = shuffled_dict(table) # shuffle dictionary in case of ties (later sorting breaks ties by initial order)
    final_table = {k: v for k, v in sorted(table.items(), key=lambda item: item[1], reverse=True)} # sort teams by points
    if verbose:
        print(final_table)
    return final_table

# simulates a singular group k times, this function is only used for testing purposes
def sim_group(teams, k, focus=None):
    nwins = {}
    for team in teams:
        nwins[team] = 0
    for i in range(k):
        final_table = play_group(teams)
        champ = list(final_table)[0]
        nwins[champ] += 1
        if champ == focus:
            print(final_table)
    # nwins = shuffled_dict(nwins)
    # nwins = {k: v for k, v in sorted(nwins.items(), key=lambda item: item[1], reverse=True)}
    return nwins

# Simulate an entire round robin group stage, returns each group ordered by finishing place
# Takes all groups( list of lists, eg: groups = [group1, group2...], group1 = [team1, team2...]
# returns the results as lists of lists (eg: results = [result1, result2], result1 =[1st, 2nd ...])
def play_group_stage(groups, verbose=False):
    results = []
    g = ord("A")
    for group in groups: # for each group
        if verbose:
            print(f"Group {chr(g)}", group)
            g += 1
            print(group)
        r = play_group(group, verbose) # simulate entire group (all matches)
        results.append(r) # add result of this group to final results
    return results

# Simulate an entire group stage where each team plays eachother once, returns each group ordered by finishing place
# Takes all groups( list of lists, eg: groups = [group1, group2...], group1 = [team1, team2...]
# returns the results as lists of lists (eg: results = [result1, result2], result1 =[1st, 2nd ...])
def play_simple_group_stage(groups, verbose=False):
    results = []
    g = ord("A")
    for group in groups: # for each group
        if verbose:
            print(f"Group {chr(g)}", group)
            g += 1
        r = play_group_once(group, verbose) # simulate entire group (all matches)
        results.append(r) # add result of this group to final results
    return results


# Gets the kth places team of each group (k = 1 first place, k = 2 second place ...)
# Takes a list of lists of the groups (results = [group1, group2..], group1 = [1st place, 2nd place ...])
# Returns a sorted dictionary of each kth placed team and the points they won
# In the case of unevenly quantified groups, matches played will not be equal
# results against the last place team are not counted to allow for equal matches played across all groups
# This can be ignored with the uneven flag
def get_place(results, k, uneven=True):
    place = {}
    s = len(results[len(results)-1]) # gets the size of the last group (which will be <= every other group)
    for r in results: # for each group
        keys = list(r.keys()) # teams
        vals = list(r.values()) # points obtained
        if uneven and len(r) > s: # if the group is larger than the smallest group and unevenness is not ignored
            place[keys[k-1]] = vals[k-1] - 6 # Disregard results against last place team by subtracting 6 points (=2 wins)
        else: # if the group is the same size as the smallest group, or unevenness is ignored
            place[keys[k-1]] = vals[k-1]
    place = shuffled_dict(place) # randomly shuffle order of dictionary (for ties)
    place = {k: v for k, v in sorted(place.items(), key=lambda item: item[1], reverse=True)} # sort the teams by points obtained
    return place

# Simulate a series of two legged matchups (Each team plays once match at home)
# Takes in a list of 2 sized tuples matchups (matchups = [matchup1, matchup2, ...], matchup1 = (team1, team2))
# Returns a list of the winning teams
# Winning both games or winning one and drawing one results in a win overall
# If both teams win one game or both games are draws, then the winner is decided by a penalty shootout
def play_two_legs(matchups, verbose=False):
    winners = []
    for matchup in matchups:
        t1 = matchup[0]
        t2 = matchup[1]
        t1wins = [("t1", "t2"), ("t1", "d"), ("d", "t2")] # Possible combinations of results for team 1 advancing
        t2wins = [("t2", "t1"), ("t2", "d"), ("d", "t1")] # Possible combinations of results for team 2 advancing
        # 1st Leg
        if verbose:
            print("1st Leg:", t1, "vs", t2)
        result1 = play_match(data[t1]["Rating"], data[t2]["Rating"], data[t1]["Home"])
        if result1 == "t1": # Team 1 wins
            if verbose:
                print(t1, "wins")
        elif result1 == "t2": # Team 2 wins
            if verbose:
                print(t2, "wins")
        else: # Draw
            if verbose:
                print("draw")
        # 2nd Leg
        if verbose:
            print("2nd Leg:", t2, "vs", t1)
        result2 = play_match(data[t2]["Rating"], data[t1]["Rating"], data[t2]["Home"])
        if result2 == "t1": # Team 2 wins
            if verbose:
                print(t2, "wins")
        elif result2 == "t2": # Team 1 wins
            if verbose:
                print(t1, "wins")
        else: # Draw
            if verbose:
                print("draw")
        results = (result1, result2)
        if results in t1wins: # Team 1 advances
            winners.append(t1)
            if verbose:
                print(t1, "advances")
        elif results in t2wins:
            winners.append(t2)
            if verbose: # Team 2 advances
                print(t2, "advances")
        else: # Draw -> penalty shootout
            w = penalty_shootout(t1, t2)
            winners.append(w)
            if verbose:
                print(w, "advances on penalties")
    return winners

# Simulate a series of matchups (Only one game)
# Takes in a list of 2 sized tuples matchups (matchups = [matchup1, matchup2, ...], matchup1 = (team1, team2))
# Returns a list of the winning teams
# Draws are decided by penalty shootout
def play_one_leg(matchups, verbose=False):
    winners = []
    for matchup in matchups:
        t1 = matchup[0]
        t2 = matchup[1]
        if verbose:
            print(t1, "vs", t2)
        result = play_match(data[t1]["Rating"], data[t2]["Rating"], 0)
        if result == "t1": # Team 1 wins
            winners.append(t1)
            if verbose:
                print(t1, "wins")
        elif result == "t2": # Team 2 wins
            winners.append(t2)
            if verbose:
                print(t2, "wins")
        else: # Draw, settled by penalty shootout
            w = penalty_shootout(t1, t2)
            winners.append(w)
            if verbose:
                print(w, "wins on penalties")
    return winners