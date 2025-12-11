############### OFC (Oceania) Specific Functions ##############

from config import data
from utils import sort_teams_by_ranking, play_one_leg, split_pots, group_draw, play_simple_group_stage, play_group_stage, play_two_legs

# Gets OFC teams, returns a list sorted by fifa ranking
def get_ofc_teams():
    ofc = []
    # Reads in all OFC teams
    for row in data:
        if data[row]['Confederation'] == "OFC":
            ofc.append(row)
    ofc = sort_teams_by_ranking(ofc)
    return ofc


# Simulates the entire process of OFC qualifying
# Takes in a list of ofc teams sorted by ranking, returns qualified team and the playoff team
# Consists of 3 rounds
def ofc_qualifying(teams, verbose=False):
    ### First Round - Preliminary knockout ###
    # Lowest 4 ranked teams compete in a single leg semi-final and final to advance one team to the next round
    if verbose:
        print("- 1st Round OFC Qualifying -")
    r1matches = [(teams[7], teams[10]), (teams[8], teams[9])] # 8th vs 11th, 9th vs 10th
    r1winners = play_one_leg(r1matches, verbose)  # Initial matches
    r1winner = play_one_leg([(r1winners[0], r1winners[1])], verbose)[0] # Final match, between the previous 2 winners
    if verbose:
        print(r1winner, "advances to the next round")
    ### Second Round - Group stage ### 
    # 2 groups of 4 teams each, top 2 teams in each group advance to final round
    if verbose:
        print("- 2nd Round OFC Qualifying -")
    r2teams = teams[:8]
    r2teams[7] = r1winner
    pots = split_pots(r2teams, 2)
    groups = group_draw(pots, 2)
    r2results = play_simple_group_stage(groups, verbose) # The actual method used
    # r2results = play_group_stage(groups, verbose) # If you want more realistic results use this
    ### Third Round - Final knockout ###
    #  The advanicng teams play a single leg semi-final and final, final winner qualifies, final loser to the playoffs
    g1 = list(r2results[0].keys())
    g2 = list(r2results[1].keys())
    if verbose:
        print(g1[0], g1[1], g2[0], g2[1], "advance to the next round")
        print("- 3rd Round OFC Qualifying -")
    r3matchups = [(g1[0], g2[1]), (g2[0], g1[1])]
    r3results = play_one_leg(r3matchups, verbose) # They play only one leg in real life
    # r3results = play_two_legs(r3matchups, verbose) # If you want more realistic results, use this
    qualified = play_one_leg([(r3results[0], r3results[1])])[0] # They play only one leg in real life
    # qualified = play_two_legs([(r3results[0], r3results[1])])[0] # If you want more realistic results use this
    playoff = r3results[0]
    if qualified == playoff:
        playoff = r3results[1]
    if verbose:
        print(qualified, "qualifies, ", playoff, "advances to the inter-continental playoffs")
    return qualified, playoff

# sims process of ofc qualifying k times
# returns dictionary of each team and how many successful qualifications
def sim_ofc_qualifying(teams, k, verbose=False):
    ofc = {}
    p = {}
    for team in teams:
        ofc[team] = 0
        p[team] = 0
    for i in range(k):
        if verbose:
            print("###### Sim", i, "######")
        qual, po = ofc_qualifying(teams, verbose)
        ofc[qual] += 1
        p[po] += 1
    ofc = {k: v for k, v in sorted(ofc.items(), key=lambda item: item[1], reverse=True)}
    p = {k: v for k, v in sorted(p.items(), key=lambda item: item[1], reverse=True)}
    return ofc, p