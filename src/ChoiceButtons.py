import variables
from Button import Button
from FrozenClass import FrozenClass

class ChoiceButtons(FrozenClass):
    # ypos and buttontextsize are multipliers of variables.height
    def __init__(self, options, ypos, buttontextsize = variables.gettextsize()/variables.height):
        # a list of strings
        self.options = options
        self.current_option = 0
        self.buttons = []

        for optiontext in self.options:
            newb = Button(0, ypos, optiontext, buttontextsize)
            self.buttons.append(newb)
        
        self._freeze()
            
    def nextoption(self):
        self.current_option = (self.current_option + 1) % len(self.buttons)

    def previousoption(self):
        self.current_option = (self.current_option-1) % len(self.buttons)

    def getoption(self):
        return self.options[self.current_option]

    def leftrightonkey(self, key):
        if variables.checkkey("left", key):
            self.previousoption()
        elif variables.checkkey("right", key):
            self.nextoption()
            
    def draw(self):
        # position things with correct spacing
        maxwidth = 0

        for button in self.buttons:
            if button.width()/variables.width > maxwidth:
                # divide by width because positions are multipliers of width
                maxwidth = button.width()/variables.width
        
        spacing = maxwidth / 4
        length = len(self.buttons)
        centering = (1 - length * maxwidth - (length-1) * spacing) / 2
        
        for i in range(len(self.buttons)):
            self.buttons[i].screenwidthoverride = maxwidth
            self.buttons[i].x = i * (maxwidth + spacing) + centering
        
        for i in range(len(self.buttons)):
            b = self.buttons[i]
            if i == self.current_option:
                b.draw(True)
            else:
                b.draw(False)
