#!/usr/bin/python
# Oliver Flatt works on Classes
import variables, pygame, classvar, random, stathandeling, math, graphics
from Battle import Battle
from graphics import viewfactorrounded
from Rock import Rock
from pygame import Mask

extraarea = 50
TREEMASK = Mask((variables.TREEWIDTH, variables.TREEHEIGHT))
BASEMASK = Mask((25, 15))
BASEMASK.fill()
TREEMASK.draw(BASEMASK,
              (int(variables.TREEWIDTH)-13, variables.TREEHEIGHT-15))

class Map():

    def __init__(self, base, terrain, leftbound = True, rightbound = True, topbound = True, bottombound = True):
        self.topbound = topbound
        self.rightbound = rightbound
        self.bottombound = bottombound
        self.leftbound = leftbound
        self.base = base
        # terrain is a list of Rock
        self.terrain = terrain
        # final image is an actual image, not a dict
        self.finalimage = pygame.Surface([10, 10])
        mapw = base["w"]
        maph = base["h"]
        if mapw < maph:
            smaller = mapw
        else:
            smaller = maph
        if maph < variables.height:
            self.map_scale_offset = variables.height / smaller
        else:
            self.map_scale_offset = 1

        self.lastx = None #none until you exit the map for the first time
        self.lasty = None

        self.startpoint = [10, 10]  # xy coordinates of spawn point
        self.exitareas = []  # list of exit
        self.colliderects = []  # list of invisible Rect for collision
        self.enemies = []  # list of possible enemy encounters
        self.lvrange = [1]
        self.last_encounter_check = 0
        #use last pos takes priority over teleportation (with newx and newy in exits)
        #It means when re-entering a map it teleports the player to the last pos they were when they were last in the map
        self.uselastposq = False
        self.encounterchecksnotactivated = 0
        self.conversations = []  # list of conversation on the map
        self.isscaled = False  # if scale stuff has been called
        self.screenxoffset = 0 # this is if the map width is less than the screen width

        self.playerenabledp = True

    # puts a number of one kind of object into the map randomly
    # if the randomly generated coordinates collide with anything, they are skipped
    # can only be used before the scaling happens
    def populate_with(self, rocktype, number):
        width = self.base["w"]
        height = self.base["h"]
        pwidth = viewfactorrounded
        treewscaled = variables.TREEWIDTH*pwidth
        treehscaled = variables.TREEHEIGHT*pwidth
        yconstraints = [-int(treehscaled/2), height-int(treehscaled/2)]
        xconstraints = [0, width-treewscaled]
        x_min_distance = 6*pwidth
        y_min_distance = 8*pwidth
        rockp = rocktype == "greyrock" or rocktype == "grey rock" or rocktype == "rock"

        if rockp:
            xconstraints = [0, width-(20*pwidth)]
            yconstraints = [0, height-(30*pwidth)]

        # this compares unscaled coordinates
        def collidewithonep(xpos, ypos, rock):
            #don't do collision with placing rocks
            if not rockp:
                rmask = TREEMASK
                overlapp = rmask.overlap(rock.mask, (int((xpos-rock.x)/pwidth), int((ypos-rock.y)/pwidth)))
            else:
                overlapp = False
            #if overlapp:
            #    print("got collision")
            return overlapp
        
        def collidesp(xpos, ypos, rocklist):
            collisiontracker = False
            if not collisiontracker:
                for r in self.terrain:
                    if collidewithonep(xpos, ypos, r):
                        collisiontracker = True
                        break
            if not collisiontracker:
                for r in rocklist:
                    if collidewithonep(xpos, ypos, r):
                        collisiontracker = True
                        break
            return collisiontracker

        # first generate the y-values for the rocks
        ypositions = [random.randint(yconstraints[0],yconstraints[1]) for _ in range(number)]
        newrocks = []
        for randy in ypositions:
            randx = random.randint(xconstraints[0], xconstraints[1])
            if not collidesp(randx, randy, newrocks):
                if rocktype == "pinetree" or rocktype == "pine tree":
                    newrocks.append(Rock(graphics.pinetree(), randx, randy, variables.TREECOLLIDESECTION))
                if rockp:
                    newrocks.append(Rock(graphics.greyrock(), randx, randy, [0,0,1,1]))
                    
        self.terrain.extend(newrocks)
        
        
            
    def scale_stuff(self):
        honeywidth = classvar.player.left_animation.pics[0]["w"]
        honeyheight = classvar.player.left_animation.pics[0]["h"]
        halfhoneyw = int(honeywidth/2)*self.map_scale_offset
        halfhoneyh = int(honeyheight/2)*self.map_scale_offset
        mapw = self.base["w"]
        maph = self.base["h"]
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
        for x in range(len(self.terrain)):
            self.terrain[x].scale_by_offset(self.map_scale_offset)
        newwidth = int(self.base["w"] * self.map_scale_offset)
        newheight = int(self.base["h"] * self.map_scale_offset)
        self.finalimage = pygame.transform.scale(self.base["img"], [newwidth,
                                                                    newheight])
        for x in range(0, len(self.exitareas)):
            self.exitareas[x].scale_by_offset(self.map_scale_offset)
        for x in range(0, len(self.conversations)):
            self.conversations[x].scale_by_offset(self.map_scale_offset)
        for x in self.colliderects:
            x.x *= self.map_scale_offset
            x.y *= self.map_scale_offset
            x.width *= self.map_scale_offset
            x.height *= self.map_scale_offset
        self.startpoint[0] *= self.map_scale_offset
        self.startpoint[1] *= self.map_scale_offset
        self.isscaled = True

        # compute screenxoffset if needed
        if newwidth < variables.width:
            self.screenxoffset = int((variables.width-newwidth)/2)

        #also sort the rocks by the y-position of the top of their background range
        def getbaseypos(rock):
            return rock.background_range.y
        self.terrain.sort(key=getbaseypos)

    def draw_background(self, drawpos):
        offset = [-drawpos[0], -drawpos[1]]
        variables.screen.blit(self.finalimage, offset)

        # detect if within the foreground range
        playerrect = pygame.Rect(classvar.player.xpos, classvar.player.ypos, classvar.player.normal_width,
                                 classvar.player.normal_height)

        for r in self.terrain:
            if r.background_range.colliderect(playerrect):
                r.draw(offset)
        
    # x and y are the player's x and y pos
    def draw(self, drawpos):
        self.draw_background(drawpos)

        # draw button above exits and conversations
        pw = classvar.player.normal_width / 2
        buttonx = classvar.player.xpos + classvar.player.normal_width / 2 - pw / 2 - drawpos[0]
        buttony = classvar.player.ypos - pw - drawpos[1]
        
        e = self.checkexit()
        if not e == False and e.showbutton:
            self.draw_interation_button(buttonx, buttony, pw)
        c = self.checkconversation()
        if not c == False and c.isbutton and c.showbutton:
            self.draw_interation_button(buttonx, buttony, pw)

    def draw_foreground(self, drawpos):
        rockoffset = [-drawpos[0], -drawpos[1]]
        # detect if within the foreground range
        playerrect = pygame.Rect(classvar.player.xpos, classvar.player.ypos, classvar.player.normal_width,
                                 classvar.player.normal_height)
        for r in self.terrain:
            if (not r.background_range.colliderect(playerrect)):
                r.draw(rockoffset)

    def draw_interation_button(self, xpos, ypos, width):
        pygame.draw.ellipse(variables.screen, variables.WHITE, [xpos, ypos, width, width])
        pygame.draw.ellipse(variables.screen, variables.GRAY,
                            [xpos + width / 4, ypos + width / 4, width / 2, width / 2])

    def changerock(self,rockname):
        if rockname != None:
            for rock in self.terrain:
                if rock.name == rockname:
                    rock.nextanimation()

    def checkexit(self):
        currentexit = False
        for x in range(0, len(self.exitareas)):
            e = self.exitareas[x]
            p = classvar.player
            if (p.xpos + p.normal_width) >= e.area[0] and p.xpos <= (e.area[0] + e.area[2]) \
                    and (p.ypos + p.normal_height) >= e.area[1] and p.ypos <= (e.area[1] + e.area[3]):
                currentexit = e
                break
        #if there is a conversation, do that instead
        if currentexit:
            if currentexit.conversation != None:
                e = currentexit.conversation
                if e.part_of_story == "none" or e.part_of_story == classvar.player.storyprogress:
                    if classvar.player.storyprogress in e.storyrequirement or len(e.storyrequirement) == 0:
                        currentexit = e

        return currentexit

    def on_tick(self):
        if len(self.enemies) > 0:
            if variables.settings.current_time - self.last_encounter_check >= variables.encounter_check_rate and classvar.player.ismoving():
                self.checkenemy()
                self.last_encounter_check = variables.settings.current_time

    def checkconversation(self):
        currentconversation = False
        for x in range(0, len(self.conversations)):
            e = self.conversations[x]
            p = classvar.player
            if (p.xpos + p.normal_width) >= e.area[0] and p.xpos <= (e.area[0] + e.area[2]) \
                    and (p.ypos + p.normal_height) >= e.area[1] and p.ypos <= (e.area[1] + e.area[3]):
                # then check if it is part of main storyline
                if e.part_of_story == "none" or e.part_of_story == classvar.player.storyprogress:
                    if classvar.player.storyprogress in e.storyrequirement or len(e.storyrequirement) == 0:
                        currentconversation = e
                        break
        return currentconversation

    def checkenemy(self):
        # goes through the list of enemies, adding up all the encounter chances up until that list number
        def collect_encounter_chances(list_placement):
            chance = 0
            for x in range(list_placement + 1):
                chance += self.enemies[x].rarity
            return chance

        # if the random chance activates
        if random.random() / (math.sqrt(self.encounterchecksnotactivated) + 0.2) < variables.encounter_chance:
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
                variables.settings.state = "battle"
                classvar.player.change_of_state()
                if (len(self.lvrange) > 1):
                    currentenemy.lv = random.randint(self.lvrange[0], self.lvrange[1])
                else:
                    currentenemy.lv = self.lvrange[0]
                currentenemy.health = stathandeling.max_health(currentenemy.lv)
                classvar.battle = Battle(currentenemy)
        else:
            self.encounterchecksnotactivated += 1
