'''
Has the functions and data structures for dealing with the ai
'''

import random



# reward_dict = {
#     'asteroidT__aliveT': 1,
#     'asteroidT__aliveF': -500,
#     'asteroidF__aliveT': 1,
#     'asteroidF__aliveF': -500
# }

reward_dict = {
    'asteroidT__aliveT': 0,
    'asteroidT__aliveF': 0,
    'asteroidF__aliveT': 0,
    'asteroidF__aliveF': 0
}
def update_reward_dict(a_score):
    reward_dict['asteroidT__aliveF'] = a_score
    reward_dict["asteroidF__aliveF"] = a_score


counter_dict = {
    'asteroidT__aliveT__moveT': {
                    'asteroidT__aliveT': 0,
                    'asteroidT__aliveF': 0,
                    'asteroidF__aliveT': 0,
                    'asteroidF__aliveF': 0,
                    },

    'asteroidT__aliveT__moveF': {
                    'asteroidT__aliveT': 0,
                    'asteroidT__aliveF': 0,
                    'asteroidF__aliveT': 0,
                    'asteroidF__aliveF': 0,
                    },

    'asteroidT__aliveF__moveT': {
                    'asteroidT__aliveT': 0,
                    'asteroidT__aliveF': 0,
                    'asteroidF__aliveT': 0,
                    'asteroidF__aliveF': 0,
                    },

    'asteroidT__aliveF__moveF': {
                    'asteroidT__aliveT': 0,
                    'asteroidT__aliveF': 0,
                    'asteroidF__aliveT': 0,
                    'asteroidF__aliveF': 0,
                    },
    'asteroidF__aliveT__moveT': {
                    'asteroidT__aliveT': 0,
                    'asteroidT__aliveF': 0,
                    'asteroidF__aliveT': 0,
                    'asteroidF__aliveF': 0,
                    },

    'asteroidF__aliveT__moveF': {
                    'asteroidT__aliveT': 0,
                    'asteroidT__aliveF': 0,
                    'asteroidF__aliveT': 0,
                    'asteroidF__aliveF': 0,
                    },

    'asteroidF__aliveF__moveT': {
                    'asteroidT__aliveT': 0,
                    'asteroidT__aliveF': 0,
                    'asteroidF__aliveT': 0,
                    'asteroidF__aliveF': 0,
                    },

    'asteroidF__aliveF__moveF': {
                    'asteroidT__aliveT': 0,
                    'asteroidT__aliveF': 0,
                    'asteroidF__aliveT': 0,
                    'asteroidF__aliveF': 0,
                    },

    }

print counter_dict['asteroidF__aliveF__moveF']['asteroidT__aliveT']
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

def get_state(rocks, ships_hit_rocks):
    '''
    Returns a pair of Booleans
    The first is if a rock is in the zone
    The second is if the ship collided (died) with the rocks
    '''
    if rocks:
        if ships_hit_rocks:
            return 'asteroidT__aliveF'
        else:
            return 'asteroidT__aliveT'
    else:
        if ships_hit_rocks:
            return 'asteroidF__aliveF'
        else:
            return 'asteroidF__aliveT'


def get_max_q(state):
    '''
    Takes a string representing a state and returns the q-values for valid moves
    '''
    if q_value_dict[state]['moveT'] > q_value_dict[state]['moveF']:
        return ['moveT', q_value_dict[state]['moveT']]
    elif q_value_dict[state]['moveT'] < q_value_dict[state]['moveF']:
        return ['moveF', q_value_dict[state]['moveF']]
    else:
        return random.choice([['moveT', q_value_dict[state]['moveT']], ['moveF', q_value_dict[state]['moveF']]])



def q_learning(qkey1, state_prime, discount, max_q, a_score):
    counter_dict[qkey1][state_prime] += 1
    total_observations = 0.0
    for key in counter_dict[qkey1]:
        # print "key", key, "counter_dict[qkey1]", counter_dict[qkey1]
        total_observations += counter_dict[qkey1][key]
    q_value = 0
    for key in counter_dict[qkey1]:
        t_probability = counter_dict[qkey1][key] / total_observations
        if reward_dict[state_prime] == 'asteroidT__aliveF' or reward_dict[state_prime] == 'asteroidF__aliveF':
            reward_given = update_reward_dict(a_score)
        else:
            reward_given = 0
        v_star = discount * (max_q[1])
        component = t_probability * (reward_given + v_star)
        q_value += component
    # print "\naverage", average
    # reward_given = reward_dict[state_prime]
    # print "reward", reward_given, "max_q1", max_q
    # q_value = average * (reward_given + (discount * (max_q[1])))
    # print 'q_value', q_value
    return q_value

def set_q_value(value, state_prime, p_action_move):
    # print 'q_value_dict[state_prime][state]', q_value_dict[state_prime][p_action_move]
    q_value_dict[state_prime][p_action_move] += value
    # print "p_action_move", p_action_move, "state_prime", state_prime, "value", value, "qval", q_value_dict[state_prime][p_action_move]
