import math, random

from graphics import flowerpot, makeplant


from .PlantNode import PlantNode
from .PlantShape import PlantShape
from .constants import potwidth


potpics = []
for x in range(10):
    potpics.append(flowerpot(potwidth))

def randompotpic():
    return random.choice(potpics)

# make a list of stems for use in ungrown plants
stem_list = [(0,0)]
for x in range(10):
    stem_list.append((x, 0))
stem_plant_shape = PlantShape(stem_list, (0, 200, 0), (0, 120, 0))
stem_node = PlantNode([stem_plant_shape], 1, math.pi/10)

random_stems = []

for x in range(5):
    random_stems.append(makeplant(stem_node))
