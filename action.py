'''
Performs the actions of the ship
'''
import random
# import game

# {'moveF': 12}

def action(picked_object, my_ship):
    '''
    Defines the actions of the ship
    80% of the time, the passed in action will be taken
    20% of the time, it will be random
    '''
    print "\n\n#############"
    print 'picked_object', picked_object
    combined_component = random.randint(0, 100)
    print "combined_component", combined_component
    if combined_component < 80:
        if picked_object[0] == 'moveT':
            print "q_actionT"
            q_action = my_ship.thrusters(True)
        else:
            print "q_actionF"
            q_action = my_ship.thrusters(False)
    else:
        random_component = random.randint(0, 100)
        print "random_component", random_component
        if random_component < 50:
            print "r_actionT"
            random_action = my_ship.thrusters(True)
        else:
            print "r_actionF"
            random_action = my_ship.thrusters(False)
