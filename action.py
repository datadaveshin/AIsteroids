'''
Performs the actions of the ship
'''
import random


def action(picked_object, my_ship):
    '''
    Defines the actions of the ship
    80% of the time, the passed in action will be taken
    20% of the time, it will be random
    '''
    # if show:
    # print "\n\n#############"
    # print 'picked_object', picked_object
    combined_component = random.randint(0, 100)
    # print "combined_component", combined_component
    if combined_component < 80:
        if picked_object[0] == 'moveT':
            # print "q_actionT"
            q_action = my_ship.thrusters(True)
            my_ship.shoot()
            return picked_object[0]
        else:
            # print "q_actionF"
            q_action = my_ship.thrusters(False)
            return 'moveF'
    else:
        random_component = random.randint(0, 100)
        # print "random_component", random_component
        if random_component < 50:
            # print "r_actionT"
            random_action = my_ship.thrusters(True)
            my_ship.shoot()
            return 'moveT'
        else:
            # print "r_actionF"
            random_action = my_ship.thrusters(False)
            return 'moveF'

# def turnRight():
#     if  6.283 < my_ship.angle or my_ship.angle < -6.283:
#         my_ship.angle = 0.0
# my_ship.angle += 1.5708
#
# def turnLeft():
#     if  6.283 < my_ship.angle or my_ship.angle < -6.283:
#         my_ship.angle = 0.0
# my_ship.angle -= 1.5708


def action2(picked_object, my_ship):
    '''
    Defines the actions of the ship
    80% of the time, the passed in action will be taken
    20% of the time, it will be random
    '''
    # if show:
    # print "\n\n#############"
    # print 'picked_object', picked_object
    # combined_component = random.randint(0, 100)
    # print "combined_component", combined_component
    # if combined_component < 100:
    if picked_object[0] == 'moveT':
        # print "q_actionT"
        q_action = my_ship.thrusters(True)
        my_ship.shoot()
        return picked_object[0]
    else:
        # print "q_actionF"
        q_action = my_ship.thrusters(False)
        return 'moveF'
    # else:
    #     random_component = random.randint(0, 100)
    #     # print "random_component", random_component
    #     if random_component < 50:
    #         # print "r_actionT"
    #         random_action = my_ship.thrusters(True)
    #         my_ship.shoot()
    #         return 'moveT'
    #     else:
    #         # print "r_actionF"
    #         random_action = my_ship.thrusters(False)
    #         return 'moveF'
