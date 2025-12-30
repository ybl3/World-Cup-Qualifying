import csv
import random
import uefa
import conmebol
import concacaf
import ofc
import caf
import afc
from utils import play_match, sort_teams_by_ranking, split_pots, group_draw, play_group_stage, get_place, get_group, play_one_leg
from config import data


# Simulates entire process of intercontinental playoffs
# Takes in the 6 teams sorted by ranking, outputs the 2 qualifying teams
# Teams are seeded by ranking, and two teams from the same confederation cannot meet
def inter_continental_playoff(teams, verbose=False):
    path1 = [teams[0]] # The top two teams are in separate paths and get a bye to the final match
    path2 = [teams[1]]
    path1conf = [data[teams[0]]["Confederation"]]
    path2conf = [data[teams[1]]["Confederation"]]
    pot2 = teams[2:] # The remaining teams are in pot 2 and will be randomly drawn to play eachother
    random.shuffle(pot2)
    for team in pot2:
        if len(path1) < 3 and data[team]["Confederation"] not in path1conf: # team can go into path 1
            path1.append(team)
            path1conf.append(data[team]["Confederation"])
        elif data[team]["Confederation"] not in path2conf: # team can go into path 2
            path2.append(team)
            path2conf.append(data[team]["Confederation"])
        else: # team cannot go into path 2
            path2.append(path1[2])
            path1[2] = team
    if verbose:
        print("Path 1:", path1)
        print("Path 2:", path2)
        print("Match 1 Inter-continental Playoff")
    r1_results = play_one_leg([(path1[1], path1[2]), (path2[1], path2[2])], verbose)
    if verbose:
        print("Match 2 Inter-continental Playoff")
    r2_results = play_one_leg([(path1[0], r1_results[0]), (path2[0], r1_results[1])], verbose)
    if verbose:
        print(r2_results, "qualify to the World Cup")
    return r2_results

# Simulates all qualifying for the world cup
def world_cup_qualifying(ccfteams, cmbteams, uefapots, cafpots, afcteams, ofcteams, verbose=False):
    qualified = ["Canada", "USA", "Mexico"]
    playoffs = []
    ### CONCACAF ###
    if verbose:
        print("##### CONCACAF Qualifying #####")
    q, ccfpo = concacaf.concacaf_qualifying(ccfteams, verbose)
    qualified += q
    playoffs += ccfpo
    ### CONMEBOL ###
    if verbose:
        print("##### CONMEBOL Qualifying #####")
    q, cmbpo = conmebol.conmebol_qualifying(cmbteams, verbose)
    qualified += q
    playoffs.append(cmbpo)
    ### UEFA ###
    if verbose:
        print("##### UEFA Qualifying #####")
    q, res, uefapo = uefa.uefa_qualifying(uefapots, verbose)
    qualified += q
    ### CAF ###
    if verbose:
        print("##### CAF Qualifying #####")
    q, cafpo = caf.caf_qualifying(cafpots, verbose)
    qualified += q
    playoffs.append(cafpo)
    ### AFC ###
    if verbose:
        print("##### AFC Qualifying #####")
    q, afcpo = afc.afc_qualifying(afcteams, verbose)
    qualified += q
    playoffs.append(afcpo)
    ### OFC ###
    if verbose:
        print("##### OFC Qualifying #####")
    q, ofcpo = ofc.ofc_qualifying(ofcteams, verbose)
    qualified.append(q)
    playoffs.append(ofcpo)
    ### Inter-Continental Playoffs ###
    if verbose:
        print("##### Inter-Continental Playoffs Qualifying #####")
    q = inter_continental_playoff(playoffs, verbose)
    qualified += q
    return qualified

# Change teams confederation to confed
# Swaps confederations with lowest ranked team in desired confederation to keep number of teams equal
# Takes in confederation dictionary which maps to lowest ranked team in the confederation
def change_confed(team, confed, confedmap):
    data[confedmap[confed]]["Confederation"] = data[team]["Confederation"]
    data[team]["Confederation"] = confed


