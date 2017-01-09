

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


# global r_value_dict
# r_value_dict = {}

def make_q_dict(state, action):
    """
    Dynamically builds Q dict takes in state and action
    Affects the global obj q_value_dict
    """
    if state in q_value_dict:
        q_value_dict[state][action] = 0
    else:
        q_value_dict[state] = {}
        q_value_dict[state][action] = 0


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

def make_counter_dict(state1, action1, state_prime1):
    sa1 = state + "__" + action
    if sa1 in counter_dict:
        if state_prime1 in counter_dict[sa1]:
            counter_dict[sa1][state_prime1] += 1
        else:
            counter_dict[sa1][state_prime1] = 0
    else:
        counter_dict[sa1] = {}
        counter_dict[sa1][state_prime1] = 0
