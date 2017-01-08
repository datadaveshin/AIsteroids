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
    # print "action 1"
    combined_component = random.randint(0, 100)
    if combined_component < 90:
        if picked_object[0] == 'moveT':
            q_action = my_ship.thrusters(True)

            if  6.283 < my_ship.angle or my_ship.angle < -6.283:
                my_ship.angle = 0.0
            direction = random.choice([-0.15,-0.1,0,0,0,0,0,0,0,0,0,0,0,0.1,0.1,0.15,0.15])
            my_ship.angle += direction

            if direction == 0.1:
                        my_ship.shoot()
            return picked_object[0]

        else:
            q_action = my_ship.thrusters(False)
            return 'moveF'
    else:
        random_component = random.randint(0, 100)
        if random_component < 50:
            random_action = my_ship.thrusters(True)

            if  6.283 < my_ship.angle or my_ship.angle < -6.283:
                my_ship.angle = 0.0
            direction = random.choice([-0.15,-0.1,0,0,0,0,0,0,0,0,0,0,0,0.1,0.1,0.15,0.15])
            my_ship.angle += direction
            if direction == 0.1:
                my_ship.shoot()
            return 'moveT'
        else:
            random_action = my_ship.thrusters(False)
            return 'moveF'


def action2(picked_object, my_ship):
    '''
    Defines the actions of the ship
    80% of the time, the passed in action will be taken
    20% of the time, it will be random
    '''
    # print "action2"
    if picked_object[0] == 'moveT':
        q_action = my_ship.thrusters(True)
        if  6.283 < my_ship.angle or my_ship.angle < -6.283:
            my_ship.angle = 0.0
        direction = random.choice([-0.15,-0.1,0,0,0,0,0,0,0,0,0,0,0,0.1,0.1,0.15,0.15])
        my_ship.angle += direction

        if direction == 0.1:
            my_ship.shoot()
        return picked_object[0]
    else:
        q_action = my_ship.thrusters(False)
        return 'moveF'
