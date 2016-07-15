

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
    return exp_needed(lv)/(1+lv)

#amount of damage done to enemy
def damage(lv):
    return max_health(lv)/4