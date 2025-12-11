############### CAF (Africa) Specific Functions ##############
from config import data
from utils import sort_teams_by_ranking, split_pots, group_draw, play_group_stage, get_place, play_one_leg

# Gets CAF teams, returns a list sorted by fifa ranking, as well as a list of pots
def get_caf_teams():
    caf = []
    # Reads in all CAF teams
    for row in data:
        if data[row]['Confederation'] == "CAF":
            caf.append(row)
    caf = sort_teams_by_ranking(caf)
    pots = split_pots(caf, 9) # Get pots of 9 teams each
    return caf, pots

# Simulates entire process of CAF qualifying
# Takes in a list of pots including the caf teams, returns list of qualified teams as well as the playoff team
# Consists of one group stage, and then a playoff for the inter-continental playoff spot
def caf_qualifying(pots, verbose=False):
    ### First Round - Group Stage ###
    # The 54 teams are divided into 9 groups of 6, play a round robin group stage where the top team from each group qualifies
    if verbose:
        print("- 1st Round CAF Qualifying -")
    groups = group_draw(pots, 9) # Prepare the groups (seeded by FIFA ranking)
    results = play_group_stage(groups, verbose) # Simulate the round-robin group stage
    if verbose:
        g = ord('A')
        for r in results:
            print(f"Group {chr(g)}", r)
            g += 1
    first = get_place(results, 1) # gets the first placed teams of each group (directly qualified)
    qualified = list(first.keys())
    ### Second Round - Playoffs ###
    # The four best 2nd place teams compete in a playoff to determine the inter-continental playoff team
    second = get_place(results, 2) # gets the runners up of each group which will contest the playoffs
    if verbose:
        print(qualified, "qualify to World Cup")
        print("2nd place rankings:", second)
        print(list(second.keys())[:4], "advance to the 2nd Round")
        print(" - 2nd Round CAF Qualifying -")
    second = list(second.keys()) # gets the runners up of each group which will contest the playoffs
    playoff_matches = [(second[0], second[3]), (second[1], second[2])]  # 1st vs 4th, 2nd vs 3rd
    playoff_results = play_one_leg(playoff_matches, verbose) # semi-finals
    playoff_winner = play_one_leg([(playoff_results[0], playoff_results[1])], verbose)[0] # winners of the previous round contest final
    if verbose:    
        print(playoff_winner, "advances to the inter-continental playoff")
    return qualified, playoff_winner

# Sims process of caf qualifying k times
# returns dictionary of each team and how many successful qualifications
def sim_caf_qualifying(teams, pots, k, verbose=False):
    caf = {}
    p = {}
    for t in teams:
        caf[t] = 0
        p[t] = 0
    for i in range(k):
        if verbose:
            print("###### Sim", i, "######")
        qualified, playoff = caf_qualifying(pots, verbose)
        for q in qualified:
            caf[q] += 1
        p[playoff] += 1
    caf = {k: v for k, v in sorted(caf.items(), key=lambda item: item[1], reverse=True)} 
    p = {k: v for k, v in sorted(p.items(), key=lambda item: item[1], reverse=True)} 
    return caf, p