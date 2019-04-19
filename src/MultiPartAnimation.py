
from typing import List

import variables
from graphics import getpic, addsurfaceGR


# make a subpart and find its offset
class AnimationPart():

    def __init__(self, picname: str):
        unclipped = getpic(picname)
        bounds = unclipped.get_bounding_rect()
        cropped = unclipped.subsurface(bounds).copy()
        cropped_name = picname + "_cropped"
        addsurfaceGR(cropped, cropped_name)
        self.picname = cropped_name
        self.rel_x = bounds.x
        self.rel_y = bounds.y


class MultiPartAnimation():

    
    # The outer list has all the lists that are drawn simultaneously, in order.
    # The inner list is all the variations for a part (AnimationParts)
    def __init__(self, parts_nested : List[List[AnimationPart]], unscaled_width, unscaled_height):

        self.parts_nested = parts_nested
        self.updatealwaysbattle = False

        self.unscaled_width = unscaled_width
        self.unscaled_height = unscaled_height
        
        # which animationpart currently is used for each part
        self.frames : List[int] = [0] * len(self.parts_nested)
        
    def change_frame(self, framenum : int, newframe = None):
        if newframe == None:
            self.frames[framenum] = (self.frames[framenum] + 1) % len(self.parts_nested[framenum])
        elif newframe >= len(self.parts_nested[framenum]):
            raise ValueError("bad new frame for this framenum")
        else:
            self.frames[framenum] = newframe

    def reset(self):
        self.frames : List[int] = [0] * len(self.parts_nested)


    # draws but does not update the screen
    def draw_topright(self, screen, height, topoffset = 0, rightoffset = 0):
        scaling_factor = height/float(self.unscaled_height)
        
        # loop through all the pictures
        for partindex in range(len(self.frames)):
            animpart = self.parts_nested[partindex][self.frames[partindex]]
            
            epic = getpic(animpart.picname, scale = scaling_factor)
            
            screen.blit(epic, [variables.width - self.unscaled_width*scaling_factor + animpart.rel_x*scaling_factor+rightoffset, 0 + animpart.rel_y*scaling_factor+topoffset])

        
    def update_topright(self, height, topoffset = 0, rightoffset= 0):
        scaling_factor = height/float(self.unscaled_height)
        variables.dirtyrects.append(Rect(variables.width-self.unscaled_width*scaling_factor+rightoffset,
                                         0,
                                         self.unscaled_width*scaling_factor,
                                         self.unscaled_height*scaling_factor))

        
    def pic_width(self, height):
        scaling_factor = height/float(self.unscaled_height)
        return self.unscaled_width*scaling_factor
    
