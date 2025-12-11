############### AFC (Asia) Specific Functions ##############
from config import data
import random
from utils import sort_teams_by_ranking, play_two_legs, split_pots, group_draw, play_group_stage, get_place, play_simple_group_stage

# Gets AFC teams, returns a list sorted by fifa ranking
def get_afc_teams():
    afc = []
    # Reads in all AFC teams
    for row in data:
        if data[row]['Confederation'] == "AFC":
            afc.append(row)
    afc = sort_teams_by_ranking(afc)
    return afc

# Simulates entire process of AFC qualifying
# Takes in a list of participating teams sorted by Fifa Ranking
# Returns a list of the 8 qualified teams and also returns the playoff team
# Consists of 5 round
def afc_qualifying(teams, verbose=False):
    playoff = None
    ### First Round - Preliminary Round ###
    # Lowest 20 ranked teams compete in two legged playoff (seeded by fifa ranking) to advance to the next round
    if verbose:
        print("1st Round AFC Qualifying")
    first_round_pot1 = teams[26:36] # teams ranked 27th to 36th
    first_round_pot2 = teams[36:]
    random.shuffle(first_round_pot1) # Randomly drawing teams together
    random.shuffle(first_round_pot2)
    first_round_matchups = []
    for i in range(10):
        first_round_matchups.append((first_round_pot1[i], first_round_pot2[i]))
    first_round_results = play_two_legs(first_round_matchups, verbose)
    ### Second Round - First Group Stage ###
    # 9 groups of 4, top 2 teams advance to the next round
    if verbose:
        print(first_round_results, "advance to the next round")
        print("2nd Round AFC Qualifying")
    second_round_teams = teams[:36]
    second_round_teams[26:] = first_round_results
    second_round_teams = sort_teams_by_ranking(second_round_teams) # sorting teams to be seeded into pots
    second_round_pots = split_pots(second_round_teams, 9)
    second_round_groups = group_draw(second_round_pots, 9) # 9 groups of 4 teams each
    second_round_results = play_group_stage(second_round_groups, verbose) # full round robin groups, 6 games played by each team
    ### Third Round - Second Group Stage ###
    # 3 groups of 6, top 2 teams qualify, 3rd and 4th place teams advance to the next round
    first_places = list(get_place(second_round_results, 1).keys())
    second_places = list(get_place(second_round_results, 2).keys())
    third_round_teams = first_places + second_places
    if verbose:
        g = ord('A')
        for r in second_round_results:
            print(f"Group {chr(g)}", r)
            g += 1
        print(third_round_teams, "advance to the next round")
        print("3rd Round AFC Qualifying")
    third_round_teams = sort_teams_by_ranking(third_round_teams) # resorting teams to be seeded into pots
    third_round_pots = split_pots(third_round_teams, 3)
    third_round_groups = group_draw(third_round_pots, 3) # 3 groups of 6 teams each
    third_round_results = play_group_stage(third_round_groups, verbose) # full round robin group stage, 10 games played total for each team
    first_places = list(get_place(third_round_results, 1).keys())
    second_places = list(get_place(third_round_results, 2).keys())
    qualified = first_places + second_places # 1st and 2nd place directly qualify
    if verbose:
        g = ord('A')
        for r in third_round_results:
            print(f"Group {chr(g)}", r)
            g += 1
        print(qualified, "qualify to World Cup")
    ### Fourth Round - Group Stage playoff ###
    # 2 groups of 3, top team qualifies, 2nd place advances to next round
    third_places = list(get_place(third_round_results, 3).keys())
    fourth_places = list(get_place(third_round_results, 4).keys()) # 3rd and 4th place advance to the 4th round
    fourth_round_teams = third_places + fourth_places
    if verbose:
        print(fourth_round_teams, "advance to the next Round")
        print("4th Round AFC Qualifying")
    fourth_round_teams = sort_teams_by_ranking(fourth_round_teams) # resort teams to be seeded into pots
    fourth_round_pots = split_pots(fourth_round_teams, 2)
    fourth_round_groups = group_draw(fourth_round_pots, 2) # 2 groups of 3 teams each
    fourth_round_results = play_simple_group_stage(fourth_round_groups, verbose) # teams only play eachother once in these groups, 2 games total
    first_places = list(get_place(fourth_round_results, 1).keys())
    qualified = qualified + first_places # first placed team from both groups qualifies directly
    if verbose:
        g = ord('A')
        for r in fourth_round_results:
            print(f"Group {chr(g)}", r)
            g += 1
        print(first_places, "qualify to World Cup")
    ### Fifth Round - Final Playoff ###
    # The advancing teams from the previous round compete in a two-legged playoff to determine the inter-continental playoff team
    second_places = list(get_place(fourth_round_results, 2).keys())
    if verbose:
        print(second_places, "advance to the next Round")
        print("5th Round AFC Qualifying")
    playoff = play_two_legs([(second_places[0], second_places[1])], verbose)[0] # 2 leg playoff between 5th round teams
    if verbose:
        print(playoff, "advances to the inter-continental playoff")
    return qualified, playoff

# Sims process of afc qualifying k times
# returns dictionary of each team and how many successful qualifications
def sim_afc_qualifying(teams, k, verbose=False):
    afc = {}
    p = {}
    for team in teams:
        afc[team] = 0
        p[team] = 0
    for i in range(k):
        if verbose:
            print("###### Sim", i, "######")
        qual, po = afc_qualifying(teams, verbose)
        for q in qual:
            afc[q] += 1
        p[po] += 1
    afc = {k: v for k, v in sorted(afc.items(), key=lambda item: item[1], reverse=True)} 
    p = {k: v for k, v in sorted(p.items(), key=lambda item: item[1], reverse=True)} 
    return afc, p