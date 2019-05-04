import unittest
from pygame import Mask, Rect


from Map import Map
from OutsideBaseImage import OutsideBaseImage

class PopulateTests(unittest.TestCase):

    def test_collide_with_horizontal_path(self):
        horizontal_collision_area = Rect(0, 100, 100, 20)
        test_map = Map(OutsideBaseImage("bad_image_name", [horizontal_collision_area]),
                       [])
        fill_mask = Mask((20, 20))
        new_rock_mask = Mask((30, 100))
        new_rock_mask.draw(fill_mask, (5, 100-20))
        self.assertEqual(True, test_map.valid_populate_rockp(20, 80, new_rock_mask, 30, 100, [], [], True))
