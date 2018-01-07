import variables
from Button import Button

class ChoiceButtons():
    def __init__(self, options, ypos, buttontextsize = 1.25):
        # a list of strings
        self.options = options
        self.current_option = 0
        self.buttons = []
        self.maxwidth = 0

        for s in options:
            newb = Button(0, ypos, s, buttontextsize)
            self.buttons.append(newb)
            if newb.width > self.maxwidth:
                self.maxwidth = newb.width
                
        spacing = self.maxwidth / 4        
        length = len(self.buttons)
        self.length = length
        centering = (variables.width - length * self.maxwidth - (length-1) * spacing) / 2
        
        for x in range(self.length):
            self.buttons[x].width = self.maxwidth
            self.buttons[x].x = x * (self.maxwidth + spacing) + centering
            
    def nextoption(self):
        self.current_option = (self.current_option + 1) % self.length

    def previousoption(self):
        self.current_option = (self.current_option-1) % self.length

    def getoption(self):
        return self.options[self.current_option]
            
    def draw(self):
        for i in range(self.length):
            b = self.buttons[i]
            if i == self.current_option:
                b.draw(True)
            else:
                b.draw(False)
