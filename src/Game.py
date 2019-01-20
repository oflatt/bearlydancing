from FrozenClass import FrozenClass

class Game(FrozenClass):

    def __init__(self, name, initfunction, inputfunction, tickfunction, drawfunction):
        # takes just the screen
        self.initfunction = initfunction
        
        # input function takes the current time, settings,  and the event
        self.inputfunction = inputfunction

        # tick function takes the current time, settings
        self.tickfunction = tickfunction

        # draw function takes the current time, settings, and screen
        self.drawfunction = drawfunction

        self._freeze()

                 
