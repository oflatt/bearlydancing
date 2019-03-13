import unittest, math

from growgame.crossplants import randomcombinecolors
from equality import assert_compare_within


class PointListTests(unittest.TestCase):

    # test the jank recombination of primary colors
    def test_combinecolors(self):
        # blue and red make magenta
        assert_compare_within(randomcombinecolors((255, 0,0), (0,0,255), 0.5),
                              (255, 0, 255), within = 2)

        # yellow and red make orange
        assert_compare_within(randomcombinecolors((255, 255, 0), (255, 0, 0), 0.5),
                              (255, 127, 0), within = 1)

        # yellow and blue make green
        #print(randomcombinecolors((255, 255, 0), (0, 0, 255), 0.5))
        assert_compare_within(randomcombinecolors((255, 255, 0), (0, 0, 255), 0.5),
                              (0, 255, 180), within = 1)
