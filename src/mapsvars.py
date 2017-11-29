import variables, classvar
from graphics import GR


STORYORDER = ["bed","letter", "that racoon", "greenie", "good job", "the end"]
# a list of story parts that the player should have no control over the bear in and bear is invisible in
DISABLEPLAYERSTORY = ["bed", "that racoon"]

def getpartofstory(storyname):
    return STORYORDER.index(storyname)

def playerenabledp():
    return not STORYORDER[classvar.player.storyprogress] in DISABLEPLAYERSTORY

# Coordinates for maps are based on the base of each map respectively
honeyw = GR["honeyside0"]["w"]
honeyh = GR["honeyside0"]["h"]
honeyfeetheight = honeyh * (3 / 29)
extraarea = 50
insidewidth = GR["honeyhouseinside"]["w"]
insideheight = GR["honeyhouseinside"]["h"]
# p is the width of a pixel
p = variables.displayscale

treecollidesection = variables.TREECOLLIDESECTION
