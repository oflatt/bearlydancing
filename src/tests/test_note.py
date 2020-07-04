import unittest

import Note


# tests
class NoteTests(unittest.TestCase):
    
    def test_compare_around(self):
        self.assertTrue(compare_around(28.1, 0, 0.1, 1))
        self.assertTrue(compare_around(28.5, 0.4, 0.2, 1))
    


