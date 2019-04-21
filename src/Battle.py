#!/usr/bin/python
import variables, pygame, stathandeling, classvar, random, maps, randombeatmap, copy, conversations, play_sound
from ChoiceButtons import ChoiceButtons
from Button import Button
from Note import Note
from play_sound import scales, play_drum
from graphics import getpic, sscale, sscale_customfactor, getpicbyheight, GR, getTextPic, difficultytocolor, numofspecialmoveeffects, numofplayerframes, drawwave
from FrozenClass import FrozenClass
from pygame import Rect
from notelistfunctions import shorten_doubles
from Soundpack import max_sample
from initiatestate import returntoworld



def enemypic_height():
    return variables.height/4.0


# battle is the class that runs the battle- information about the game such as storyeventonwin is stored in enemy
class Battle(FrozenClass):

    def __init__(self, enemy):

        self.current_beatmap = 0
        self.damage_multiplier = 1
        self.beatmaps = []

        # keeps track of combo carrying over from last round
        self.runningcombo = 0

        # copy the enemy first to avoid editing originals
        self.enemy = copy.copy(enemy)
        self.enemy.reset()
        # offset enemy lv by difficulty
        self.enemy.lv += variables.settings.difficulty
        
        # state can be choose, dance, or attacking, win, lose, exp, got exp
        self.state = "choose"
        self.tutorialstate = None
        self.tutorialconversations = None
        
        
        # if the enemy's level is 0 and there have been no battles, the tutorial is triggered
        self.tutorialp = self.enemy.lv - variables.settings.difficulty == 0 and classvar.player.totalbattles == 0 and not variables.settings.dancepadmodep

        # if the accidental tutorial has not been activated and lv is above the threshhold, trigger accidental tutorial
        self.accidentaltutorialp = classvar.player.getstoryevent("accidentaltutorial") == 0 and self.enemy.lv >= variables.accidentallvthreshhold and not variables.settings.dancepadmodep

        # accidental tutorial will never be in the same battle as the normal tutorial
        # or if there are no accidentals in the beatmap
        if "noaccidentals" in self.enemy.beatmapspecs["rules"] or self.tutorialp:
            self.accidentaltutorialp = False
        elif self.accidentaltutorialp:
            # if we do activate the accidentaltutorial, set the tutorial and all the conversations
            self.tutorialp = True

        if self.tutorialp:
            if not self.accidentaltutorialp:
                # set all the conversations for the tutorial
                self.tutorialconversations = ["tutorialconversation1",
                                              "pressanow",
                                              "releaseanow",
                                              "endtutorial",
                                              "releasedearly"]
            else:
                # set all the accidental conversations
                self.tutorialconversations = ["accidentaltutorialintro",
                                              "presswnow",
                                              "releasewnow",
                                              "endtutorial",
                                              "releasedwearly"]
        
        
        # for attacking animation
        self.isplayernext = False  # if the player is currently being damaged
        self.oldenemyhealth = 0
        self.oldplayerhealth = 0
        self.newplayerhealth = 0
        self.newenemyhealth = 0

        # animation time is used for all animations
        self.animationtime = 0
        self.starttime = variables.settings.current_time

        # for win animation
        self.newexp = 0
        self.oldexp = 0

        # drawing buttons
        # extra space around dance to leave space for synth options
        self.battlechoice = ChoiceButtons(["   DANCE!   ", "leave", variables.settings.soundpack, self.getscalename()], 13 / 16)

        self.retrychoice = ChoiceButtons(["retry", "go home"], 13/16)

        # if pausetime is 0 it is not paused, otherwise it is paused and it records when it was paused
        self.pausetime = 0
        self.enemy.sethealth()

        self.playerframe = 0
        self.playercurrentanim = 0

        # the frame of the current special move effect
        self.currentspecialmove = 0
        # if we are currently doing a special move
        self.specialmovep = False

        self._freeze()

    def startnew(self):
        self.enemy.sethealth()
        classvar.player.heal()
        
        self.state = "dance"
        self.setfirstbeatmap()
        # clear screen
        variables.dirtyrects = [Rect(0,0,variables.width,variables.height)]

    def getscalename(self):
        if self.enemy.specialscale != None:
            return self.enemy.specialscale
        else:
            return classvar.player.scales[variables.settings.scaleindex]

    def setfirstbeatmap(self):
        self.enemy.beatmapspecs["lv"] = self.enemy.lv
        specs = self.enemy.beatmapspecs
        self.beatmaps = [randombeatmap.random_beatmap(specs)]
        self.initiatenewbeatmap()
        self.reset_time()
        self.reset_enemy()
        
        if self.tutorialp:
            self.tutorialstate = "starting"
            # if it is the tutorial, add two notes for the player to fail on, and change first note to a
            b = self.beatmaps[0]
            del b.notes[0]
            b.notes.insert(0, Note(0, b.notes[0].time, 3))

            # set it to be an accidental for the accidental tutorial
            if self.accidentaltutorialp:
                b.notes[0].accidentalp = True
            
            # first add ten to give space for the new notes
            for note in b.notes:
                note.time += 24
            b.notes[0].time -= 12

            if not self.accidentaltutorialp:
                b.notes = [Note(0, 1, 1), Note(1, 2, 1)] + b.notes
            else:
                newn = Note(0, 1, 2, accidentalp = True)
                b.notes.insert(0, newn)

    def reset_time(self):
        self.starttime = variables.settings.current_time
        self.beatmaps[self.current_beatmap].reset(self.starttime, True)
        

    def pause(self):
        self.pausetime = variables.settings.current_time
        if len(self.beatmaps) > 0:
            self.beatmaps[self.current_beatmap].pause()
            self.beatmaps[self.current_beatmap].reset_buttons()

    def unpause(self):
        self.starttime += variables.settings.current_time - self.pausetime
        self.pausetime = 0
        if len(self.beatmaps) > 0:
            self.beatmaps[self.current_beatmap].unpause()
        self.reset_enemy()

    def getcombo(self):
        currentb = self.beatmaps[self.current_beatmap]
        if len(currentb.scores)>currentb.currentcombo:
            self.runningcombo = 0
        return self.runningcombo + currentb.currentcombo

    def new_beatmaps(self):
        self.beatmaps = [randombeatmap.variation_of_notes_to_beatmap(self.beatmaps[0].originalnotes, self.beatmaps[0].tempo, self.enemy.beatmapspecs)]

    def initiatenewbeatmap(self):
        self.beatmaps[0].scale = scales[self.getscalename()]
        self.beatmaps[0].notes = shorten_doubles(self.beatmaps[0].notes)

    def next_beatmap(self):
        # first set the carry over for the combo
        self.runningcombo = self.runningcombo + self.beatmaps[self.current_beatmap].currentcombo
        
        if self.current_beatmap + 1 == len(self.beatmaps):
            self.new_beatmaps()
            self.current_beatmap = 0
        else:
            print("should only have one beatmap in the list!")
            self.current_beatmap += 1
            
        self.beatmaps[self.current_beatmap].reset(self.starttime, False)
        self.initiatenewbeatmap()
        self.reset_enemy()

    def reset_enemy(self):
        self.enemy.reset()
        if len(self.beatmaps) > 0:
            self.enemy.animation.framerate = self.beatmaps[self.current_beatmap].tempo
        self.enemy.animation.beginning_time = self.starttime

    def currentplayerframename(self):
        return "honeydance" + str(self.playercurrentanim) + "-" + str(self.playerframe)

    # returns the picture for the player and the rect for position in a tuple
    def getplayerpicandrect(self):
        playerpic = None
        if self.state != "dance":
            playerpic = getpicbyheight("honeydance0-0", variables.height/4)
        else:
            playerpic = getpicbyheight(self.currentplayerframename(), variables.height/4)
        playery = variables.height-playerpic.get_height()*1.5
        playerrect = Rect(variables.width-playerpic.get_width(), playery, playerpic.get_width(), variables.height-playery)
        return (playerpic, playerrect)

    def drawspecialmove(self):
        if self.specialmovep:
            playerr = self.getplayerpicandrect()[1]
            playerr.height = variables.height - playerr.y
            effectpic = getpicbyheight("specialmoveeffect" + str(self.currentspecialmove), playerr.height)
            variables.screen.blit(effectpic, playerr)

    def drawcombo(self):
        currentb=self.beatmaps[self.current_beatmap]
        totalcombo = self.getcombo()
        if totalcombo >= 10:
            combocolor = difficultytocolor(((totalcombo-9)/variables.numofrounds)/len(currentb.originalnotes))
            # find combo height based on the last time it was increased
            comboheight = variables.gettextsize()
            deltatcombo = variables.settings.current_time-currentb.timeoflastcomboaddition
            # threshhold in millis for making the resizing text animation
            comboanimthreshhold = 100
            if deltatcombo < comboanimthreshhold:
                comboheight *= 1 + (1 - deltatcombo/comboanimthreshhold)*0.5

            playerpicandrect = self.getplayerpicandrect()
                
            combopic = getTextPic("COMBO: " + str(totalcombo), comboheight, combocolor)
            combox = variables.width-combopic.get_width()
            combodif = combox-(variables.width-playerpicandrect[1].width)
            if combodif > 0:
                combox = combox-combodif/2
            comborect = Rect(combox, playerpicandrect[1].y-comboheight*1.5, combopic.get_width(), combopic.get_height())
            variables.screen.blit(combopic, comborect)
            variables.dirtyrects.append(comborect)

    def drawscoretable(self):
        scores = self.beatmaps[self.current_beatmap].scores
        if len(scores) > 0:
            percent = int((sum(scores) / (len(scores)*2))*10) / 10.0

            misses = 0
            okays = 0
            goods = 0
            perfects = 0
            for s in scores:
                if s == variables.miss_value:
                    misses += 1
                elif s == variables.ok_value:
                    okays += 1
                elif s == variables.good_value:
                    goods += 1
                elif s == variables.perfect_value:
                    perfects += 1

            tabletext = str(percent) + "%   perfects: " + str(perfects) + \
            "  goods: " + str(goods) + "  okays: " + str(okays) + \
            "  misses: " + str(misses) + "  total: " + str(len(scores))
            
            tablepic = getTextPic(tabletext, variables.gettextsize(), variables.WHITE)
            tabley = variables.height-tablepic.get_height()
            tablerect = Rect((variables.width-tablepic.get_width())/2, tabley, tablepic.get_width(), tablepic.get_height())
            
            variables.screen.blit(tablepic, tablerect)
            variables.dirtyrects.append(tablerect)
            
    def draw(self):
        if self.current_beatmap<len(self.beatmaps):
            currentb = self.beatmaps[self.current_beatmap]
        else:
            currentb = None
        h = variables.height
        w = variables.width
        b = h * 13 / 16
        p = classvar.player
        # background
        variables.screen.fill(variables.BLACK)

        # draw enemy first
        if self.state != "dance":
            self.enemy.animation.reset() # if not dancing, use first frame
            

        # draw enemy
        self.enemy.animation.draw_topright(variables.screen, enemypic_height())
            
        playerpicandrect = self.getplayerpicandrect()
        

        # draw the player
        if self.state == "dance":
            # draw the special animation behind the player
            self.drawspecialmove()
        variables.screen.blit(playerpicandrect[0], playerpicandrect[1])

        if currentb != None:
            # now draw the combo if necessary
            self.drawcombo()

        if self.enemy.animation.updatealwaysbattle:
            self.updatescreenforenemy()
        
        # draw beatmap
        if self.state == "dance":
            self.beatmaps[self.current_beatmap].draw()
        elif self.state == "attacking":
            self.beatmaps[self.current_beatmap].draw_pads()

        if self.state == "choose":
            # enemy name
            enemyname = variables.font.render("LV " + str(self.enemy.lv) + " " + self.enemy.name + " appears!", 0,
                                              variables.WHITE)
            enemynamescaled = sscale(enemyname)
            variables.screen.blit(enemynamescaled, [w / 2 - (enemynamescaled.get_width() / 2), h / 2])

            self.battlechoice.draw()
            
            # draw the wave above the battlechoice
            wavex = self.battlechoice.buttons[-2].x * variables.width
            # the height of the wave
            waveamp = (self.battlechoice.buttons[-2].height()*3/4) * 0.5
            
            wavelen = self.battlechoice.buttons[-2].width()*3/4
            wavey = self.battlechoice.buttons[-2].y*variables.height-waveamp
            loopbuffer = play_sound.all_tones[variables.settings.soundpack].loopbuffers[0]
            skiplen = (len(loopbuffer)/25)/wavelen
            drawwave(loopbuffer, skiplen, wavex, wavey, waveamp, wavelen, (255,255,255))

            # draw the scale above battlechoice
            firstscalex = self.battlechoice.buttons[-1].x * variables.width
            scalex = firstscalex
            scaley = self.battlechoice.buttons[-1].y*variables.height - self.battlechoice.buttons[-1].height()
            scaleintervals = play_sound.scales[self.getscalename()]
            for i in scaleintervals:
                tpic = getTextPic(str(i)+" ", variables.gettextsize(), variables.WHITE)
                variables.screen.blit(tpic, (scalex, scaley))
                scalex += tpic.get_width()
            variables.dirtyrects.append(Rect(firstscalex, scaley, scalex-firstscalex, self.battlechoice.buttons[-1].height()))

        elif self.state == "lose" or self.state == "win":

            # button
            if self.state == "win":
                conttext = "continue"
                # button coordinates are multipliers of screen width and height
                continuebutton = Button(1 / 2, b/h, conttext, variables.gettextsize()/h)
                continuebutton.iscentered = True
                continuebutton.draw(True)
            else:
                self.retrychoice.draw()

            # text
            text = None
            if self.state == "lose":
                text = variables.font.render("you lost...", 0, variables.WHITE)
            else:
                text = variables.font.render("you win!", 0, variables.WHITE)
            textscaled = sscale(text)
            variables.screen.blit(textscaled, [w / 2 - (textscaled.get_width() / 2), h / 2])
            self.drawscoretable()

        
        elif self.state == "exp" or self.state == "got exp":
            text = "continue"
            # continue button
            continuebutton = Button(1 / 2, b/h, text, variables.gettextsize()/h)
            continuebutton.iscentered = True
            continuebutton.draw(True)

            # text
            text = variables.font.render("EXP", 0, variables.WHITE)
            textscaled = sscale(text)
            exppos = [w / 2 - (textscaled.get_width() / 2), h / 3]
            variables.screen.blit(textscaled, exppos)
            variables.dirtyrects.append(Rect(exppos[0], exppos[1], textscaled.get_width(), textscaled.get_height()))
            text = variables.font.render("Lv " + str(classvar.player.lv()), 0, variables.WHITE)
            textscaled = sscale(text)
            lvpos = [0, h / 3 - textscaled.get_height()]
            variables.screen.blit(textscaled, lvpos)
            variables.dirtyrects.append(Rect(lvpos[0], lvpos[1], textscaled.get_width(), textscaled.get_height()))

            # exp bar
            percentofbar = stathandeling.percentoflevel(p.exp)
            barrect = Rect(0, h/2, w*percentofbar, h/18)
            variables.screen.fill(variables.BLUE, barrect)
            variables.dirtyrects.append(barrect)

            # level up text
            if self.state == "got exp" and stathandeling.explv(self.oldexp) < stathandeling.explv(self.newexp):
                text = variables.font.render(variables.settings.bearname + "'s dance level increased.", 0, variables.GREEN)
                textscaled = sscale(text)
                coordinates = [w / 2 - (textscaled.get_width() / 2), h / 3 - textscaled.get_height()]
                variables.screen.blit(textscaled,
                                      coordinates)
                variables.dirtyrects.append(Rect(coordinates[0], coordinates[1], textscaled.get_width(), textscaled.get_height()))

            self.drawscoretable()

        # player health bar
        playermaxh = stathandeling.max_health(p.lv())
        healthh = h * (1 / 18)
        enemyhealthh = h * (1 / 50)
        
        epich = enemypic_height()
        epicw = self.enemy.animation.pic_width(epich)
        percenthealthlefte = self.enemy.health / stathandeling.max_health(self.enemy.lv)
        healthbarcolor = variables.GREEN
        if p.health != playermaxh:
            percenthealthleft = p.health / playermaxh
            barrect = Rect(w - epicw, epich, epicw * (1 - percenthealthleft),enemyhealthh)
            variables.screen.fill(healthbarcolor, barrect)
            variables.dirtyrects.append(barrect)
        if not percenthealthlefte == 1:
            barrect = Rect(0, h-healthh, w*(1-percenthealthlefte), healthh)
            variables.screen.fill(healthbarcolor, barrect)
            variables.dirtyrects.append(barrect)
        # if they did not miss any in the last beatmap
        if (self.damage_multiplier > variables.perfect_value and self.state == "attacking"):
            punscaled = variables.font.render("PERFECT!", 0, variables.WHITE)
            ptext = sscale_customfactor(punscaled, 1.5)
            coordinates = [(variables.width / 2) - (ptext.get_width() / 2) - epich, variables.getpadypos() - ptext.get_height() - 10]
            variables.screen.blit(ptext, coordinates)
            variables.dirtyrects.append(Rect(coordinates[0], coordinates[1], ptext.get_width(), ptext.get_height()))

    def updatescreenforenemy(self):
        self.enemy.animation.update_topright(enemypic_height())

    def partofbeatlist(self):
        pofbeatlist = [0]
        # list of honey animations that should be double speed
        doublespeedlist = [2,3,4,5,7]
        if self.playercurrentanim in doublespeedlist:
            # double speed of animation 3 (spin)
            pofbeatlist.append(2)
        return pofbeatlist
            
    def drumbeat(self, partofbeat):
        # play the drum
        if partofbeat == 0:
            play_drum(0, self.enemy.drumpackname)

            # chance for a special move based on combo
            specialmovechance = (self.getcombo())/len(self.beatmaps[self.current_beatmap].originalnotes)
            specialmovechance *= (1.0/4.0)

            # not before combo reaches 10
            if self.getcombo() < 10:
                specialmovechance = 0
                
            if self.getcombo()%10 == 0:
                specialmovechance *= 3.5
            elif self.getcombo()%5 == 0:
                specialmovechance *= 2

            if random.random() < specialmovechance:
                self.newplayerspecialmove()
            else:
                self.specialmovep = False
            
        elif partofbeat == 2:
            drumchance = self.getcombo()/len(self.beatmaps[self.current_beatmap].originalnotes)
            if random.random() <drumchance:
                drumoctave = 4
                if random.random() < 0.3:
                    drumoctave = random.randint(3, 7)
                play_drum(drumoctave, self.enemy.drumpackname)
        else:
            drumchance = self.getcombo()/len(self.beatmaps[self.current_beatmap].originalnotes)
            drumchance = drumchance/4
            if random.random() <drumchance:
                drumoctave = 4
                if random.random() < 0.6:
                    drumoctave = random.randint(3, 7)
                play_drum(drumoctave, self.enemy.drumpackname)
        

        # player dirty rect and enemy dirty rect on beat
        if partofbeat in self.partofbeatlist():

            # update screen for enemy, player
            self.updatescreenforenemy()
            # player dirty rect
            variables.dirtyrects.append(self.getplayerpicandrect()[1])

        # change player pic
        self.nextplayerpic(partofbeat)
        
    def nextplayerpic(self, partofbeat):
        if partofbeat in self.partofbeatlist():
            self.playerframe += 1
            
            newname = self.currentplayerframename()
            # if this frame does not exist pick a new dance animation
            if not newname in GR:
                self.newplayeranimation()

    def newplayeranimation(self):
        self.playerframe = 0
        maxanimnumber = max(1, classvar.player.lv() - variables.settings.difficulty)
        maxanimnumber = min(numofplayerframes-1, maxanimnumber)
        self.playercurrentanim = random.randint(0, maxanimnumber)

    def newplayerspecialmove(self):
        maxanimnumber = numofspecialmoveeffects-1
        self.currentspecialmove = random.randint(0, maxanimnumber)
        self.specialmovep = True
        

    def deletetutorialnote(self):
        # get rid of the third turorial note
        b = self.beatmaps[0]
        deletedp = False
        i = 0
        while not deletedp:
            if b.notes[i].time >= 12:
                del b.notes[i]
                deletedp = True
            else:
                i += 1
        # offset the rest
        for note in b.notes:
            if note.time >= 24:
                note.time -= 12

    def exittutorial(self):
        self.tutorialp = False
        if self.accidentaltutorialp:
            classvar.player.addstoryevent("accidentaltutorial")

    def tutorialdancetick(self,currentb, dt):
        if self.tutorialstate == "starting":
            if currentb.notetime() > 4:
                skiptutorialp = False
                if self.accidentaltutorialp:
                    skiptutorialp = len(currentb.scores) == 1 and currentb.scores[0] >= variables.ok_value
                else:
                    skiptutorialp = len(currentb.scores) == 2 and (currentb.scores[0] + currentb.scores[1])/2 >= variables.ok_value
                
                #exit the tutorial if the got the first two notes perfectly
                if skiptutorialp:
                    self.exittutorial()
                    # get rid of the third turorial note
                    self.deletetutorialnote()
                else:
                    self.tutorialstate = "first note"
                    currentb.showkeys(self.accidentaltutorialp)
                    maps.engage_conversation(self.tutorialconversations[0], True)
        elif self.tutorialstate == "first note":
            fnote = currentb.notes[0]
            if fnote.pos[1] >= variables.getpadypos() and fnote.time > variables.settings.notes_per_screen + 2:
                self.tutorialstate = "release note"
                maps.engage_conversation(self.tutorialconversations[1], True)
        elif self.tutorialstate == "release note":
            fnote = currentb.notes[0]
            if fnote.pos[1] - fnote.height(currentb.tempo) > variables.getpadypos() and fnote.time > 10:
                self.tutorialstate = "finished first"
                maps.engage_conversation(self.tutorialconversations[2], True)
        elif self.tutorialstate == "finished first":
            fnote = currentb.notes[0]
            if fnote.time >= 24:
                self.tutorialstate = "done"
                currentb.scores = []
                maps.engage_conversation(self.tutorialconversations[3], True)
                self.exittutorial()

    def drummermodep(self):
        return "drummer" in self.beatmaps[self.current_beatmap].enemyspecs["rules"]
        
    # for things like the attack animation
    def ontick(self):
        currentb = None
        if self.state == "dance":
            currentb = self.beatmaps[self.current_beatmap]
            olddrum = currentb.drumcounter
            currentb.ontick()
            if currentb.drumcounter > olddrum and not self.drummermodep():
                self.drumbeat(currentb.drumcounter%4)
        
        dt = variables.settings.current_time - self.animationtime

        
        if self.tutorialp and self.state == "dance":
            self.tutorialdancetick(currentb, dt)
            
        if self.state == "attacking":
            if self.isplayernext == True:
                damage = self.oldplayerhealth - self.newplayerhealth
                hs = variables.healthanimationspeed
                damagefactor = (hs - dt) / hs
                # set player's health to somewhere between the old and new depending on time (damagefactor)
                classvar.player.health = self.newplayerhealth + damage * damagefactor
                # if the player's health is now at the end of the animation
                if classvar.player.health <= self.newplayerhealth:
                    classvar.player.health = self.newplayerhealth  # set it to the new health when done
                    if self.newplayerhealth <= 0:
                        self.state = "lose"
                        if self.enemy.name == "chimney":
                            maps.engage_conversation("losetochimney", True)
                    elif self.newenemyhealth == self.enemy.health:  # if done with the animation
                        self.state = "dance"  # exit
                        self.next_beatmap()
                    else:
                        self.isplayernext = False
                        self.animationtime = variables.settings.current_time
            elif self.isplayernext == False:
                damage = self.oldenemyhealth - self.newenemyhealth
                hs = variables.healthanimationspeed
                damagefactor = (hs - dt) / hs
                # set enemy's health to somewhere between the old and new depending on time (damagefactor)
                self.enemy.health = self.newenemyhealth + damage * damagefactor
                # if the enemy's health is now at the end of the animation
                if self.enemy.health <= self.newenemyhealth:
                    self.enemy.health = self.newenemyhealth
                    if self.newenemyhealth <= 0:
                        self.state = "win"
                    elif classvar.player.health == self.newplayerhealth:  # if done with the animation
                        self.state = "dance"  # exit
                        self.next_beatmap()
                    else:
                        self.isplayernext = True
                        self.animationtime = variables.settings.current_time

        elif self.state == "exp":
            es = variables.expanimationspeed
            timefactor = dt / es
            expgained = self.newexp - self.oldexp
            classvar.player.exp = self.oldexp + expgained * timefactor
            if classvar.player.exp >= self.newexp:
                classvar.player.exp = self.newexp
                if stathandeling.explv(self.oldexp) < stathandeling.explv(self.newexp):
                    classvar.player.heal()
                self.state = "got exp"

        # check for end of beatmap
        elif self.state == "dance":
            if len(currentb.notes) == 0:
                self.trade(currentb.scores)
                currentb.reset_buttons()


    def lose(self):
        # go home
        classvar.player.addstoryevents(self.enemy.storyeventsonlose)
        
        maps.teleportplayerhome()
        
        classvar.player.timeslost += 1
        classvar.player.totalbattles += 1
        returntoworld()

        
    def win(self):
        classvar.player.addstoryevents(self.enemy.storyeventsonwin)
        classvar.player.totalbattles += 1
        returntoworld()
        
    def flee(self):
        classvar.player.addstoryevents(self.enemy.storyeventsonflee)
        if self.enemy.lv - variables.settings.difficulty == 0:
            maps.engage_conversation("letsflee", True)
        returntoworld()

    def onkey(self, key):
        def change_soundpack(offset):
            i = classvar.player.soundpacks.index(variables.settings.soundpack)
            variables.settings.soundpack = classvar.player.soundpacks[(i + offset) % len(classvar.player.soundpacks)]
            self.battlechoice.buttons[-2].assign_text(variables.settings.soundpack)

        def change_scale(offset):
            variables.settings.scaleindex = (variables.settings.scaleindex + offset) % len(classvar.player.scales)
            self.battlechoice.buttons[-1].assign_text(self.getscalename())
        
        if(variables.devmode):
            if(key == variables.devlosebattlekey):
                self.lose()
            elif(key == variables.devwinbattlekey):
                self.win()
        if self.state == 'dance':
            if self.tutorialp:
                if not self.tutorialstate == "first note" or (not variables.checkkey("note1", key) and not variables.checkkey("note1modified", key)):
                    self.beatmaps[self.current_beatmap].onkey(key)
            else:
                self.beatmaps[self.current_beatmap].onkey(key)

            # check for octopus animation change
            if self.drummermodep():
                for noteindex in range(8):
                    if variables.checkkey("note" + str(noteindex+1), key):
                        self.enemy.animation.change_frame(variables.octopusarmtomultipartpart[noteindex], newframe = 1)
        elif self.state == "choose":
            if variables.checkkey("enter", key):
                if self.battlechoice.current_option == 0:
                    self.startnew()
                elif self.battlechoice.current_option == 1:
                    self.flee()
                elif self.battlechoice.current_option == 2:
                    change_soundpack(1)
                elif self.battlechoice.current_option == 3:
                    change_scale(1)
            else:
                if variables.checkkey("left", key):
                    play_drum(4, self.enemy.drumpackname)
                    self.battlechoice.previousoption()
                elif variables.checkkey("right", key):
                    play_drum(4, self.enemy.drumpackname)
                    self.battlechoice.nextoption()
                elif variables.checkkey("up", key) and self.battlechoice.current_option == 2:
                    change_soundpack(-1)
                elif variables.checkkey("down", key) and self.battlechoice.current_option == 2:
                    change_soundpack(1)
                elif variables.checkkey("up", key) and self.battlechoice.current_option == 3:
                    change_scale(-1)
                elif variables.checkkey("down", key) and self.battlechoice.current_option == 3:
                    change_scale(1)

        elif self.state == "lose":
            if  variables.checkkey("enter", key):
                if self.retrychoice.getoption() == "retry":
                    self.startnew()
                else:
                    self.lose()
            else:
                self.retrychoice.leftrightonkey(key)
        elif self.state == "win" and variables.checkkey("enter", key):
            self.addexp()
        elif self.state == "got exp" and variables.checkkey("enter", key):
            self.win()

    def onrelease(self, key):
        releasep = False
        if self.state == "dance":
            if self.tutorialp:
                if (variables.checkkey("note1", key) and not self.accidentaltutorialp)  or (variables.checkkey("note1modified", key) and self.accidentaltutorialp):
                    if self.tutorialstate == "first note":
                        pass
                    elif self.tutorialstate == "release note":
                        maps.engage_conversation(self.tutorialconversations[4], True)
                    else:
                        releasep = True
                else:
                    releasep = True
            else:
                releasep = True
        if releasep:
            # check for octopus animation change
            if self.drummermodep():
                for noteindex in range(8):
                    if variables.checkkey("note" + str(noteindex+1), key):
                        self.enemy.animation.change_frame(variables.octopusarmtomultipartpart[noteindex], newframe = 0)

            self.beatmaps[self.current_beatmap].onrelease(key)
            

    def addexp(self):
        self.state = "exp"
        expgained = stathandeling.exp_gained(self.enemy.lv)
        if self.enemy.lv > classvar.player.lv():
            expgained *= 1.5
        self.newexp = classvar.player.exp + expgained
        self.animationtime = variables.settings.current_time
        self.oldexp = classvar.player.exp
            
    # "damages" player and enemy after a round and before the animation
    def trade(self, scores):
        currentb = self.beatmaps[self.current_beatmap]
        self.damage_multiplier = sum(scores) / len(scores)
        self.damage_multiplier *= variables.player_advantage_multiplier
        
        # if they did not miss any
        if (not (variables.miss_value in scores)):
            self.damage_multiplier *= variables.all_perfect_multiplier

        combomultiplier = 1 + (self.runningcombo + currentb.roundmaxcombo) / len(currentb.originalnotes) * variables.player_combo_multiplier
        
        playerlv = classvar.player.lv()
        enemylv = self.enemy.lv
        self.state = "attacking"
        self.oldenemyhealth = self.enemy.health
        self.oldplayerhealth = classvar.player.health
        self.animationtime = variables.settings.current_time

        def damageplayer():
            self.newplayerhealth = classvar.player.health - stathandeling.damage(enemylv)
            if self.newplayerhealth <= 0.25:
                self.newplayerhealth = 0

        def damageenemy():
            self.newenemyhealth = self.enemy.health - stathandeling.damage(playerlv) * self.damage_multiplier
            if self.newenemyhealth <= 0.25:
                self.newenemyhealth = 0

        #if playerlv > enemylv or (playerlv == enemylv and random.choice([True, False])) or \
        #                self.damage_multiplier > variables.perfect_value:
        #    self.isplayernext = False
        #else:
        #    self.isplayernext = True
        # player always attacks first
        self.isplayernext = False
        
        damageenemy()
        damageplayer()

        # set the player animation back to default
        self.playerframe = 0
        self.playercurrentanim = 0
        # player dirty rect
        playerpic = getpicbyheight("honeydance0-0", variables.height/4)
        variables.dirtyrects.append(self.getplayerpicandrect()[1])
