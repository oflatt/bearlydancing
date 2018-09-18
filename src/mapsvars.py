import variables, classvar
from EventRequirement import EventRequirement
from graphics import GR


# Coordinates for maps are based on the base of each map respectively
honeyw = GR["honeyside0"]["w"]
honeyh = GR["honeyside0"]["h"]
honeyfeetheight = honeyh * (3 / 29)
extraarea = 50

# p is the width of a pixel
p = 1

treecollidesection = variables.TREECOLLIDESECTION


# conversation is the conversation before the reward is given
# specialbattle is a conversation special_battle, which is an enemy
def makeconversationreward(conversation, specialbattle, rewardname):
    ename = specialbattle.name
    beatevent = "beat" + ename

    # set up event with the specialbattle
    specialbattle.storyeventsonwin = [beatevent]
    
    cevent = "beat" + ename + "c"
    conversation.storyevent = cevent
    # make conversation only go once based on own event
    conversation.eventrequirements.append(EventRequirement(beatevent))
    conversation.eventrequirements.append(EventRequirement(cevent, -1, 1))
    conversation.area = [0,0,10000, 10000]
    conversation.isbutton = False
    conversation.reward = rewardname
    
