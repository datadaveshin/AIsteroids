Skip to content
This repository
Search
Pull requests
Issues
Gist
 @datadaveshin
 Unwatch 2
  Star 0
 Fork 1 datadaveshin/AIsteroids Private
 Code  Issues 0  Pull requests 0  Projects 0  Wiki  Pulse  Graphs  Settings
Branch: addingTurns Find file Copy pathAIsteroids/testing.py
4d17665  13 minutes ago
 Michael Liu get_state get_max make_q_dict and make_r_dict
0 contributors
RawBlameHistory
136 lines (118 sloc)  3.75 KB


def get_state(killed, scored, in_zone1, in_zone2, in_zone3):
    """
    Builds A string for the STATE
    State is used in all other functions

    """
    string = "killed" + str(killed) + "__" + 'scored' +str(scored) + "__" + "in_zone1" + str(in_zone1) + "__" + "in_zone2" + str(in_zone2) + "__" + "in_zone3" + str(in_zone3)
    return string

# obj = {'killedFalse__scoredTrue__in_zone1True__in_zone2False__in_zone3False': {'thrustR': 10, 'shoot': 3, 'turnR': 5},
# 'killedTrue__scoredFalse__in_zone1False__in_zone2True__in_zone3False': {'thrustR': 4, 'shoot': 3, 'turnR': 5}}

def get_max(state):
    """
    takes in state and queries q_value_dict for maximum Value
    Returns an Array with they Key and max Value
    """
    print obj
    max_no = 0
    max_q_array =[]
    for key in obj[state]:
        if obj[state][key] > max_no:
            max_no = obj[state][key]
            max_q_array = [key, max_no]
    return max_q_array


# string2 = 'killedTrue__scoredFalse__in_zone1False__in_zone2True__in_zone3False'
# string = 'killedFalse__scoredTrue__in_zone1True__in_zone2False__in_zone3False'
#
# print get_max(string2)

# state3 = get_state(True, False, True, False, False)
# state4 = get_state(True, False, False, True, False)
# state5 = get_state(True, False, False, False, True)
# state6 = get_state(False, True, True, False, False)
#
#
# action = "thrustR"
# action2 = "shoot"
#
# global obj
# obj = {}
#
#

global r_value_dict
r_value_dict = {}
def make_q_dict(state, action):
    """
    Dynamically builds Q dict takes in state and action
    Affects the global obj q_value_dict
    """
    if state in obj:
        obj[state][action] = 0
    else:
        obj[state] = {}
        obj[state][action] = 0

state1 = 'killedTrue__scoredFalse__in_zone1False__in_zone2True__in_zone3False'
state2 = 'killedFalse__scoredFalse__in_zone1False__in_zone2True__in_zone3False'
state3 = 'killedFalse__scoredTrue__in_zone1True__in_zone2False__in_zone3False'
state4 = 'killedTrue__scoredFalse__in_zone1False__in_zone2False__in_zone3True'

['killedTrue', 'scoredFalse', 'in_zone1False', 'in_zone2True', 'in_zone3False']
def make_r_dict(state):
    """
    builds the Reward Table based on states encountered
    takes in state (a really long string) splits at every __ and assigns rewards
    constantly Updates r_value_dict Global Empty Object
    """
    split = state.split("__")
    if state in r_value_dict:
        #killed
        if split[0][-2:] == "ue":
            r_value_dict[state] += 0
        if split[0][-2:] == "se":
            r_value_dict[state] -= 500
        #scored
        if split[1][-2:] == "ue":
            r_value_dict[state] += 100
        if split[1][-2:] == "se":
            r_value_dict[state] -= 0
        #in_zone1
        if split[2][-2:] == "ue":
            r_value_dict[state] += 10
        if split[2][-2:] == "se":
            r_value_dict[state] -= 5
        #in_zone2
        if split[3][-2:] == "ue":
            r_value_dict[state] += 10
        if split[3][-2:] == "se":
            r_value_dict[state] -= 5
        #in_zone3
        if split[4][-2:] == "ue":
            r_value_dict[state] += 10
        if split[4][-2:] == "se":
            r_value_dict[state] -= 5
        #add keys to obj
    else:
            r_value_dict[state] = 0

make_r_dict(state1)
make_r_dict(state2)
make_r_dict(state1)
make_r_dict(state4)
make_r_dict(state3)
make_r_dict(state3)
make_r_dict(state3)
make_r_dict(state3)

print obj_reward



#
# make_obj(state3, action)
# make_obj(state4, action)
# make_obj(state5, action)
# make_obj(state6, action)
# # print obj
#
# make_obj(state3, action2)
# make_obj(state4, action2)
# make_obj(state5, action2)
# make_obj(state6, action2)
# def printobj(obj1):
#     print '\n \n#######'
#     for key in obj1:
#         print key, obj1[key]
#
# printobj(obj)
Contact GitHub API Training Shop Blog About
© 2017 GitHub, Inc. Terms Privacy Security Status Help
