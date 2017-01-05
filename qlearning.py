'''
Has the functions and data structures for dealing with the ai
'''

import random

def get_state(rocks, ships_hit_rocks):
    '''
    Returns a pair of Booleans
    The first is if a rock is in the zone
    The second is if the ship collided (died) with the rocks
    '''
    if rocks:
        if ships_hit_rocks:
            return 'asteroidT__aliveT'
        else:
            return 'asteroidT__aliveF'
    else:
        if ships_hit_rocks:
            return 'asteroidF__aliveT'
        else:
            return 'asteroidF__aliveF'

print get_state(True, False)

reward_dict = {
    'asteroidT__aliveT': 1,
    'asteroidT__aliveF': -50,
    'asteroidF__aliveT': 1,
    'asteroidF__aliveF' -50
}

counter_dict = {
    'asteroidT__aliveT__moveT': {
                    'asteroidT__aliveT': 0,
                    'asteroidT__aliveF': 0,
                    'asteroidF__aliveT': 0,
                    'asteroidF__aliveF:': 0,
                    },

    'asteroidT__aliveT__moveF': {
                    'asteroidT__aliveT': 0,
                    'asteroidT__aliveF': 0,
                    'asteroidF__aliveT': 0,
                    'asteroidF__aliveF:': 0,
                    },

    'asteroidT__aliveF__moveT': {
                    'asteroidT__aliveT': 0,
                    'asteroidT__aliveF': 0,
                    'asteroidF__aliveT': 0,
                    'asteroidF__aliveF:': 0,
                    },

    'asteroidT__aliveF__moveF': {
                    'asteroidT__aliveT': 0,
                    'asteroidT__aliveF': 0,
                    'asteroidF__aliveT': 0,
                    'asteroidF__aliveF:': 0,
                    },
    'asteroidF__aliveT__moveT': {
                    'asteroidT__aliveT': 0,
                    'asteroidT__aliveF': 0,
                    'asteroidF__aliveT': 0,
                    'asteroidF__aliveF:': 0,
                    },

    'asteroidF__aliveT__moveF': {
                    'asteroidT__aliveT': 0,
                    'asteroidT__aliveF': 0,
                    'asteroidF__aliveT': 0,
                    'asteroidF__aliveF:': 0,
                    },

    'asteroidF__aliveF__moveT': {
                    'asteroidT__aliveT': 0,
                    'asteroidT__aliveF': 0,
                    'asteroidF__aliveT': 0,
                    'asteroidF__aliveF:': 0,
                    },

    'asteroidF__aliveF__moveF': {
                    'asteroidT__aliveT': 0,
                    'asteroidT__aliveF': 0,
                    'asteroidF__aliveT': 0,
                    'asteroidF__aliveF:': 0,
                    },

    }


# q_value_dict  = {
#     'asteroidT__aliveT__moveT': 0,
#     'asteroidT__aliveT__moveF': 0,
#     'asteroidT__aliveF__moveT': 0,
#     'asteroidT__aliveF__moveF': 0,
#     'asteroidF__aliveT__moveT': 0,
#     'asteroidF__aliveT__moveF': 0,
#     'asteroidF__aliveF__moveT': 0,
#     'asteroidF__aliveF__moveF': 0,
#     }

q_value_dict  = {
    'asteroidT__aliveT': {'moveT': 0, 'moveF': 0},
    'asteroidT__aliveF': {'moveT': 0, 'moveF': 0},
    'asteroidF__aliveT': {'moveT': 0, 'moveF': 0},
    'asteroidF__aliveF': {'moveT': 0, 'moveF': 0},
    }


def lookup_q_values(state):
    '''
    Takes a string representing a state and returns the q-values for valid moves
    '''
    if q_value_dict[state]['moveT'] > q_value_dict[state]['moveF']:
        return ['moveT', q_value_dict[state]['moveT']]
    elif q_value_dict[state]['moveT'] < q_value_dict[state]['moveF']:
        return ['moveF', q_value_dict[state]['moveF']]
    else:
        return random.choice([['moveT', q_value_dict[state]['moveT']], ['moveF', q_value_dict[state]['moveF']]])

print lookup_q_values('asteroidT__aliveT')


def q_learning(qkey1, state_prime, discount, max_q):
    counter_dict[qkey1][state_prime] += 1
    sum = 0
    counter = 0
    for key in counter_dict[qkey1]:
        sum += counter_dict[qkey1][key]
        counter++
    average = sum / counter
    reward_given = reward_dict[state_prime]
    q_value = average * (reward_given + (discount * max_q))
    return q_value

def set_q_value(value, state_prime):
    q_value_dict[state_prime] = value
