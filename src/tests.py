import pygame, unittest, random, sys, copy



from rdraw.rdrawmodify import findanchor

s = pygame.Surface((20, 20), pygame.SRCALPHA)

s.set_at((9,10), (255,0,0,255))

p = pygame.surfarray.pixels2d(s)
p[9][10] = s.map_rgb((255,255,0,255))



class AnchorTests(unittest.TestCase):

    def test_normal(self):
        s = pygame.Surface((20, 20), pygame.SRCALPHA)
        s.set_at((9, 9), (255,255,0,255))
        s.set_at((9,10), (255,0,0,255))
        
        anchor = findanchor(s)
        self.assertEqual(anchor, (9, 10))
        

    def test_randomfill(self):
        s = pygame.Surface((20, 20), pygame.SRCALPHA)
        fillist = []
        for x in range(5):
            fillist.append((random.randint(0, 9), random.randint(0, 10)))

        pygame.draw.polygon(s, (255,0,0,255), fillist)
        
        s.set_at((9,10), (255,0,0,255))
        
        anchor = findanchor(s)
        self.assertEqual(anchor, (9, 10))


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
        
        

    
        
if __name__ == "__main__":
    
    unittest.main(argv=["--novideomode"])    