def main():
    global data
    qualified_teams = []
    qualifications = {}
    rankings = {}
    filename = "data2.csv"
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data[row['Team']] = row
            qualifications[row['Team']] = 0
    

    # # Focuses
    # focus = "USA"
    # confed = "UEFA"
    # confedmap = {"CONCACAF": "USVirginIslands",
    #              "CONMEBOL": "Bolivia",
    #              "UEFA": "SanMarino",
    #              "CAF": "Eritrea",
    #              "AFC": "Macau",
    #              "OFC": "AmericanSamoa"}
    # change_confed(focus, confed, confedmap)

    # team1 = "Kazakhstan"
    # team2 = "Bulgaria"
    # t1 = data[team1]['Rating']
    # t2 = data[team2]['Rating']
    # h1 = data[team1]['Home']
    # h2 = data[team2]['Home']
    # # t1 = 13
    # # t2 = 95
    # gg = {}
    # gg["t1"] = 0
    # gg["d"] = 0
    # gg["t2"] = 0
    # ggh = {}
    # ggh["t1"] = 0
    # ggh["d"] = 0
    # ggh["t2"] = 0
    # for i in range(1000):
    #     gg[play_match(t1, t2, h1)] += 1
    #     ggh[play_match(t2, t1, h2)] += 1
    # print(gg)
    # print(ggh)
    # return 0
    ### UEFA ###
    # uefa_teams, uefa_pots = uefa.get_uefa_teams()
    # print(len(uefa_teams))
    # uefa_qualified = uefa.uefa_qualifying(uefa_pots, True)
    # qualified_teams += uefa_qualified
    # focus = None
    # verbose = False
    # k = 1000
    # d = uefa.sim_uefa_qualifying(uefa_teams, uefa_pots, k, focus=focus, verbose=verbose)
    # if focus is not None:
    #     print(focus, "qualified", d[focus], "out of", k, "times")
    # # print(d)
    # if focus is None:
    #     for team in d:
    #         print(team, d[team])
    # print(qualified_teams)    
    ### CONMEBOL ###
    # conmebol_teams = conmebol.get_conmebol_teams()
    # conmebol_qualified, conmebol_playoff = conmebol.conmebol_qualifying(conmebol_teams, True)
    # print(conmebol_qualified, conmebol_playoff)
    # k = 1000
    # q = conmebol.sim_conmebol_qualifying(conmebol_teams, k, verbose=False)
    # vals = list(q.values())
    # print(q)
    ### CONCACAF ###
    # ccf = concacaf.get_concacaf_teams()
    # print(len(ccf))
    # c = concacaf.concacaf_qualifying(ccf, True)
    # print(c)
    # k = 1000
    # q, p = concacaf.sim_concacaf_qualifying(ccf ,k)
    # # print(q)
    # # print(p)
    # for team in q:
    #     print(team, q[team], p[team])
    ### OFC ###
    # ofc_teams = ofc.get_ofc_teams()
    # print(len(ofc_teams))
    # ofc_qual = ofc.ofc_qualifying(ofc_teams, True)
    # print(ofc_qual)
    # k = 1000
    # q, p = ofc.sim_ofc_qualifying(ofc_teams, k)
    # for team in q:
    #     print(team, q[team], p[team])
    ### CAF ###
    # caf_teams, caf_pots = caf.get_caf_teams()
    # print(len(caf_teams))
    # q, p = caf.caf_qualifying(caf_pots, True)
    # print(q, p)
    # k = 1000
    # q, p = caf.sim_caf_qualifying(caf_teams, caf_pots, k, False)
    # for team in q:
    #     print(team, q[team], p[team])
    ### AFC ###
    # afc_teams = afc.get_afc_teams()
    # print(len(afc_teams))
    # verbose=True
    # # verbose=False
    # q, p = afc.afc_qualifying(afc_teams, verbose)
    # k = 1000
    # q, p = afc.sim_afc_qualifying(afc_teams, k, False)
    # for team in q:
    #     print(team, q[team], p[team])
    ### Inter-Continental Playoffs ###
    # icp_teams = ["Suriname", "Jamaica", "Bolivia", "DRCongo", "Iraq", "NewCaledonia"]
    # icp_teams = sort_teams_by_ranking(icp_teams)
    # icp = {}
    # for t in icp_teams:
    #     icp[t] = 0
    # for i in range(100):
    #     icp_q = inter_continental_playoff(icp_teams, False)
    #     for q in icp_q:
    #         icp[q] += 1
    # for team in icp:
    #     print(team, icp[team])


    # ccfteams = concacaf.get_concacaf_teams()
    # cmbteams = conmebol.get_conmebol_teams()
    # uefateams, uefapots = uefa.get_uefa_teams()
    # cafteams, cafpots = caf.get_caf_teams()
    # afcteams = afc.get_afc_teams()
    # ofcteams = ofc.get_ofc_teams()


    # for i in range(100):
    #     qualified = world_cup_qualifying(ccfteams, cmbteams, uefapots, cafpots, afcteams, ofcteams, False)
    #     for q in qualified:
    #         qualifications[q] += 1
    # qualifications = {k: v for k, v in sorted(qualifications.items(), key=lambda item: item[1], reverse=True)}
    # for team in qualifications:
    #     print(team, qualifications[team])
    # print("Qualified Teams:")
    # for q in qualified:
    #     print(q)

    





    ## End

    

if __name__ == "__main__":
    main()