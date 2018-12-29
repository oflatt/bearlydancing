import pygame, unittest, random

from rdrawmodify import findanchor

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
    

if __name__ == "__main__":
    unittest.main()    


