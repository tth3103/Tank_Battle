import pygame, random
from Tank import Tank

class Enemy(Tank):
    WIDTH ,HEIGHT = 680,550
    def __init__(self, x, y, lives,tank_img,bullet_img):
        super().__init__(x, y, lives)
        self.tank_img = tank_img
        self.bullet_img = bullet_img
        self.mask = pygame.mask.from_surface(self.tank_img)
        self.max_lives = lives
        self.speed = 2
        self.mv_cd_counter = 0
        self.dir = 0
        self.MOVEMENT_CD = random.randrange(60,60*5,60)
        self.COOLDOWN = random.randrange(60,60*5,30)
    def movement_cooldown(self):
        if self.mv_cd_counter >= self.MOVEMENT_CD:
            self.mv_cd_counter = 0
        elif self.mv_cd_counter > 0:
            self.mv_cd_counter += 1

    def random_move(self):
        self.get_direction()
        self.movement_cooldown()
        if self.dir == 1:
            self.move_down()
        if self.dir == 2:
            self.move_up()
        if self.dir == 3:
            self.move_left()
        if self.dir == 4:
            self.move_right()
    
    def get_direction(self):
        if self.mv_cd_counter == 0:
            direction = ["up", "down", "left", "right"]
            ran = random.choice(direction)
            if ran == "down":
                self.dir= 1
            if ran == "up":
                self.dir= 2
            if ran == "left":
                self.dir= 3
            if ran == "right":
                self.dir= 4
            self.mv_cd_counter = 1

    def move_bullet(self,obj):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(bullet.direction)
            if bullet.off_screen(self.HEIGHT,self.WIDTH):
                self.bullets.remove(bullet)
            else:
                if bullet.collision(obj):
                 obj.lose_lives(1)
                 self.bullets.remove(bullet)

    