import pygame
from Tank import Tank
from utils import check_collision

class Player(Tank):
    WIDTH ,HEIGHT = 680,550
    def __init__(self, x, y, lives,tank_img, bullet_img,launch_sound,hit_sound,explode_sound):
        super().__init__(x, y, lives)
        self.tank_img = tank_img
        self.bullet_img = bullet_img
        self.mask = pygame.mask.from_surface(self.tank_img)
        self.max_lives = lives
        self.launch_sfx = launch_sound
        self.hit_sfx=hit_sound
        self.explode_sfx = explode_sound

    def move_bullet(self,objs):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(bullet.direction)
            if bullet.off_screen(self.HEIGHT,self.WIDTH):
                self.bullets.remove(bullet)
            else:
                for obj in objs[:]:
                    if bullet.collision(obj):
                        pygame.mixer.Sound.play(self.explode_sfx)
                        objs.remove(obj)
                        if len(self.bullets) <= 0:
                            return
                        else:
                            try:
                                self.bullets.remove(bullet)
                            except:
                                return

    def lose_lives(self,amount):
        if self.max_lives == 0:
            pygame.mixer.Sound.play(self.explode_sfx)
            self.destroy()
        else:
            pygame.mixer.Sound.play(self.hit_sfx)
            self.max_lives -= amount

    def collide_with_enemy(self,objs):
        for obj in objs[:]:
            if check_collision(self,obj):
                objs.remove(obj)
                self.lose_lives(1)