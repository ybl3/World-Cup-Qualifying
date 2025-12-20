############### CONCACAF (North America) Specific Functions ##############

from config import data
from utils import sort_teams_by_ranking, play_two_legs, split_pots, group_draw, play_simple_group_stage, get_place, play_group_stage

# Gets CONCACAF teams, returns a list sorted by fifa ranking
# If remove_hosts flag is true, removes the current hosts (USA, Canada, Mexico) as they will not participate in qualifying
def get_concacaf_teams(remove_hosts=True):
    concacaf = []
    hosts = ["Canada", "USA", "Mexico"]
    # Reads in all CONCACAF teams
    for row in data:
        if data[row]['Confederation'] == "CONCACAF":
            if row in hosts and remove_hosts == True:
                continue
            concacaf.append(row)
    concacaf = sort_teams_by_ranking(concacaf)
    return concacaf

# Simulates the entire CONCACAF qualifying process (*For 2026 specifically)
# Note that this is assuming that the 3 hosts (USA, Canada, Mexico) are not participating in qualifying
# Takes in a list of participating teams (assuming 32) sorted by Fifa Ranking
# Returns a list of the 3 qualified teams as well as the 2 playoff teams
# Consists of 3 rounds
def concacaf_qualifying(teams, verbose=False):
    ### 1st round - Preliminary Round ###
    # 2-legged knockout between 4 lowest ranked teams (29th vs 32nd, 30th vs 31st)
    if verbose:
        print("- 1st Round CONCACAF Qualifying -")
    r1matchups = [(teams[28], teams[31]), (teams[29], teams[30])]
    r1results = play_two_legs(r1matchups, verbose)
    if verbose:
        print(r1results, "advance to the next round")
    ### 2nd round - First Group stage ###
    # 6 groups of 5, teams only play once against eachother, top 2 teams from each group advance to final round
    if verbose:
        print("- 2nd Round CONCACAF Qualifying -")
    r2teams = teams[:30]
    r2teams[28] = r1results[0]
    r2teams[29] = r1results[1]
    pots = split_pots(r2teams, 6) # split teams into 5 pots
    groups = group_draw(pots, 6) # conduct draw for 6 groups
    r2results = play_simple_group_stage(groups, verbose) # only one game between each team
    if verbose:
        g = ord('A')
        for r in r2results:
            print(f"Group {chr(g)}", r)
            g += 1
    ### 3rd round, Final Group Stage ###
    # 3 groups of 4, round-robin groups, top team qualifies directly to world cup, the 2 best runners up go to the playoffs
    p1 = list(get_place(r2results, 1).keys())
    p2 = list(get_place(r2results, 2).keys())
    r3teams = p1 + p2
    if verbose:
        print(r3teams, "advance to the next round")
        print("- 3rd Round CONCACAF Qualifying -")
    r3teams = sort_teams_by_ranking(r3teams)  # Need to sort advancing teams by ranking in order to seed them
    r3pots = split_pots(r3teams, 3) # split teams into 4 pots
    r3groups = group_draw(r3pots, 3) # conduct draw for 3 groups
    r3results = play_group_stage(r3groups, verbose) # two games between each team
    if verbose:
        g = ord('A')
        for r in r3results:
            print(f"Group {chr(g)}", r)
            g += 1
    qualified = list(get_place(r3results, 1).keys())
    p2 = list(get_place(r3results, 2).keys())[:2] # best2 second place teams make the intercontinental playoffs
    if verbose:
        print(qualified, "qualify to the World Cup")
        print(p2[0], "and", p2[1], "advance to the intercontinental playoffs")
    return qualified, p2

# Sims concacaf qualifying k times
def sim_concacaf_qualifying(teams, k, verbose=False):
    concacaf = {}
    playoffs = {}
    for team in teams:
        concacaf[team] = 0
        playoffs[team] = 0
    for i in range(k):
        if verbose:
            print("###### Sim", i, "######")
        qualified, p = concacaf_qualifying(teams, verbose)
        for q in qualified:
            concacaf[q] += 1
        playoffs[p[0]] += 1
        playoffs[p[1]] += 1
    concacaf = {k: v for k, v in sorted(concacaf.items(), key=lambda item: item[1], reverse=True)}
    playoffs = {k: v for k, v in sorted(playoffs.items(), key=lambda item: item[1], reverse=True)}
    return concacaf, playoffs