import variables, graphics, enemies
from random import randint
from Map import Map
from graphics import snowland
from Exit import Exit
from Rock import Rock

snowentrance = Map(snowland(650, 500, True), [])
snowentrance.populate_with("snowpinetree", randint(4, 10))

snowentrance.exitareas = [Exit("right", False, "jeremyhome", "left", "same"),
                          Exit("left", False, "snowarea1", "right", "same")]
snowentrance.enemies = enemies.snowenemies

snowarea1 = Map(snowland(700, 500), [])
snowarea1.populate_with("snowpinetree", randint(10, 15))

snowarea1.exitareas = [Exit("right", False, "snowentrance", "left", "same")]
