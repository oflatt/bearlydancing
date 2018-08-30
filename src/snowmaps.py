import variables, graphics
from random import randint
from Map import Map
from graphics import snowland
from Exit import Exit
from Rock import Rock

snowentrance = Map(snowland(650, 500), [])
snowentrance.populate_with("snowpinetree", randint(4, 10))

snowentrance.exitareas = [Exit("right", False, "jeremyhome", "left", "same")]
