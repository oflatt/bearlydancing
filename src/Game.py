from FrozenClass import FrozenClass

class Game(FrozenClass):

    def __init__(self, name, initfunction, inputfunction, tickfunction, drawfunction, pausefunction, unpausefunction):
        # takes just the screen
        self.initfunction = initfunction
        
        # input function takes the current time, settings,  and the event
        self.inputfunction = inputfunction

        # tick function takes the current time, settings
        self.tickfunction = tickfunction

        # draw function takes the current time, settings, and screen
        # it returns a list of dirtyrects to update
        self.drawfunction = drawfunction

        # takes the current time
        self.pausefunction = pausefunction
        
        # takes the current time
        self.unpausefunction = unpausefunction

        self._freeze()


                 
