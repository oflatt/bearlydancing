import variables, classvar
from Battle import Battle
from pygame import Rect

def initiatebattle(enemy, storypenalty = None):
    variables.settings.state = "battle"
    classvar.player.change_of_state()
    enemy.sethealth()
    classvar.player.heal()
    classvar.battle = Battle(enemy)
    if storypenalty != None:
        classvar.battle.storypenalty = storypenalty
    classvar.battle.reset_time()
