import classvar

class EventRequirement():

    def __init__(self, eventname, eventgreaterthan = 0, eventlessthan = 99999999):
        # name of the storyevent recorded in player
        self.eventname = eventname
        # for requirement to be fulfilled, the number of times the event has to have occured more than
        self.eventgreaterthan = eventgreaterthan
        # the number of times the event has to have occurred less than
        self.eventlessthan = eventlessthan

    def check(self):
        times = classvar.player.getstoryevent(self.eventname)
        return times>self.eventgreaterthan and times<self.eventlessthan
