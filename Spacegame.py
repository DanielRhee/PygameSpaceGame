import pygame
import os
import time
import math
import random

pygame.init()
global window
window = pygame.display.set_mode([800,500])
pygame.display.set_caption("Space Game")

class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Background.png").convert()
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.speed = 0
        self.rect.center = self.x,self.y

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        global player
        self.rotation = player.rotation
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load("Laser.png")
        self.image = pygame.transform.rotate(pygame.transform.scale(self.original_image,(10,2)), self.rotation+90)
        self.rect = self.image.get_rect()
        self.x = player.x
        self.y = player.y
        #How far the laser can travel
        self.range = 200
        self.x_velocity = 0
        self.y_velocity = 0
        self.speed = 15
        self.rect.center = self.x,self.y
        self.delete = False
    def move(self):
        #subtract from the range 
        self.range -= self.speed
        #move it. Yeah this is the code copied over from the player @future me
        self.x_velocity = math.sin(math.radians(360-self.rotation))*self.speed
        self.y_velocity = math.cos(math.radians(360-self.rotation))*self.speed
        self.x += self.x_velocity
        self.y -= self.y_velocity

        self.rect.center = self.x,self.y
    def update(self):
        if self.x > 800:
            self.x -= 800
        elif self.x < 0:
            self.x += 800
        if self.y > 500:
            self.y -= 500
        elif self.y < 0:
            self.y += 500
        if self.range < 0:
            self.delete = True

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rotation = 0
        #self.image = pygame.transform.scale(pygame.image.load("/Users/daniel/Documents/SpaceGame/SpaceShip1.png"), (40, 40))
        #self.image = pygame.transform.rotate(pygame.image.load("/Users/daniel/Documents/SpaceGame/SpaceShip1.png"), 90)
        #self.image = pygame.transform.scale(pygame.transform.rotate(pygame.image.load("/Users/daniel/Documents/SpaceGame/SpaceShip1.png"), self.rotation),(30,30))
        self.original_image = pygame.image.load("SpaceShip1.png")
        self.image = pygame.transform.scale(self.original_image,(40,40))
        self.rect = self.image.get_rect()
        self.x = 400
        self.y = 250
        self.x_velocity = 0
        self.y_velocity = 0
        self.speed = 0
        self.rect.center = self.x,self.y
        self.health = 100
    def forward(self):
        #Somehow makes it move forward. Idk don't touch it
        self.x_velocity = math.sin(math.radians(360-self.rotation))*self.speed
        self.y_velocity = math.cos(math.radians(360-self.rotation))*self.speed
        self.x += self.x_velocity
        self.y -= self.y_velocity

        self.rect.center = self.x,self.y
    def slow(self):
        #how much to slow down by
        slow_down_rate = 0.8
        if (self.x_velocity > 0.01 or self.y_velocity > 0.01) or (self.x_velocity < -0.01 or self.y_velocity < -0.01):
            #print(self.x_velocity,self.y_velocity)
            self.x_velocity *= slow_down_rate
            self.y_velocity *= slow_down_rate
    def rotate(self,angle,forward):
        self.rotation += angle*-1
        #reset rotation
        if self.rotation < 0:
            self.rotation = 360
        elif self.rotation > 360:
            self.rotation = 0
        if forward:
            forward()
        #print(self.rotation)
        self.image = pygame.transform.rotate(pygame.transform.scale(self.original_image,(40,40)), self.rotation)
        #self.image = pygame.transform.rotate(self.original_image, self.rotation)
        #self.rect = self.temp.get_rect()
        self.rect.center = self.x,self.y
    def update(self):
        #slow down
        self.x_velocity *= 0.99
        self.y_velocity *= 0.99
        #move it
        self.x += self.x_velocity
        self.y -= self.y_velocity
        self.rect.center = self.x,self.y
        # make it come around the edges
        if self.x > 800:
            self.x -= 800
        elif self.x < 0:
            self.x += 800
        if self.y > 500:
            self.y -= 500
        elif self.y < 0:
            self.y += 500
        if self.speed > 10:
            self.speed = 10
        #decrease speed to 0 to save memory. The second one is to make sure it's not some random increment
        if self.speed < 0.5 and int(self.speed) != self.speed:
            self.speed = 0
