

def max_health(lv):
    return lv * 5 + 20

#calculated the exp needed to get to the next level
def exp_needed(lv):
    return int((lv+1)^3 - lv^3)

#lv is the lv of the enemy
def exp_gained(lv):
    return int(exp_needed(lv)/(lv/2 + 2))

#amount of damage done to enemy
def damage(lv):
    return 5 + lv*3