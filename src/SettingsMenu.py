import variables
from graphics import getTextPic
from FrozenClass import FrozenClass


class SettingsMenu(FrozenClass):
    def __init__(self, textxoffset):
        self.option = 0
        self.textxoffset = textxoffset
        
        self._freeze()

    def draw(self):
        ...


    def drawline(self, key, ypos):
        title = getTextPic(key, variables.textsize, variables.WHITE)
        variables.screen.blit(title, (self.textxoffset, ypos))
        for pk in variables.settings.keydict[key]:
            
