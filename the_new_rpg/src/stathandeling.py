

def max_health(lv):
    return lv * 5 + 20

#exp needed to have a certain level
def lvexp(lv):
    return int(lv**3)

def explv(exp):
    return int(exp**(1./3.))

#calculated the exp needed to get to the next level
def exp_needed(lv):
    return int(lvexp(lv+1) - lvexp(lv))

#lv is the lv of the enemy
def exp_gained(lv):
    return int(exp_needed(lv)/(lv/2 + 2))

#amount of damage done to enemy
def damage(lv):
    return 5 + lv*3