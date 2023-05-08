import pygame
from utils import check_collision

class Bullet:
    def __init__(self,x ,y ,bullet_img,direction,vel):
        self.x = x
        self.y = y
        self.bullet_img = bullet_img
        self.mask = pygame.mask.from_surface(self.bullet_img)
        self.direction= direction
        self.vel = vel

    def move(self, direction):
        if direction == False:
            self.x += self.vel
            return
        elif direction == True:
            self.y += self.vel
            return
        
    def draw(self,window):
        window.blit(self.bullet_img, (self.x, self.y))
    
    def off_screen(self, height,width):
        return not (self.y <= height and self.y >= 0 and self.x <= width and self.x >= 0) 
    def collision(self ,obj):
        return check_collision(self,obj)

