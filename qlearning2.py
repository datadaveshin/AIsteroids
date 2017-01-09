'''
Has the functions and data structures for dealing with the AI
'''
import random

counter_dict = {}
r_val_dict = {}
q_value_dict = {}


def make_counter_dict(state1, action1, state_prime1):
    sa1 = state1 + "__" + action1
    if sa1 in counter_dict:
        if state_prime1 in counter_dict[sa1]:
            counter_dict[sa1][state_prime1] += 1
        else:
            counter_dict[sa1][state_prime1] = 0
        else:
            counter_dict[sa1] = {}
            counter_dict[sa1][state_prime1] = 0


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


def get_state(killed, scored, in_zone1, in_zone2, in_zone3):
    """
    Builds A string for the STATE
    State is used in all other functions

    """
    string = "killed" + str(killed) + "__" + 'scored' +str(scored) + "__" + "in_zone1" + str(in_zone1) + "__" + "in_zone2" + str(in_zone2) + "__" + "in_zone3" + str(in_zone3)
    return string

def get_max_q(state):
    """
    takes in state and queries q_value_dict for maximum Value
    Returns an Array with they Key and max Value
    """
    max_no = 0
    max_q_array =[]
    for key in q_value_dict[state]:
        if q_value_dict[state][key] > max_no:
            max_no = q_value_dict[state][key]
            max_q_array = [key, max_no]
    return max_q_array

def q_learning(qkey1, state_prime, discount, max_q):
    '''
    qkey1: asteroidT__aliveT__moveT
    state_prime: asteroidF__aliveT
    discount: 0.5
    max_q: 0
    '''
    counter_dict[qkey1][state_prime] += 1
    total_observations = 0.0

    for key in counter_dict[qkey1]:
        # print "key", key, "counter_dict[qkey1]", counter_dict[qkey1]
        total_observations += counter_dict[qkey1][key]
    q_value = 0

    for key in counter_dict[qkey1]:
        t_probability = counter_dict[qkey1][key] / total_observations
        reward_given = reward_dict[state_prime]
        v_star = discount * (max_q[1])
        component = t_probability * (reward_given + v_star)
        q_value += component

    return q_value


def set_q_value(value, state_prime, p_action_move):
    q_value_dict[state_prime][p_action_move] = value
