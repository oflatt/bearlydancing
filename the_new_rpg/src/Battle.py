#!/usr/bin/python
#Oliver works on classes
import variables, pygame, stathandeling, classvar, random, graphics, maps, randombeatmap
from Button import Button

class Battle():
    #for attacking animation
    isplayernext = False #if the player is currently being damaged
    oldenemyhealth = 20
    oldplayerhealth = 20
    newplayerhealth = 10
    newenemyhealth = 10

    #animation time is used for all animations
    animationtime = 0

    #for win animation
    newexp = 0
    oldexp = 0

    #drawing buttons
    buttons = []

    beatmaps = []
    #-1 so that when it first changes it it becomes 0
    current_beatmap = -1
    damage_multiplier = 1
    def __init__(self, enemy):
        self.enemy = enemy
        variables.beatmaptype = "melodic"
        #state can be choose, dance, or attacking, win, lose, exp, got exp
        self.state = "choose"
        self.option = 1
        self.enemy.pic = graphics.scale_pure(self.enemy.pic, variables.width/5)
        self.new_beatmaps()
        classvar.player.heal()

    def new_beatmaps(self):
        self.beatmaps = randombeatmap.very_random_v(self.enemy.lv)

    def next_beatmap(self):
        if self.current_beatmap+1 == len(self.beatmaps):
            self.new_beatmaps()
            self.current_beatmap = 0
        else:
            self.current_beatmap += 1
        self.beatmaps[self.current_beatmap].reset()

    def draw(self):
        h = variables.height
        w = variables.width
        b = h*13/16
        p = classvar.player
        #background
        pygame.draw.rect(variables.screen, variables.BLACK, [0, 0, w, h])

        #draw beatmap
        if self.state == "dance":
            self.beatmaps[self.current_beatmap].draw()
        elif self.state == "attacking":
            self.beatmaps[self.current_beatmap].draw_pads()

        if self.state == "choose":
            #enemy name
            enemyname = variables.font.render("LV "+str(self.enemy.lv) + " " + self.enemy.name + " appears!", 0,
                                              variables.WHITE)
            enemynamescaled = graphics.sscale(enemyname)
            variables.screen.blit(enemynamescaled, [w/2-(enemynamescaled.get_width()/2), h/2])

            #two buttons
            dancebutton = Button(w/4, b, "DANCE!", 1.5)
            fleebutton = Button(w*3/4, b, "Flee..", 1.5)
            if self.option == 1:
                dancebutton.ison = True
            else:
                fleebutton.ison = True
            self.buttons = [dancebutton, fleebutton]
            self.draw_buttons()

        elif self.state == "lose" or self.state == "win":
            #button
            if self.state== "lose":
                text = "go home..."
            else:
                text = "continue"
            continuebutton = Button(w/2, b, text, 1.5)
            continuebutton.ison = True
            self.buttons = [continuebutton]
            self.draw_buttons()

            #text
            if self.state == "lose":
                text = variables.font.render("you can't go on...", 0, variables.WHITE)
            else:
                text = variables.font.render("you win!", 0, variables.WHITE)
            textscaled = graphics.sscale(text)
            variables.screen.blit(textscaled, [w/2-(textscaled.get_width()/2), h/2])

        elif self.state == "exp" or self.state == "got exp":
            #continue button
            continuebutton = Button(w/2, b, "continue", 1.5)
            continuebutton.ison = True
            self.buttons = [continuebutton]
            self.draw_buttons()

            #text
            text = variables.font.render("EXP", 0, variables.WHITE)
            textscaled = graphics.sscale(text)
            variables.screen.blit(textscaled, [w/2-(textscaled.get_width()/2), h/3])
            text = variables.font.render("Lv " + str(classvar.player.lv), 0, variables.WHITE)
            textscaled = graphics.sscale(text)
            variables.screen.blit(textscaled, [0, h/3 - textscaled.get_height()])

            #exp bar
            percentofbar = (p.exp - stathandeling.lvexp(p.lv))/stathandeling.exp_needed(p.lv)
            pygame.draw.rect(variables.screen, variables.BLUE, [0,
                                                            h/2,
                                                            w*percentofbar,
                                                            h/18])

            #level up text
            if self.state == "got exp" and stathandeling.explv(self.oldexp) < stathandeling.explv(self.newexp):
                text = variables.font.render("LEVEL UP!", 0, variables.GREEN)
                textscaled = graphics.sscale(text)
                variables.screen.blit(textscaled, [w/2-(textscaled.get_width()/2), h/3 - textscaled.get_height()])


        epic = self.enemy.pic
        variables.screen.blit(epic, [w-epic.get_width(), 0])

        #player health bar
        playermaxh = stathandeling.max_health(p.lv)
        healthh = h*(1/18)
        enemyhealthh = h*(1/50)
        e = self.enemy
        epicw = epic.get_width()
        epich = epic.get_height()
        percenthealthlefte = e.health/stathandeling.max_health(e.lv)
        healthbarcolor = variables.GREEN
        if p.health != playermaxh:
            percenthealthleft = p.health/playermaxh
            pygame.draw.rect(variables.screen, healthbarcolor, [w-epicw,
                                                                epich,
                                                                epicw*(1-percenthealthleft),
                                                                enemyhealthh])
        if not percenthealthlefte == 1:
            pygame.draw.rect(variables.screen, healthbarcolor, [0,
                                                                h-healthh,
                                                                w*(1-percenthealthlefte),
                                                                healthh])
        #if they did not miss any in the last beatmap
        if(self.damage_multiplier>variables.perfect_value and self.state == "attacking"):
            punscaled = variables.font.render("PERFECT!", 0, variables.WHITE)
            ptext = graphics.sscale_customfactor(punscaled, 1.5)
            variables.screen.blit(ptext, [(variables.width/2)-(ptext.get_width()/2)-epicw,
                                          variables.padypos-ptext.get_height()-10])


    #for things like the attack animation
    def ontick(self):
        self.beatmaps[self.current_beatmap].ontick()

        if self.state == "attacking":
            if self.isplayernext == True:
                damage = self.oldplayerhealth - self.newplayerhealth
                differenceintime = variables.current_time-self.animationtime
                hs = variables.healthanimationspeed
                damagefactor = (hs-differenceintime)/hs
                #set player's health to somewhere between the old and new depending on time (damagefactor)
                classvar.player.health = self.newplayerhealth + damage*damagefactor
                #if the player's health is now at the end of the animation
                if classvar.player.health <= self.newplayerhealth:
                    classvar.player.health = self.newplayerhealth#set it to the new health when done
                    if self.newplayerhealth <= 0:
                        self.state = "lose"
                    elif self.newenemyhealth == self.enemy.health: #if done with the animation
                        self.state = "dance" #exit
                        self.next_beatmap()
                    else:
                        self.isplayernext = False
                        self.animationtime = variables.current_time
            elif self.isplayernext == False:
                damage = self.oldenemyhealth - self.newenemyhealth
                differenceintime = variables.current_time-self.animationtime
                hs = variables.healthanimationspeed
                damagefactor = (hs-differenceintime)/hs
                #set enemy's health to somewhere between the old and new depending on time (damagefactor)
                self.enemy.health = self.newenemyhealth + damage*damagefactor
                #if the enemy's health is now at the end of the animation
                if self.enemy.health <= self.newenemyhealth:
                    self.enemy.health = self.newenemyhealth
                    if self.newenemyhealth <= 0:
                        self.state = "win"
                    elif classvar.player.health == self.newplayerhealth: #if done with the animation
                        self.state = "dance" #exit
                        self.next_beatmap()
                    else:
                        self.isplayernext = True
                        self.animationtime = variables.current_time

        elif self.state == "exp":
            differenceintime = variables.current_time-self.animationtime
            es = variables.expanimationspeed
            timefactor = differenceintime/es
            expgained = self.newexp - self.oldexp
            classvar.player.exp = self.oldexp + expgained*timefactor
            if classvar.player.exp >= self.newexp:
                classvar.player.exp = self.newexp
                if stathandeling.explv(self.oldexp) < stathandeling.explv(self.newexp):
                    classvar.player.heal()
                self.state = "got exp"
            classvar.player.lv = stathandeling.explv(classvar.player.exp)

        #check for end of beatmap
        elif self.state == "dance":
            if len(self.beatmaps[self.current_beatmap].notes) == 0:
                scores = self.beatmaps[self.current_beatmap].scores
                self.damage_multiplier = sum(scores)/len(scores)
                #if they did not miss any
                if(not (variables.miss_value in scores)):
                    self.damage_multiplier += variables.perfect_value
                self.beatmaps[self.current_beatmap].reset_buttons()
                self.trade()


    def onkey(self, key):
        if self.state == 'dance':
            self.beatmaps[self.current_beatmap].onkey(key)
        if self.state == "choose":
            if key in variables.enterkeys:
                if self.option == 1:
                    self.state = "dance"
                    self.next_beatmap()
                else:
                    variables.state = "world"
            else:
                if self.option == 1:
                    self.option = 2
                else:
                    self.option = 1
        elif self.state == "lose" and key in variables.enterkeys:
            #go home
            classvar.player.heal()
            variables.state = "world"
            maps.change_map(maps.home_map)
            classvar.player.teleport(maps.current_map.startpoint[0], maps.current_map.startpoint[1])
        elif self.state == "win" and key in variables.enterkeys:
            self.state = "exp"
            self.newexp = classvar.player.exp + stathandeling.exp_gained(self.enemy.lv)
            self.animationtime = variables.current_time
            self.oldexp = classvar.player.exp
        elif self.state == "got exp" and key in variables.enterkeys:
            variables.state = "world" #finally exit Battle

    def onrelease(self, key):
        if self.state == "dance":
            self.beatmaps[self.current_beatmap].onrelease(key)

    def trade(self):
        playerlv = classvar.player.lv
        enemylv = self.enemy.lv
        self.state = "attacking"
        self.oldenemyhealth = self.enemy.health
        self.oldplayerhealth = classvar.player.health
        self.animationtime = variables.current_time
        def damageplayer():
            self.newplayerhealth = classvar.player.health - stathandeling.damage(enemylv)
            if self.newplayerhealth <= 0.25:
                self.newplayerhealth = 0
        def damageenemy():
            self.newenemyhealth = self.enemy.health - stathandeling.damage(playerlv)*self.damage_multiplier
            if self.newenemyhealth <= 0.25:
                self.newenemyhealth = 0
        if playerlv > enemylv or (playerlv == enemylv and random.choice([True, False])) or \
                self.damage_multiplier>variables.perfect_value:
            self.isplayernext = False
        else:
            self.isplayernext = True
        damageenemy()
        damageplayer()

    def draw_buttons(self):
        for x in range(0, len(self.buttons)):
            self.buttons[x].draw()