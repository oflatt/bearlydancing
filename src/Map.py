 #!/usr/bin/python

import pygame, random, math
from pygame import Mask, Rect


import variables, classvar, stathandeling, graphics, devoptions, initiatebattle
from graphics import getpic, GR
from Rock import Rock
from FrozenClass import FrozenClass
from Animation import Animation
from Wind import Wind
from WindEffect import WindEffect
from WindShift import WindShift
from OutsideBaseImage import OutsideBaseImage

extraarea = 50
interact = Animation(["interactionbutton0", "interactionbutton1"], 1000)

class Map(FrozenClass):

    def __init__(self, base, terrain, leftbound = True, rightbound = True, topbound = True, bottombound = True, shadowsp = True):
        self.topbound = topbound
        self.rightbound = rightbound
        self.bottombound = bottombound
        self.leftbound = leftbound

        # base is a string for a pic in GR or a OutsideBaseImage
        if type(base) == OutsideBaseImage:
            self.map_base_collision_areas = base.collision_areas
            base = base.image_name
        else:
            self.map_base_collision_areas = []
            
        self.base = base
            
        
        # terrain is a list of Rock
        self.terrain = terrain
        # final image is the name of the image for the background
        self.finalimage = base

        self.lastx = None #none until you exit the map for the first time
        self.lasty = None

        self.startpoint = [10, 10]  # xy coordinates of spawn point
        self.exitareas = []  # list of exit
        self.colliderects = []  # list of invisible Rect for collision
        self.enemies = []  # list of possible enemy encounters
        self.lvrange = [1]
        self.last_encounter_check = 0
        # use last pos takes priority over teleportation (with newx and newy in exits)
        #It means when re-entering a map it teleports the player to the last pos they were when they were last in the map
        self.uselastposq = False
        self.encounterchecksnotactivated = 0
        self.conversations = []  # list of conversation on the map
        self.isscaled = False  # if scale stuff has been called
        
        self.playerenabledp = True

        # if the map has shadows, which also implies that it can spawn wind
        self.shadowsp = shadowsp

        self.windlist = []
        self.windeffect = WindEffect()
        
        self.lastwindspawncheck = 0
        
        self._freeze()

    def map_width(self):
        return GR[self.finalimage]["w"]

    def map_height(self):
        return GR[self.finalimage]["h"]

    # clear wind stuff before saving
    def preparetosave(self):
        self.windlist = []
        self.windeffect = WindEffect()
        for r in self.terrain:
            r.windeffect = WindEffect()

    # this describes if the map should be scaled up because it doesn't fit well in the screen
    def map_scale_offset(self):
        mapw = GR[self.base]["w"] * variables.displayscale
        maph = GR[self.base]["h"] * variables.displayscale
        if mapw < maph:
            smaller = mapw
        else:
            smaller = maph
        if maph < variables.height:
            return variables.height / smaller
        else:
            return 1

    def clearrockfunctions(self):
        for r in self.terrain:
            r.clearfunctions()


    def valid_populate_rockp(self, xpos, ypos, new_rock_mask, rocklist, colliderects, terraincollidep):
        new_rock_width, new_rock_height = new_rock_mask.get_size()
        
        def collidewithonep(xpos, ypos, existing_rock):
            return new_rock_mask.overlap(existing_rock.get_mask(),
                                         [int(existing_rock.x-xpos),
                                          int(existing_rock.y-ypos)])

        def maskwithrectcollidep(xpos, ypos, mask, rect):
            maskrects = mask.get_bounding_rects()
            for colliderect in maskrects:
                colliderect.x += xpos
                colliderect.y += ypos
                devoptions.devprint(colliderect)
                if rect.colliderect(colliderect):
                    return True
            return False
        
        
        collisiontracker = False

        # check if it collides with the colliderects given to the populate function. These colliderects check the entire box of the rock, not just the mask
        new_rock_rect = Rect(xpos, ypos, new_rock_width, new_rock_height)
        for crect in colliderects:
            if crect.colliderect(new_rock_rect):
                collisiontracker = True
                break

        # check if it collides with the base collisions (this is to prevent trees growing on the path)
        for crect in self.map_base_collision_areas:
            if maskwithrectcollidep(xpos, ypos, new_rock_mask, crect):
                collisiontracker = True
                break

        # for grey rocks, don't collide with other terrain
        if terraincollidep:
            # check against the terrain
            if not collisiontracker:
                for existing_rock in self.terrain:
                    if collidewithonep(xpos, ypos, existing_rock):
                        collisiontracker = True
                        break

            # check against the rocklist given (new rocks)
            if not collisiontracker:
                for existing_rock in rocklist:
                    if collidewithonep(xpos, ypos, existing_rock):
                        collisiontracker = True
                        break

        return not collisiontracker

    # puts a number of one kind of object into the map randomly
    # call with greyrocks before trees
    # if the randomly generated coordinates collide with anything, they are skipped
    # colliderects is a list of rects in which rocks cannot be spawned- no part of it can be displayed in it
    def populate_with(self, rocktype, number_to_populate_with, colliderects = []):
        terraincollidep = True
        map_width = GR[self.base]["w"]
        map_height = GR[self.base]["h"]
        
        treew = variables.TREEWIDTH
        treeh = variables.TREEHEIGHT
        x_min_distance = 6
        y_min_distance = 8
        
        greyrockp = rocktype == "greyrock" or rocktype == "grey rock" or rocktype == "rock"
        pinetreep = rocktype == "pinetree" or rocktype == "pine tree" or rocktype == "snowpinetree"
        flowerp = rocktype == "flower"

        rock_collide_section = None
        rock_generating_function = None
        if pinetreep:
            if rocktype == "snowpinetree":
                rock_generating_function = graphics.snowpinetree
                rock_collide_section = variables.TREECOLLIDESECTION
            else:
                rock_generating_function = graphics.pinetree
                rock_collide_section = variables.TREECOLLIDESECTION
        elif greyrockp:
            terraincollidep = False
            rock_generating_function = graphics.greyrock
            rock_collide_section = variables.ROCKCOLLIDESECTION
        elif flowerp:
            rock_generating_function = graphics.flower
            rock_collide_section = variables.FLOWERCOLLIDESECTION
        else:
            raise Exception("unrecognized rock type " + rocktype + " for populate_with")


        # first generate the y-values for the rocks
        newrocks = []
        # cached potential rock is a cached call to the generating function
        cached_potential_graphic = None
        
        
        for rock_index in range(number_to_populate_with):

            if cached_potential_graphic == None:
                cached_potential_graphic = rock_generating_function()

            potential_width = graphics.getpic(cached_potential_graphic).get_width()
            potential_height = graphics.getpic(cached_potential_graphic).get_height()
            
            randx = random.randint(int(-potential_width/2), int(map_width + potential_width/2))
            randy = random.randint(int(-potential_height/2), int(map_height + potential_height/2))

            potential_rock_with_position = Rock(cached_potential_graphic, randx, randy, rock_collide_section)
            
            if self.valid_populate_rockp(randx, randy, potential_rock_with_position.get_mask(),
                                         newrocks, colliderects,
                                         terraincollidep):
                newrocks.append(potential_rock_with_position)
                cached_potential_graphic = None

        self.terrain.extend(newrocks)

    # now used to set the exitareas, for shorthand
    def scale_stuff(self):
        
        honeywidth = GR[classvar.player.left_animation.pics[0]]["w"]
        honeyheight = GR[classvar.player.left_animation.pics[0]]["h"]
        halfhoneyw = int(honeywidth/2)
        halfhoneyh = int(honeyheight/2)
        mapw = self.map_width()
        maph = self.map_height()
        
        for e in self.exitareas:
            if e.area == "left" or e.area == "l":
                self.leftbound = False
                e.area = [-extraarea-halfhoneyw, 0, extraarea, maph]
            elif e.area == "right" or e.area == "r":
                self.rightbound = False
                e.area = [mapw+halfhoneyw, 0, extraarea, maph]
            elif e.area == "up" or e.area == "u" or e.area == "top" or e.area == "t":
                self.topbound = False
                e.area = [0, -extraarea-halfhoneyh, mapw, extraarea]
            elif e.area == "down" or e.area == "d" or e.area == "bottom" or e.area == "b":
                self.bottombound = False
                e.area = [0, maph+halfhoneyh, mapw, extraarea]
                
        self.isscaled = True

                        
            
        #also sort the rocks by the y-position of the top of their background range
        def getbaseypos(rock):
            # if it has no background range, it would go in front of everything- so pick a large number
            if rock.background_range == None:
                return variables.height*10
            else:
                return rock.background_range.y
        
        self.terrain.sort(key=getbaseypos)

    # drawpos comes from the player's mapdrawx and mapdrawy
    def draw_background(self, drawpos):
        offset = [-drawpos[0], -drawpos[1]]

        if self.screenxoffset() == 0:
            mapbaserect = Rect(drawpos[0], drawpos[1], self.map_width()*variables.compscale()+1, self.map_height()*variables.compscale()+1)
            variables.screen.blit(getpic(self.finalimage, variables.compscale()), (0,0), mapbaserect)
        else:
            variables.screen.blit(getpic(self.finalimage, variables.compscale()), (self.screenxoffset(),offset[1]))

        self.windeffect.draw(offset)

        
        playerrect = Rect(classvar.player.xpos, classvar.player.ypos, classvar.player.normal_width,
                                 classvar.player.normal_height)

        for r in self.terrain:
            if r.hiddenp:
                r.drawnp = True
            else:
                if r.background_range != None:
                    if r.background_range.colliderect(playerrect):
                        r.draw(self.shadowsp, offset = offset)
                        r.drawnp = True
                    else:
                        r.drawnp = False
                else:
                    r.drawnp = False
        
    # x and y are the player's x and y pos
    def draw(self, drawpos):
        self.draw_background(drawpos)

    def draw_foreground(self, drawpos):
            
        rockoffset = [-drawpos[0], -drawpos[1]]
        # detect if within the foreground range
        playerrect = Rect(classvar.player.xpos, classvar.player.ypos, classvar.player.normal_width,
                                 classvar.player.normal_height)
        for r in self.terrain:
            if not r.drawnp:
                r.draw(self.shadowsp, offset= rockoffset)

        # draw button above exits and conversations
        bwidth = 8*variables.compscale()
        buttonx = classvar.player.xpos + classvar.player.normal_width / 2
        buttony = classvar.player.ypos - 2
        buttonx = buttonx * variables.compscale() - drawpos[0] - bwidth/2
        buttony = buttony * variables.compscale() - drawpos[1] - bwidth
        e = self.checkexit()
        if not e == False and e.showbutton and e.isbutton:
            self.draw_interaction_button(buttonx, buttony)
        c = self.checkconversation()
        if not c == False and c.showbutton and c.isbutton:
            self.draw_interaction_button(buttonx, buttony)

    def draw_interaction_button(self, xpos, ypos):
        variables.dirtyrects.append(Rect(xpos, ypos, 8*variables.compscale(), 8*variables.compscale()))
        pic = getpic(interact.current_frame(), variables.compscale())
        variables.screen.blit(pic, [xpos, ypos])

    def checkexit(self):
        currentexit = False
        for x in range(0, len(self.exitareas)):
            e = self.exitareas[x]
            if e.activatedp():
                p = classvar.player
                if (p.xpos + p.normal_width) >= e.area[0] and p.xpos <= (e.area[0] + e.area[2]) \
                        and (p.ypos + p.normal_height) >= e.area[1] and p.ypos <= (e.area[1] + e.area[3]):
                    currentexit = e
                    break

        return currentexit

    def checkconversation(self):
        currentconversation = False
        for x in range(0, len(self.conversations)):
            e = self.conversations[x]
            p = classvar.player
            if e.activatedp():
                p = classvar.player
                if (p.xpos + p.normal_width) >= e.area[0] and p.xpos <= (e.area[0] + e.area[2]) \
                        and (p.ypos + p.normal_height) >= e.area[1] and p.ypos <= (e.area[1] + e.area[3]):
                    currentconversation = e
                    break
        return currentconversation

    def screenxoffset(self):
        drawwidth = self.map_width() * variables.compscale()
        
        if drawwidth < variables.width:
            return int((variables.width-drawwidth)/2)
        else:
            return 0

    def windtick(self):
        if self.shadowsp:

            # remove wind not on screen
            i = 0
            while i < len(self.windlist):
                wind = self.windlist[i]
                if wind.windpos() > self.map_width():
                    self.windlist.pop(i)
                else:
                    i = i + 1

            # chance to spawn new wind
            if (variables.settings.current_time-self.lastwindspawncheck) > variables.windcheckrate:
                self.lastwindspawncheck = variables.settings.current_time
                if len(self.windlist) <2:
                    if random.random() < variables.windchance:
                        self.windlist.append(Wind())

            
            # for all the winds, have a chance to spawn windshift on the grass and give all the rocks a chance to spawn a windshift
            for w in self.windlist:
                for r in self.terrain:
                    r.processwind(w)
                
                numbertogenerate = random.randint(2, 4)
                for x in range(numbertogenerate):
                    self.addwindshift(w)

    def addwindshift(self, w):
        mapbase = getpic(self.finalimage, variables.compscale())
        shiftrect = Rect(w.windpos()*variables.compscale(), random.randint(0, variables.height)*variables.compscale(), random.randint(3, 10)*variables.compscale(), random.randint(3, 10)*variables.compscale())

        newwindshift = self.windeffect.windshiftifgreen(mapbase, shiftrect)
        if newwindshift != None:
            newwindshift.xpos += 1
            newwindshift.ypos += random.randint(0, 1)
            self.windeffect.addwindshift(newwindshift)



    def on_tick(self):
        self.windtick()
         
        if len(self.enemies) > 0:
            if variables.settings.current_time - self.last_encounter_check >= variables.encounter_check_rate and classvar.player.ismoving():
                self.checkenemy()
                self.last_encounter_check = variables.settings.current_time

                
        for r in self.terrain:
            r.ontick()


    def checkenemy(self):
        # goes through the list of enemies, adding up all the encounter chances up until that list number
        def collect_encounter_chances(list_placement):
            chance = 0
            for x in range(list_placement + 1):
                chance += self.enemies[x].rarity
            return chance

        minencounterchecks = 20
        # if the random chance activates
        if self.encounterchecksnotactivated>minencounterchecks:
            if random.random() < variables.encounter_chance * math.sqrt(self.encounterchecksnotactivated-minencounterchecks):
                self.encounterchecksnotactivated = 0
                currentenemy = False

                # if all the chances are 1, just select a random enemy by default
                if (collect_encounter_chances(len(self.enemies) - 1) == len(self.enemies)):
                    currentenemy = random.choice(self.enemies)
                else:
                    random_factor = random.random()
                    for x in range(0, len(self.enemies)):
                        e = self.enemies[x]
                        # if the random factor is below all of the chances previously to now added up
                        if random_factor < collect_encounter_chances(x):
                            currentenemy = e
                            break

                if currentenemy:
                    if (len(self.lvrange) > 1):
                        currentenemy.lv = random.randint(self.lvrange[0], self.lvrange[1])
                    else:
                        currentenemy.lv = self.lvrange[0]
                    initiatebattle.initiatebattle(currentenemy)
            else:
                self.encounterchecksnotactivated += 1    
        else:
            self.encounterchecksnotactivated += 1

    def changerock(self,rockname):
        if rockname != None:
            for rock in self.terrain:
                if rock.name == rockname:
                    rock.nextanimation()

    def unhiderock(self, rockname):
        if rockname != None:
            for rock in self.terrain:
                if rock.name == rockname:
                    rock.unhide()

    def getrockbyname(self, rockname):
        returnrock = None
        if rockname != None:
            for rock in self.terrain:
                if rock.name == rockname:
                    returnrock = rock
                    break
        return returnrock
            
    def getconversation(self, name):
        c = None
        for i in range(len(self.conversations)):
            x = self.conversations[i]
            if x.name == name:
                c = x
                break
        if c == None:
            print("---------------------------")
            print("Error: No conversation in map called " + name)
            print("--------------------------")
            return None
        else:
            return c