#------------------------------------------------------------------------------------#
class Enemy_Ship(pygame.sprite.Sprite):
    def __init__(self):
        self.rotation = 0
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load("shuttle.png")
        self.image = pygame.transform.scale(self.original_image,(40,40))
        self.rect = self.image.get_rect()
        self.x = random.randint(0,800)
        self.y = random.randint(0,500)
        self.x_velocity = 0
        self.y_velocity = 0
        self.speed = 10
        self.rect.center = self.x,self.y
        #health is a random number
        self.delete = False
        self.health = random.randint(1,15)
    def move(self,choice):
        if choice == 1:
            #print("hi")
            self.forward()
        elif choice == 2:
            self.rotate(-15)
        else:
            self.rotate(15)
    def forward(self):
        #Somehow makes it move forward. Idk don't touch it
        self.x_velocity = math.sin(math.radians(360-self.rotation))*self.speed
        self.y_velocity = math.cos(math.radians(360-self.rotation))*self.speed
        self.x += self.x_velocity
        self.y -= self.y_velocity

    def rotate(self,angle,forward=False):
        self.rotation += angle*-1
        #reset rotation
        if self.rotation < 0:
            self.rotation = 360
        elif self.rotation > 360:
            self.rotation = 0
        if forward:
            forward()
        #print(self.rotation)
        self.image = pygame.transform.rotate(pygame.transform.scale(self.original_image,(40,40)), self.rotation)
        #self.image = pygame.transform.rotate(self.original_image, self.rotation)
        #self.rect = self.temp.get_rect()
        self.rect.center = self.x,self.y
    def update(self):
        if self.health < 0:
            self.delete = True
        #slow down
        self.x_velocity *= 0.99
        self.y_velocity *= 0.99
        #move it
        self.x += self.x_velocity
        self.y -= self.y_velocity
        self.rect.center = self.x,self.y
        # make it come around the edges
        if self.x > 800:
            self.x -= 800
        elif self.x < 0:
            self.x += 800
        if self.y > 500:
            self.y -= 500
        elif self.y < 0:
            self.y += 500
        if self.speed > 10:
            self.speed = 10
        #decrease speed to 0 to save memory. The second one is to make sure it's not some random increment
        if self.speed < 0.5 and int(self.speed) != self.speed:
            self.speed = 0
class Button(pygame.sprite.Sprite):
    def __init__(self):
        self.rotation = 90
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load("Laser2.png")
        self.image = pygame.transform.rotate(pygame.transform.scale(self.original_image,(200,100)), self.rotation+90)
        self.rect = self.image.get_rect()
        self.rect.center = 400,250
class Enemy_Laser(pygame.sprite.Sprite):
    def __init__(self,rotation,x,y):
        self.rotation = rotation
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load("Laser2.png")
        self.image = pygame.transform.rotate(pygame.transform.scale(self.original_image,(10,2)), self.rotation+90)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        #How far the laser can travel
        self.range = 400
        self.x_velocity = 0
        self.y_velocity = 0
        self.speed = 15
        self.rect.center = self.x,self.y
        self.delete = False
    def move(self):
        #subtract from the range 
        self.range -= self.speed
        #move it. Yeah this is the code copied over from the player @future me
        self.x_velocity = math.sin(math.radians(360-self.rotation))*self.speed
        self.y_velocity = math.cos(math.radians(360-self.rotation))*self.speed
        self.x += self.x_velocity
        self.y -= self.y_velocity

        self.rect.center = self.x,self.y
    def update(self):
        if self.x > 800:
            self.x -= 800
        elif self.x < 0:
            self.x += 800
        if self.y > 500:
            self.y -= 500
        elif self.y < 0:
            self.y += 500
        if self.range < 0:
            self.delete = True


def Health_Bar():
    global window
    global player
    #draw outline of health bar
    pygame.draw.rect(window, (150, 150, 150), pygame.Rect(10, 30, 103, 15),2)
    green = (140,240,50)
    yellow = (220,200,53)
    orange = (220,150,50)
    red = (200,50,50)
    if player.health == 100:
        color = green
    elif player.health > 70:
        color = yellow
    elif player.health > 30:
        color = orange
    else:
        color = red
    for i in range(12, player.health+12):
        pygame.draw.rect(window, color, pygame.Rect(i, 32, 1, 12),1)   
