

def max_health(lv):
    return lv * 5 + 20

#calculated the exp needed to get to the next level
def exp_needed(lv):
    return (lv+1)^3 - lv^3

#amount of damage done to enemy
def damage(lv):
    return 5 + lv*3