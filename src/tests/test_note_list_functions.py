import unittest

from notelistfunctions import *
from Note import Note


class NoteListTests(unittest.TestCase):

    def test_any_collide(self):
        collidelist = [Note(0, 0, 1), Note(0, 2, 1), Note(0, 2.5, 3)]
        self.assertEqual(2, anynotescollide(collidelist))

    def test_any_collide_no_collide(self):
        collidelist = [Note(0, 0, 1), Note(0, 2, 1), Note(2, 2.5, 3)]
        self.assertEqual(None, anynotescollide(collidelist))

    def test_haschordsgreaterthan(self):
        l = [Note(0, 0, 3), Note(0, 3, 1), Note(2, 3, 1), Note(0,3.2,3)]
        self.assertEqual(3, haschordsgreaterthan(l, 1))
        self.assertEqual(None, haschordsgreaterthan(l, 2))

