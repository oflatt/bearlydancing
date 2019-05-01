
from FrozenClass import FrozenClass

class OutsideBaseImage(FrozenClass):

    def __init__(self, image_name, collision_areas):
        self.image_name = image_name
        self.collision_areas = collision_areas
        self._freeze()
