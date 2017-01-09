def gen_all_states(states):
    list_of_states = []
    expanded_list = []
    for item in states:
        first = item + 'True'
        second = item + 'False'
        expanded_list.append([first, second])
    expanded_list.reverse()
    print expanded_list
    # for item2 in explanded_list:
    #     for subitem in item2:
    #         pass


gen_all_states(['killed', 'scored', 'in_zone2'])
