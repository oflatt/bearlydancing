import variables
from Button import Button

class ChoiceButtons():
    # ypos and buttontextsize are multipliers of variables.height
    def __init__(self, options, ypos, buttontextsize = variables.gettextsize()/variables.height):
        # a list of strings
        self.options = options
        self.current_option = 0
        self.buttons = []
        self.maxwidth = 0

        for s in options:
            newb = Button(0, ypos, s, buttontextsize)
            self.buttons.append(newb)
            if newb.width() > self.maxwidth:
                # devide by width because positions are multipliers of width
                self.maxwidth = newb.width()/variables.width
        
        spacing = self.maxwidth / 4
        length = len(self.buttons)
        self.length = length
        centering = (1 - length * self.maxwidth - (length-1) * spacing) / 2
        
        for i in range(self.length):
            self.buttons[i].screenwidthoverridee = self.maxwidth
            self.buttons[i].x = i * (self.maxwidth + spacing) + centering
            
    def nextoption(self):
        self.current_option = (self.current_option + 1) % self.length

    def previousoption(self):
        self.current_option = (self.current_option-1) % self.length

    def getoption(self):
        return self.options[self.current_option]

    def leftrightonkey(self, key):
        if variables.checkkey("left", key):
            self.previousoption()
        elif variables.checkkey("right", key):
            self.nextoption()
            
    def draw(self):
        for i in range(self.length):
            b = self.buttons[i]
            if i == self.current_option:
                b.draw(True)
            else:
                b.draw(False)
