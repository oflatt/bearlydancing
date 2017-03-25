#!/usr/bin/python
# Oliver Flatt works on Classes
import variables, pygame, classvar, random, stathandeling, math
from Battle import Battle


class Map():
    startpoint = [10, 10]  # xy coordinates of spawn point
    exitareas = []  # list of exit
    colliderects = []  # list of invisible Rect for collision
    enemies = []  # list of possible enemy encounters
    lvrange = [1]
    last_encounter_check = 0
    #use last pos takes priority over teleportation (with newx and newy in exits)
    #It means when re-entering a map it teleports the player to the last pos they were when they were last in the map
    uselastposq = False
    lastx = None #none until you exit the map for the first time
    lasty = None
    encounterchecksnotactivated = 0
    conversations = []  # list of conversation on the map
    isscaled = False  # if scale stuff has been called

    def __init__(self, base, terrain):
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
        if mapw < variables.width or maph < variables.height:
            self.map_scale_offset = variables.width / smaller
        else:
            self.map_scale_offset = 1

    def draw_map(self, b, t):
        i = b
        for x in range(0, len(t)):
            r = t[x]
            i.blit(r.base["img"], [r.x, r.y])
        return i

    def scale_stuff(self):
        for x in range(len(self.terrain)):
            self.terrain[x].scale_by_offset(self.map_scale_offset)
        scaled_base = pygame.transform.scale(self.base["img"], [int(self.base["w"] * self.map_scale_offset),
                                                                int(self.base["h"] * self.map_scale_offset)])
        self.finalimage = self.draw_map(scaled_base, self.terrain)
        for x in range(0, len(self.exitareas)):
            self.exitareas[x].scale_by_offset(self.map_scale_offset)
        for x in range(0, len(self.conversations)):
            self.conversations[x].scale_by_offset(self.map_scale_offset)
        for x in self.colliderects:
            x.x *= self.map_scale_offset
            x.y *= self.map_scale_offset
            x.width *= self.map_scale_offset
            x.height *= self.map_scale_offset
        self.isscaled = True

    # x and y are the player's x and y pos
    def draw(self, x, y):
        # check if scale stuff needs to be called- only called for the first map
        if not self.isscaled:
            self.scale_stuff()

        w = self.finalimage.get_width()
        h = self.finalimage.get_height()
        if x < variables.hh:  # if it is in the left side of the map
            drawx = 0  # do not scroll the map at all
        elif x > (w - variables.hh):  # if it is on the right side of the map
            drawx = w - variables.height  # set it to the maximum scroll
        else:
            drawx = x - variables.hh  # otherwise, scroll it by pos (accounting for the initial non-scolling area
        if y < variables.hh:  # same but for y pos
            drawy = 0
        elif y > (h - variables.hh):
            drawy = h - variables.height
        else:
            drawy = y - variables.hh

        variables.screen.blit(self.finalimage, [-drawx, -drawy])

        # draw button above exits and conversations
        e = self.checkexit()
        pw = classvar.player.normal_width / 2
        if not e == False:
            self.draw_interation_button(classvar.player.xpos + classvar.player.current_display.get_width() / 2 - pw / 2,
                                        classvar.player.ypos - pw, pw)
        c = self.checkconversation()
        if not c == False and c.isbutton:
            self.draw_interation_button(classvar.player.xpos + classvar.player.current_display.get_width() / 2 - pw / 2,
                                        classvar.player.ypos - pw, pw)

    def draw_foreground(self):
        # detect if within the foreground range
        playerrect = pygame.Rect(classvar.player.xpos, classvar.player.ypos, classvar.player.normal_width,
                                 classvar.player.normal_height)
        for r in self.terrain:
            if (not r.background_range.colliderect(playerrect)):
                r.draw()

    def draw_interation_button(self, xpos, ypos, width):
        pygame.draw.ellipse(variables.screen, variables.WHITE, [xpos, ypos, width, width])
        pygame.draw.ellipse(variables.screen, variables.GRAY,
                            [xpos + width / 4, ypos + width / 4, width / 2, width / 2])

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
