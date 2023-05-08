import pygame
from Bullet import Bullet
from utils import *

class Tank:
    COOLDOWN = 30
    WIDTH ,HEIGHT = 680,550
    def __init__(self,x,y,lives):
        self.x = x
        self.y = y
        self.lives = lives
        self.speed = 2
        self.tank_img = None
        self.bullet_img = None
        self.bullets = []
        self.cd_counter = 0
        self.angle = 0
        self.launch_sfx = None
        self.hit_sfx = None
  
    def move_left(self):
        if self.x - self.speed > 0:
            self.angle = 90
            self.x -= self.speed

    def move_right(self):
        if self.x + self.speed + self.get_width() < self.WIDTH:
            self.angle = -90
            self.x += self.speed

    def move_up(self):
        if self.y - self.speed > 0:
            self.angle = 0
            self.y -= self.speed

    def move_down(self):
        if self.y + self.speed + self.get_height() < self.HEIGHT:
            self.angle = 180
            self.y += self.speed
    
    def shoot(self,vel):
        direction = check_direction(self.angle)
        if self.check_vel():
            vel= - vel
        if self.cd_counter == 0:
            if(self.launch_sfx != None):
                pygame.mixer.Sound.play(self.launch_sfx)
            bullet = Bullet( self.x+ self.get_width()/2, self.y +self.get_height()/2 , self.bullet_img,direction,vel)
            self.bullets.append(bullet)
            self.cd_counter = 1

    def cooldown(self):
        if self.cd_counter >= self.COOLDOWN:
            self.cd_counter = 0
        elif self.cd_counter > 0:
            self.cd_counter += 1

    def move_bullet(self,obj):
        self.cooldown()
        for bullet in self.bullets:
            if bullet.off_screen(self.HEIGHT,self.WIDTH):
                self.bullets.remove(bullet)
            elif bullet.collision(obj):
                obj.lives -=1
                self.bullets.remove(bullet)  
            bullet.move(bullet.direction)

    def check_vel(self):
        if self.angle == 0 or self.angle ==90:
            return True
        else:
            return False
    
    def draw(self,window):
        rotated_image = pygame.transform.rotate(self.tank_img,self.angle)
        window.blit(rotated_image,rotated_image.get_rect(center=self.tank_img.get_rect(topleft=(self.x, self.y)).center).topleft)
        for bullet in self.bullets:
            bullet.draw(window)

    def hit(self, bullet):
        if check_collision(self, bullet):
            self.destroy()
            bullet.destroy()
            self.lives -= 1

    def destroy(self):
        self.visible = False

    def get_width(self):
        return self.tank_img.get_width()
    def get_height(self):
        return self.tank_img.get_height()
