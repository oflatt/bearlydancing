import variables, classvar
from Battle import Battle
from pygame import Rect
from play_sound import stop_music, play_effect
from saveandload import save

def initiatebattle(enemy):
    variables.settings.state = "battle"
    classvar.player.change_of_state()
    enemy.sethealth()
    enemy.enterbattle()
    classvar.player.heal()
    classvar.battle = Battle(enemy)

    variables.dirtyrects = [Rect(0,0,variables.width,variables.height)]
    play_effect("engagebattle")
    stop_music()

    save(False);
    
