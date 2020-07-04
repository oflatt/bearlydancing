import variables
from Button import Button
from FrozenClass import FrozenClass

class ChoiceButtons(FrozenClass):
    # ypos and buttontextsize are multipliers of variables.height
    def __init__(self, options, ypos, buttontextsize = variables.gettextsize()/variables.height):
        # a list of strings
        self.options = options
        self.currentoption = 0
        self.buttons = []
        self.currentxscroll = 0
        self.isselected = True

        for optiontext in self.options:
            newb = Button(0, ypos, optiontext, buttontextsize)
            self.buttons.append(newb)
        
        self._freeze()
            
    def nextoption(self):
        self.currentoption = (self.currentoption + 1) % len(self.buttons)

    def previousoption(self):
        self.currentoption = (self.currentoption-1) % len(self.buttons)

    def getoption(self):
        return self.options[self.currentoption]

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

        buttonpositions = []
        for i in range(len(self.buttons)):
            buttonpositions.append(i * (maxwidth+spacing) + spacing)
            self.buttons[i].screenwidthoverride = maxwidth

        totalwidth = length * maxwidth + (length-1) * spacing
        
        if totalwidth <= 1:
            centering = (1 - length * maxwidth - (length-1) * spacing - 2*spacing) / 2
            self.currentxscroll = centering
        else:
            if buttonpositions[self.currentoption] + self.currentxscroll < 0:
                self.currentxscroll = -(buttonpositions[self.currentoption])
            if buttonpositions[self.currentoption] + maxwidth + self.currentxscroll > 1:
                self.currentxscroll = -(buttonpositions[self.currentoption] + maxwidth - 1)
                
            if self.currentoption == 0:
                self.currentxscroll = 0
            elif self.currentoption == len(self.buttons)-1:
                self.currentxscroll = -(totalwidth+2*spacing - 1)
            
        
        for i in range(len(self.buttons)):
            self.buttons[i].x = buttonpositions[i] + self.currentxscroll
        
        for i in range(len(self.buttons)):
            b = self.buttons[i]
            if b.x + maxwidth > 0:
                if i == self.currentoption and self.isselected:
                    b.draw(True)
                else:
                    b.draw(False)
