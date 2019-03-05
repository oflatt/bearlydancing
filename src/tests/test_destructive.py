import pygame, unittest, random, sys, copy


from DestructiveFrozenClass import DestructiveFrozenClass
class TestClassFrozen(DestructiveFrozenClass):

    def __init__(self, testarg):
        
        self.data = 1
        self.testarg = testarg
        
        self._freeze()

    def makedatapurple(self):
        return self.destructiveset("data","purple")
        
    def setdata(self, newdata):
        return self.destructiveset("data", newdata)
        
        
class DestructiveFrozenClassTests(unittest.TestCase):
    
    def test_frozen(self):
        t = TestClassFrozen("testargstring")
        
        self.assertEqual(t.data, 1)
        self.assertEqual(t.testarg, "testargstring")
        with self.assertRaises(TypeError):
            t.green = 3

    def test_parameter_method(self):
        t = TestClassFrozen("testargstring")
        
        self.assertEqual(t.data, 1)
        
        self.assertEqual(t.setdata(3).data, 3)

    def test_no_parameter_method(self):
        t = TestClassFrozen("testargstring")
        
        self.assertEqual(t.data, 1)
        t = t.makedatapurple()
        
        self.assertEqual(t.data, "purple")

    def test_set_method(self):
        t = TestClassFrozen("testargstring")
        t.data = 4
        with self.assertRaises(AttributeError):
            t.data

    def test_copying(self):
        t = TestClassFrozen("testargsstring")
        t = t.destructiveset("data", ["green"])
        copied = copy.copy(t)
        copied = copied.destructiveset("data", ["yellow"])
        self.assertEqual(t.data, ["green"])
        self.assertEqual(copied.data, ["yellow"])

        deepcopied = copy.deepcopy(t)
        t.data.append("blue")
        self.assertEqual(t.data, ["green", "blue"])
        self.assertEqual(deepcopied.data, ["green"])

    def test_nested(self):

        t = TestClassFrozen(TestClassFrozen("green"))
        
        t.data = 2
        with self.assertRaises(AttributeError):
            t.data

        t = TestClassFrozen(TestClassFrozen(t))
        t = t.destructiveset("data", TestClassFrozen("testargval"))
        self.assertEqual(1, t.data.data)
