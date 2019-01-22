import variables, classvar, maps
from pygame import Rect
from play_sound import stop_music, play_effect


# initiate battle is in a seperate files because of dependencies

def initiategame(gamename):
    variables.settings.state = "game"
    

    variables.settings.currentgame = gamename
    if callable(variables.games[gamename]):
        variables.games[gamename] = variables.games[gamename]()

    variables.games[gamename].initfunction(variables.screen)

    classvar.player.change_of_state()
    play_effect("engagebattle")
    stop_music()
    


def returntoworld():
    classvar.player.heal()
    variables.settings.state = "world"
    variables.dirtyrects = [Rect(0,0,variables.width,variables.height)]
    maps.initiatemusic()
