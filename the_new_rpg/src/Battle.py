#!/usr/bin/python
#Oliver works on classes
import variables, pygame, stathandeling, classvar, random, graphics

class Battle():
    #for attacking animation
    isplayernext = False #if the player is currently being damaged
    oldenemyhealth = 20
    oldplayerhealth = 20
    newplayerhealth = 10
    newenemyhealth = 10

    #animation time is used for all animations
    animationtime = 0

    def __init__(self, enemy):
        self.enemy = enemy
        self.state = "choose"
        self.option = 1
        self.enemy.pic = pygame.transform.scale(self.enemy.pic, [int(variables.width/5), int(variables.height/5)])

    def draw(self):
        h = variables.height
        w = variables.width
        b = h*13/16
        p = classvar.player
        #background
        pygame.draw.rect(variables.screen, variables.BLACK, [0, 0, w, h])

        if self.state == "choose":
            if self.option == 1:
                dancerectcolor = variables.GREEN
                fleerectcolor = variables.WHITE
            else:
                dancerectcolor = variables.WHITE
                fleerectcolor = variables.GREEN

            #enemy name
            enemyname = variables.font.render("LV "+str(self.enemy.lv) + " " + self.enemy.name + " appears!", 0,
                                              variables.WHITE)
            enemynamescaled = graphics.sscale(enemyname)
            variables.screen.blit(enemynamescaled, [w/2-(enemynamescaled.get_width()/2), h/2])

            #two buttons
            pygame.draw.rect(variables.screen, dancerectcolor, [w/10, b, w/2 - (w/5), h*3/16 - h/10])
            pygame.draw.rect(variables.screen, fleerectcolor, [w/2+w/10, b, w/2 - (w/5), h*3/16 - h/10])
            dancepic = variables.font.render("DANCE!", 0, variables.BLACK)
            dance = pygame.transform.scale(dancepic, [int(w/2 - (w/5)), int(h*3/16 - h/10)])
            fleepic = variables.font.render("flee....", 0, variables.BLACK)
            flee = pygame.transform.scale(fleepic, [int(w/2 - (w/5)), int(h*3/16 - h/10)])
            variables.screen.blit(dance, [w/10, b])
            variables.screen.blit(flee, [w/2+w/10, b])

        elif self.state == "dance":
            dancerectcolor = variables.GREEN
            pygame.draw.rect(variables.screen, dancerectcolor, [w/2-(w/2 - (w/5))/2, b, w/2 - (w/5), h*3/16 - h/10])
            dancepic = variables.font.render("DANCE!", 0, variables.BLACK)
            dance = pygame.transform.scale(dancepic, [int(w/2 - (w/5)), int(h*3/16 - h/10)])
            variables.screen.blit(dance, [w/2-(w/2 - (w/5))/2, b])

        elif self.state == "lose" or self.state == "win":
            #button
            rectcolor = variables.GREEN
            pygame.draw.rect(variables.screen, rectcolor, [w/2-(w/2 - (w/5))/2, b, w/2 - (w/5), h*3/16 - h/10])
            if self.state== "lose":
                continuepic = variables.font.render("go home", 0, variables.BLACK)
            else:
                continuepic = variables.font.render("continue", 0, variables.BLACK)
            text = pygame.transform.scale(continuepic, [int(w/2 - (w/5)), int(h*3/16 - h/10)])
            variables.screen.blit(text, [w/2-(w/2 - (w/5))/2, b])

            #text
            if self.state == "lose":
                text = variables.font.render("your confidence has never been so low...", 0, variables.WHITE)
            else:
                text = variables.font.render("you win!", 0, variables.WHITE)
            textscaled = graphics.sscale(text)
            variables.screen.blit(textscaled, [w/2-(textscaled.get_width()/2), h/2])


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
        barlabelunscaled = variables.font.render("Confidence "+str(p.health)+" / "+str(playermaxh), 0, variables.WHITE)
        barlabel = pygame.transform.scale(barlabelunscaled, [int(healthh*5), int(healthh*2/3)])
        variables.screen.blit(barlabel, [0,h-2-healthh-healthh/2])

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

    #for things like the attack animation
    def ontick(self):
        if self.state == "attacking":
            if self.isplayernext == True:
                damage = self.oldplayerhealth - self.newplayerhealth
                differenceintime = pygame.time.get_ticks()-self.animationtime
                hs = variables.healthanimationspeed
                damagefactor = (hs-differenceintime)/hs
                #set player's health to somewhere between the old and new depending on time (damagefactor)
                classvar.player.health = self.newplayerhealth + damage*damagefactor
                #if the player's health is now at the end of the animation
                if classvar.player.health <= self.newplayerhealth:
                    classvar.player.health = self.newplayerhealth#set it to the new health when done
                    if self.newplayerhealth <= 0:
                        self.state = "lose"
                    if self.newenemyhealth == self.enemy.health: #if done with the animation
                        self.state = "dance" #exit
                    else:
                        self.isplayernext = False
                        self.animationtime = pygame.time.get_ticks()
            elif self.isplayernext == False:
                damage = self.oldenemyhealth - self.newenemyhealth
                differenceintime = pygame.time.get_ticks()-self.animationtime
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
                        self.animationtime = pygame.time.get_ticks()


    def onkey(self, key):
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
        elif self.state == "lose":
            #reset game
            variables.state = "world"
        elif self.state == "win":
            self.state = "exp"

    def trade(self):
        playerlv = classvar.player.lv
        enemylv = self.enemy.lv
        self.state = "attacking"
        self.oldenemyhealth = self.enemy.health
        self.oldplayerhealth = classvar.player.health
        self.animationtime = pygame.time.get_ticks()
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