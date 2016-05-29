#!/usr/bin/python
#Oliver works on classes
import variables, pygame, stathandeling, classvar, random, graphics, maps
from Button import Button
from Beatmap import Beatmap
from Note import Note

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

    def __init__(self, enemy):
        self.enemy = enemy
        self.state = "choose"
        self.option = 1
        self.enemy.pic = graphics.scale_pure(self.enemy.pic, variables.width/5)
        self.beatmap = Beatmap(1000, [Note(1, 1, 1), Note(2, 2, 1), Note(8, 2, 3), Note(6, 3, 0.5)], [])

    def draw(self):
        h = variables.height
        w = variables.width
        b = h*13/16
        p = classvar.player
        #background
        pygame.draw.rect(variables.screen, variables.BLACK, [0, 0, w, h])

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

        elif self.state == "dance":
            dancebutton = Button(w/2, b, "DANCE!", 1.5)
            dancebutton.ison = True
            self.buttons = [dancebutton]
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
            percentofneeded = (p.exp - stathandeling.lvexp(p.lv))/stathandeling.exp_needed(p.lv)
            pygame.draw.rect(variables.screen, variables.BLUE, [0,
                                                            h/2,
                                                            w*percentofneeded,
                                                            h/18])

            #level up text
            if self.state == "got exp" and stathandeling.explv(self.oldexp) < stathandeling.explv(self.newexp):
                text = variables.font.render("LEVEL UP!", 0, variables.GREEN)
                textscaled = graphics.sscale(text)
                variables.screen.blit(textscaled, [w/2-(textscaled.get_width()/2), h/3 - textscaled.get_height()])


        epic = self.enemy.pic
        variables.screen.blit(epic, [w-epic.get_width(), 0])

        #confidece bar
        healthh = h*(1/18)
        playermaxh = stathandeling.max_health(p.lv)
        percenthealthleft = p.health/playermaxh
        if percenthealthleft<=0.2:
            healthbarcolor = variables.RED
        else:
            healthbarcolor = variables.GREEN
        pygame.draw.rect(variables.screen, healthbarcolor, [0,
                                                            h-healthh,
                                                            w*percenthealthleft,
                                                            healthh])
        barlabelunscaled = variables.font.render("Health "+str(p.health)+" / "+str(playermaxh), 0, variables.WHITE)
        barlabel = graphics.sscale_customfactor(barlabelunscaled, 0.75)
        variables.screen.blit(barlabel, [0,h-healthh-barlabel.get_height()])

        #enemy bar
        enemyhealthh = h*(1/50)
        e = self.enemy
        epicw = epic.get_width()
        epich = epic.get_height()
        percenthealthleft = e.health/stathandeling.max_health(e.lv)
        if percenthealthleft<=0.2:
            healthbarcolor = variables.RED
        else:
            healthbarcolor = variables.GREEN
        if not e.health == 0:
            pygame.draw.rect(variables.screen, healthbarcolor, [w-epicw,
                                                                epich,
                                                                epicw*percenthealthleft,
                                                                enemyhealthh])

        self.beatmap.draw()

    #for things like the attack animation
    def ontick(self):
        self.beatmap.ontick()

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
                    if classvar.player.health == self.newplayerhealth: #if done with the animation
                        self.state = "dance" #exit
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


    def onkey(self, key):
        self.beatmap.onkey(key)
        if self.state == "choose":
            if key in variables.enterkeys:
                if self.option == 1:
                    self.state = "dance"
                else:
                    variables.state = "world"
            else:
                if self.option == 1:
                    self.option = 2
                else:
                    self.option = 1
        elif self.state == "dance" and key in variables.enterkeys:
            self.trade()
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
        self.beatmap.onrelease(key)

    def trade(self):
        playerlv = classvar.player.lv
        enemylv = self.enemy.lv
        self.state = "attacking"
        self.oldenemyhealth = self.enemy.health
        self.oldplayerhealth = classvar.player.health
        self.animationtime = variables.current_time
        def damageplayer():
            self.newplayerhealth = classvar.player.health - stathandeling.damage(enemylv)
            if self.newplayerhealth <= 0:
                self.newplayerhealth = 0
        def damageenemy():
            self.newenemyhealth = self.enemy.health - stathandeling.damage(playerlv)
            if self.newenemyhealth <= 0:
                self.newenemyhealth = 0
        if playerlv > enemylv or (playerlv == enemylv and random.choice([True, False])):
            self.isplayernext = False
            damageenemy()
            damageplayer()
        else:
            self.isplayernext = True
            damageplayer()
            damageenemy()

    def draw_buttons(self):
        for x in range(0, len(self.buttons)):
            self.buttons[x].draw()