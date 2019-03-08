import math

from graphics import flowerpot, makeplant


from .PlantNode import PlantNode
from .PlantShape import PlantShape
from .constants import potwidth


potpic = flowerpot(potwidth)


# make a list of stems for use in ungrown plants
stem_list = [(0,0)]
for x in range(10):
    stem_list.append((x, 0))
stem_plant_shape = PlantShape(stem_list, (0, 200, 0), (0, 120, 0))
stem_node = PlantNode([stem_plant_shape], 1, (0, 0), math.pi/10)

random_stems = []

for x in range(5):
    random_stems.append(makeplant(stem_node))
