import unittest, math

from rdraw.pointlist import rotatepointlist, listangleatindex
from equality import assert_compare_within


class PointListTests(unittest.TestCase):

    def test_rotate(self):
        l = [(0, 0), (0, -1.0), (0, -2.0)]
        lrotated = rotatepointlist(l, math.pi/2)
        assert_compare_within(lrotated, [(0.0,0.0), (-1.0, 0.0), (-2.0, 0.0)])

        lrotated = rotatepointlist(l, math.pi*3/2 + math.pi/4, offsetresult = (4.5, -9))
        assert_compare_within(lrotated, [(0.0+4.5, 0.0-9), (math.sqrt(2)/2+4.5, -math.sqrt(2)/2-9), (math.sqrt(2)+4.5, -math.sqrt(2)-9)])

    
    def test_angleatindex(self):
        l = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)]

        assert_compare_within(listangleatindex(l, 0), math.pi)

        assert_compare_within(listangleatindex(l, 1), math.pi/2)
        assert_compare_within(listangleatindex(l, 2), 0.0)

        l = [(0.0, 0.0), (0.0, -1.0), (1.0, 0.0)]
        assert_compare_within(listangleatindex(l, 0), math.pi+math.pi/4)
        l = [(1.0, 0.0), (0.0, 0.0), (0.0, -1.0)]
        assert_compare_within(listangleatindex(l, 1), math.pi+math.pi/4)
        l = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
        assert_compare_within(listangleatindex(l, 0), math.pi-math.pi/4)

        l = [(0.0, 0.0), (1.0, -1.0), (1.5, -1.5)]
        assert_compare_within(listangleatindex(l, 1), math.pi/2+math.pi/4)

        l = [(0.0, 1.0), (1.0, 0.0), (1.25, 0.25)]
        assert_compare_within(listangleatindex(l, 1), math.pi/2)

        l = [(2.0, 1.0), (1.0, 2.0), (0.0, 1.0)]
        assert_compare_within(listangleatindex(l, 1), math.pi+math.pi/2)
