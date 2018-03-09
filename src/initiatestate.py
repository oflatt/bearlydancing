import variables, classvar
from Battle import Battle
from pygame import Rect

def initiatebattle(enemy):
    variables.settings.state = "battle"
    classvar.player.change_of_state()
    enemy.sethealth()
    classvar.player.heal()
    classvar.battle = Battle(enemy)
    classvar.battle.reset_time()

    variables.dirtyrects = [Rect(0,0,variables.width,variables.height)]