def start():
    start_time = time.time()
    global player
    player = Player()
    background = Background()
    c = pygame.time.Clock()
    playing = True
    keydown = False
    left_arrow_down = False
    right_arrow_down = False
    up_arrow_down = False
    down_arrow_down = False
    global lasers
    lasers = []
    global enemy_lasers
    enemy_lasers = []
    kills = 0
    global enemies
    enemies = []
    enemies.append(Enemy_Ship())
    exited = False
    font = pygame.font.SysFont("Times new Roman", 17) 
    text = font.render("Health:", True, (255, 255, 255))  
    while playing:
        window.fill((60,205,60))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exited = True
                playing = False
            #key stuff
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not keydown:
                    left_arrow_down = True
                    keydown = True
                if event.key == pygame.K_RIGHT and not keydown:
                    right_arrow_down = True
                    keydown = True
                if event.key == pygame.K_UP and not keydown:
                    up_arrow_down = True
                    keydown = True
                if event.key == pygame.K_DOWN and not keydown:
                    down_arrow_down = True
                    keydown = True
                elif event.key == pygame.K_SPACE:
                    lasers.append(Laser())
            #if a key is up stop it
            if event.type == pygame.KEYUP:
                keydown = False
                up_arrow_down = False
                left_arrow_down = False
                right_arrow_down = False
                down_arrow_down = False
                
        if keydown:
            if left_arrow_down:
                player.rotate(-15,up_arrow_down)
            if right_arrow_down:
                player.rotate(15,up_arrow_down)
            if up_arrow_down:
                player.speed += 0.5
                player.forward()
            if down_arrow_down:
                player.slow()


        player.update()
        window.blit(background.image, background.rect)
        
        window.blit(player.image, player.rect)
        window.blit(text,(10, 10)) 
        Health_Bar()
        #Draw lasers
        #Go through enemies and move them, make them shoot, delete them etc
        iterate_enemies = 0
        max_iterate = len(enemies)
        while iterate_enemies < max_iterate:
            sprite = enemies[iterate_enemies]
            window.blit(sprite.image,sprite.rect)
            #see if it needs to be destroyed
            for temp in lasers:
                if pygame.sprite.collide_rect(sprite,temp):
                    sprite.health -= random.randint(1,4)
            window.blit(sprite.image,sprite.rect)

            #Just do this stuff. I'm only doing this becuase i don't want to unindent @future me good job 
            if True:
                enemy_choice = random.randint(1,4)
                if enemy_choice != 4:
                    #make it move 
                    sprite.move(enemy_choice)
                else:
                    #print("shooting")
                    #print(enemy.x,enemy.y)
                    #make it shoot
                    enemy_lasers.append(Enemy_Laser(sprite.rotation,sprite.x,sprite.y))
            #check if the sprite should be deleted
            if sprite.delete:
                max_iterate -= 1
                enemies.pop(iterate_enemies)
                kills += 1
            #if it doesn't delete
            else:
                #draw and update
                iterate_enemies += 1
                sprite.update()
                window.blit(sprite.image, sprite.rect)

        #Spawn new enemy?
        spawnnewenempy = random.randint(1,300)
        if spawnnewenempy == 1:
            enemies.append(Enemy_Ship())
        for sprite in enemy_lasers:
            sprite.move()
            sprite.update()
            window.blit(sprite.image,sprite.rect)
        for sprite in lasers:
            sprite.update()
            sprite.move()
            window.blit(sprite.image,sprite.rect)
        iterate_lasers = 0
        max_iterate = len(enemy_lasers)
        #delete laser stuff
        #print(max_iterate)
        #enemy laser stuff
        while iterate_lasers < max_iterate:
            #print(iterate_lasers)
            temp_laser = enemy_lasers[iterate_lasers]
            if temp_laser.delete:
                max_iterate -= 1
                enemy_lasers.pop(iterate_lasers)
            elif pygame.sprite.collide_rect(temp_laser,player):
                player.health -= random.randint(1,5)
                max_iterate -= 1
                enemy_lasers.pop(iterate_lasers)
            iterate_lasers += 1

        #Go through and delete stuff. Iterate lasers is index. max is to subtract to not screw things up
        iterate_lasers = 0
        max_iterate = len(lasers)
        while iterate_lasers < max_iterate:
            temp_laser = lasers[iterate_lasers]
            if temp_laser.delete:
                max_iterate -= 1
                lasers.pop(iterate_lasers)
            iterate_lasers += 1

        pygame.display.flip()
        c.tick(30)
        #end game?
        if player.health <= 0:
            playing = False
    #stop the game.
    #score is time/100 + kills
    font = pygame.font.SysFont("Times new Roman", 50) 
    text = font.render("Score: " +str(math.floor(time.time()-start_time/1-0+kills)), True, (255, 255, 255))  
    if not exited:
        ending = True
        while ending:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ending = False
            window.blit(text,(325, 200)) 
            pygame.display.flip()
        
if __name__ == '__main__':
    notstarting = True
    background = Background()
    #steal enemy laser sprite and stretch it
    button = Button()
    window.blit(background.image,background.rect)
    font = pygame.font.SysFont("Times new Roman", 50) 
    font2 = pygame.font.SysFont("Times new Roman",14)
    text = font.render("Start", True, (0, 0, 0))  

    text2 = font2.render("Arrow keys to move. Space to shoot. You can go through the edge and come out the other side", True, (255, 0,0))  
    while notstarting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                notstarting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if button.rect.collidepoint(x,y):
                    start()

        window.blit(button.image,button.rect)
        
        window.blit(text,(350, 218)) 
        window.blit(text2,(150,300))
        pygame.display.flip()
        #start()