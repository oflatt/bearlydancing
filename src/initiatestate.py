import variables, classvar
from Battle import Battle
from pygame import Rect

def initiatebattle(enemy, storypenalty):
    variables.settings.state = "battle"
    classvar.player.change_of_state()
    enemy.sethealth()
    classvar.player.heal()
    classvar.battle = Battle(enemy)
    classvar.battle.storypenalty = storypenalty
    classvar.battle.reset_time()
    # set up display
    variables.dirtyrects = [Rect(0,0,variables.width,variables.height)]
    variables.screen.fill(variables.BLACK)
