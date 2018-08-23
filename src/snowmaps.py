import variables
from Map import Map
from graphics import snowland
from Exit import Exit

snowentrance = Map(snowland(650, 500), [])

snowentrance.exitareas = [Exit("right", False, "jeremyhome", "left", "same")]
