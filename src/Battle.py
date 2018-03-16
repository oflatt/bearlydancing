#!/usr/bin/python
import variables, pygame, stathandeling, classvar, random, maps, randombeatmap, copy, conversations
from ChoiceButtons import ChoiceButtons
from Button import Button
from Note import Note
from play_sound import play_sound
from play_sound import soundpackkeys
from play_sound import scales
from graphics import getpic, sscale, sscale_customfactor, getpicbyheight, GR
from FrozenClass import FrozenClass
from pygame import Rect


# battle is the class that runs the battle- information about the game such as storyeventonwin is stored in enemy
class Battle(FrozenClass):

    def __init__(self, enemy):

        self.current_beatmap = 0
        self.damage_multiplier = 1
        self.beatmaps = []

        # copy the enemy first to avoid editing originals
        self.enemy = copy.copy(enemy)
        # offset enemy lv by difficulty
        self.enemy.lv += variables.settings.difficulty
        
        # state can be choose, dance, or attacking, win, lose, exp, got exp
        self.state = "choose"
        self.tutorialstate = None
        
        # if the enemy's level is 0 and there have been no battles, the tutorial is triggered
        self.tutorialp = self.enemy.lv - variables.settings.difficulty == 0 and classvar.player.totalbattles == 0

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
        self.battlechoice = ChoiceButtons(["   DANCE!   ", "Flee", variables.settings.soundpack, classvar.player.scales[variables.settings.scaleindex]], 13 / 16)

        # if pausetime is 0 it is not paused, otherwise it is paused and it records when it was paused
        self.pausetime = 0
        self.enemy.sethealth()

        self.playerframe = 0
        self.playercurrentanim = 0

        self._freeze()

    def setfirstbeatmap(self):
        specs = copy.deepcopy(variables.generic_specs)
        specs["lv"] = self.enemy.lv
        specs["rules"].extend(self.enemy.beatmaprules)
        self.beatmaps = [randombeatmap.random_beatmap(specs)]
        self.beatmaps[0].scale = scales[classvar.player.scales[variables.settings.scaleindex]]
        self.reset_time()
        self.reset_enemy()

        if self.tutorialp:
            self.tutorialstate = "starting"
            # if it is the tutorial, add two notes for the player to fail on, and change first note to a
            b = self.beatmaps[0]
            b.notes[0] = Note(0, b.notes[0].time, 3)
            # first add ten to give space for the new notes
            for note in b.notes:
                note.time += 24
            b.notes[0].time -= 12
            b.notes = [Note(0, 1, 1), Note(1, 2, 1)] + b.notes

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
        self.beatmaps[self.current_beatmap].unpause()
        self.reset_enemy()

    def new_beatmaps(self):
        self.beatmaps = [randombeatmap.variation_of(self.beatmaps[0].originalnotes, self.beatmaps[0].tempo)]
        self.beatmaps[0].scale = scales[classvar.player.scales[variables.settings.scaleindex]]

    def next_beatmap(self):
        if self.current_beatmap + 1 == len(self.beatmaps):
            self.new_beatmaps()
            self.current_beatmap = 0
        else:
            print("should only have one beatmap in the list!")
            self.current_beatmap += 1
        self.beatmaps[self.current_beatmap].reset(self.starttime, False)
        self.reset_enemy()

    def reset_enemy(self):
        self.enemy.reset()
        if len(self.beatmaps) > 0:
            self.enemy.animation.framerate = self.beatmaps[self.current_beatmap].tempo
        self.enemy.animation.beginning_time = self.starttime

    def currentplayerframename(self):
        return "honeydance" + str(self.playercurrentanim) + "-" + str(self.playerframe)

    def draw(self):
        h = variables.height
        w = variables.width
        b = h * 13 / 16
        p = classvar.player
        # background
        variables.screen.fill(variables.BLACK)

        # draw enemy first
        if self.state != "dance":
            self.enemy.animation.reset() # if not dancing, use first frame
        epic = getpicbyheight(self.enemy.animation.current_frame(), variables.height/5)

        if self.state != "dance":
            playerpic = getpicbyheight("honeydance0-0", variables.height/4)
        else:
            playerpic = getpicbyheight(self.currentplayerframename(), variables.height/4)
        
        variables.screen.blit(epic, [w - epic.get_width(), 0])
        variables.screen.blit(playerpic, [w-playerpic.get_width(), h-playerpic.get_height()])

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

        elif self.state == "lose" or self.state == "win":
            text = None
            # button
            if self.state == "lose":
                text = "go home in shame"
            else:
                text = "continue"
            # button coordinates are multipliers of screen width and height
            continuebutton = Button(1 / 2, b/h, text, variables.gettextsize()/h)
            continuebutton.iscentered = True
            continuebutton.draw(True)

            # text
            if self.state == "lose":
                text = variables.font.render("you lost...", 0, variables.WHITE)
            else:
                text = variables.font.render("you win!", 0, variables.WHITE)
            textscaled = sscale(text)
            variables.screen.blit(textscaled, [w / 2 - (textscaled.get_width() / 2), h / 2])

        elif self.state == "exp" or self.state == "got exp":
            text = "continue"
            # continue button
            continuebutton = Button(1 / 2, b/h, text, variables.gettextsize()/h)
            continuebutton.iscentered = True
            continuebutton.draw(True)

            # text
            text = variables.font.render("EXP", 0, variables.WHITE)
            textscaled = sscale(text)
            variables.screen.blit(textscaled, [w / 2 - (textscaled.get_width() / 2), h / 3])
            text = variables.font.render("Lv " + str(classvar.player.lv()), 0, variables.WHITE)
            textscaled = sscale(text)
            variables.screen.blit(textscaled, [0, h / 3 - textscaled.get_height()])

            # exp bar
            percentofbar = stathandeling.percentoflevel(p.exp)
            barrect = Rect(0, h/2, w*percentofbar, h/18)
            variables.screen.fill(variables.BLUE, barrect)
            variables.dirtyrects.append(barrect)

            # level up text
            if self.state == "got exp" and stathandeling.explv(self.oldexp) < stathandeling.explv(self.newexp):
                text = variables.font.render(variables.settings.bearname + "'s dance level increased.", 0, variables.GREEN)
                textscaled = sscale(text)
                variables.screen.blit(textscaled,
                                      [w / 2 - (textscaled.get_width() / 2), h / 3 - textscaled.get_height()])

        # player health bar
        playermaxh = stathandeling.max_health(p.lv())
        healthh = h * (1 / 18)
        enemyhealthh = h * (1 / 50)
        e = self.enemy
        epicw = epic.get_width()
        epich = epic.get_height()
        percenthealthlefte = e.health / stathandeling.max_health(e.lv)
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
            variables.screen.blit(ptext, [(variables.width / 2) - (ptext.get_width() / 2) - epicw,
                                          variables.getpadypos() - ptext.get_height() - 10])

    def drumbeat(self):
        # update screen for enemy, player
        epic = getpicbyheight(self.enemy.animation.current_frame(), variables.height/5)
        variables.dirtyrects.append(Rect(variables.width-epic.get_width(), 0, epic.get_width(), epic.get_height()))
        playerpic = getpicbyheight("honeydance0-0", variables.height/4)
        variables.dirtyrects.append(Rect(variables.width-playerpic.get_width(), variables.height-playerpic.get_height(), playerpic.get_width(), playerpic.get_height()))

        # change player pic
        self.nextplayerpic()

    def nextplayerpic(self):
        self.playerframe += 1
        
        newname = self.currentplayerframename()
        # if this frame does not exist pick a new dance animation
        if not newname in GR:
            self.newplayeranimation()

    def newplayeranimation(self):
        self.playerframe = 0
        maxanimnumber = classvar.player.lv() - variables.settings.difficulty
        self.playercurrentanim = random.randint(0, maxanimnumber)
        # if this number is too large because an animation for that level does not exist, pick a new one lower than it
        while not self.currentplayerframename() in GR:
            maxanimnumber = self.playercurrentanim-1
            self.playercurrentanim = random.randint(0, maxanimnumber)
        

    # for things like the attack animation
    def ontick(self):
        currentb = None
        if self.state == "dance":
            currentb = self.beatmaps[self.current_beatmap]
            olddrum = currentb.drumcounter
            currentb.ontick()
            if currentb.drumcounter > olddrum:
                self.drumbeat()
        
        dt = variables.settings.current_time - self.animationtime

        
        if self.tutorialp and self.state == "dance":
            if self.tutorialstate == "starting":
                if currentb.notetime() > 4:
                    #exit the tutorial if the got the first two notes perfectly
                    if len(currentb.scores) == 2:
                        if (currentb.scores[0] + currentb.scores[1])/2 >= variables.ok_value:
                            self.tutorialp = False
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
                    else:
                        self.tutorialstate = "first note"
                        currentb.showkeys()
                        maps.engage_conversation(conversations.tutorialconversation1)
            elif self.tutorialstate == "first note":
                fnote = currentb.notes[0]
                if fnote.pos[1] >= variables.getpadypos() and fnote.time > variables.settings.notes_per_screen + 2:
                    self.tutorialstate = "release note"
                    maps.engage_conversation(conversations.pressanow)
            elif self.tutorialstate == "release note":
                fnote = currentb.notes[0]
                if fnote.pos[1] - fnote.height(currentb.tempo) > variables.getpadypos() and fnote.time > 10:
                    self.tutorialstate = "finished first"
                    maps.engage_conversation(conversations.releaseanow)
            elif self.tutorialstate == "finished first":
                fnote = currentb.notes[0]
                if fnote.time >= 24:
                    self.tutorialstate = "done"
                    currentb.scores = []
                    maps.engage_conversation(conversations.endtutorial)

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
                            maps.engage_conversation(conversations.losetochimney)
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
        classvar.player.heal()
        variables.settings.state = "world"
        maps.change_map_nonteleporting(maps.home_map_name)
        classvar.player.teleport(maps.current_map.startpoint[0], maps.current_map.startpoint[1])
        classvar.player.timeslost += 1
        classvar.player.totalbattles += 1

    def win(self):
        classvar.player.addstoryevents(self.enemy.storyeventsonwin)
        classvar.player.totalbattles += 1
        variables.dirtyrects = [Rect(0,0,variables.width,variables.height)]
        variables.settings.state = "world"  # finally exit Battle

    def flee(self):
        variables.settings.state = "world"
        variables.dirtyrects = [Rect(0,0,variables.width,variables.height)]
        classvar.player.addstoryevents(self.enemy.storyeventsonflee)
        if self.enemy.lv - variables.settings.difficulty == 0:
            maps.engage_conversation(conversations.letsflee)

    def onkey(self, key):
        def change_soundpack(offset):
            i = soundpackkeys.index(variables.settings.soundpack)
            variables.settings.soundpack = soundpackkeys[(i + offset) % len(soundpackkeys)]
            self.battlechoice.buttons[-2].assign_text(variables.settings.soundpack)

        def change_scale(offset):
            variables.settings.scaleindex = (variables.settings.scaleindex + offset) % len(classvar.player.scales)
            self.battlechoice.buttons[-1].assign_text(classvar.player.scales[variables.settings.scaleindex])
        
        if(variables.devmode):
            if(key == variables.devlosebattlekey):
                self.lose()
            elif(key == variables.devwinbattlekey):
                self.win()
        if self.state == 'dance':
            if self.tutorialp:
                if not self.tutorialstate == "first note" or not variables.checkkey("note1", key):
                    self.beatmaps[self.current_beatmap].onkey(key)
            else:
                self.beatmaps[self.current_beatmap].onkey(key)
        elif self.state == "choose":
            if variables.checkkey("enter", key):
                if self.battlechoice.current_option == 0:
                    self.state = "dance"
                    self.setfirstbeatmap()
                    # clear screen
                    variables.dirtyrects = [Rect(0,0,variables.width,variables.height)]
                elif self.battlechoice.current_option == 1:
                    self.flee()
                elif self.battlechoice.current_option == 2:
                    change_soundpack(1)
                elif self.battlechoice.current_option == 3:
                    change_scale(1)
            else:
                if variables.checkkey("left", key):
                    self.battlechoice.previousoption()
                elif variables.checkkey("right", key):
                    self.battlechoice.nextoption()
                elif variables.checkkey("up", key) and self.battlechoice.current_option == 2:
                    change_soundpack(-1)
                elif variables.checkkey("down", key) and self.battlechoice.current_option == 2:
                    change_soundpack(1)
                elif variables.checkkey("up", key) and self.battlechoice.current_option == 3:
                    change_scale(-1)
                elif variables.checkkey("down", key) and self.battlechoice.current_option == 3:
                    change_scale(1)

        elif self.state == "lose" and variables.checkkey("enter", key):
            self.lose()
        elif self.state == "win" and variables.checkkey("enter", key):
            self.addexp()
        elif self.state == "got exp" and variables.checkkey("enter", key):
            self.win()

    def onrelease(self, key):
        releasep = False
        if self.state == "dance":
            if self.tutorialp:
                if variables.checkkey("note1", key):
                    if self.tutorialstate == "first note":
                        pass
                    elif self.tutorialstate == "release note":
                        maps.engage_conversation(conversations.releasedearly)
                    else:
                        releasep = True
                else:
                    releasep = True
            else:
                releasep = True
        if releasep:
            self.beatmaps[self.current_beatmap].onrelease(key)

    def addexp(self):
        self.state = "exp"
        self.newexp = classvar.player.exp + stathandeling.exp_gained(self.enemy.lv)
        self.animationtime = variables.settings.current_time
        self.oldexp = classvar.player.exp
            
    # "damages" player and enemy after a round and before the animation
    def trade(self, scores):
        self.damage_multiplier = sum(scores) / len(scores)
        self.damage_multiplier *= variables.player_advantage_multiplier
        
        # if they did not miss any
        if (not (variables.miss_value in scores)):
            self.damage_multiplier *= variables.all_perfect_multiplier

        
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

        if playerlv > enemylv or (playerlv == enemylv and random.choice([True, False])) or \
                        self.damage_multiplier > variables.perfect_value:
            self.isplayernext = False
        else:
            self.isplayernext = True
            
        damageenemy()
        damageplayer()
