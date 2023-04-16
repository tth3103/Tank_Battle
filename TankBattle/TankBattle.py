import pygame,sys,os,random
from pygame import mixer
pygame.init()

#display setup
WIDTH, HEIGHT = 1080,720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tank Battle')
P_WIDTH, P_HEIGHT = 48,60
E_WIDTH, E_HEIGHT = 32,40
B_WIDTH, B_HEIGHT = 10,10

#define color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (0,102,102)
DARK_RED =(153,0,0)
LOSE_COLOR = (25,0,51)
LEVEL_COLOR = (255,51,51)
P1_COLOR = (102,204,0)
P2_COLOR = (255,153,51)

#define game settings
FPS = 60
ENEMY_COUNT = 15

# loading assets
BG_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','background.png')),(WIDTH,HEIGHT))
TANK1_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','Tank_Green.png')),(P_WIDTH,P_HEIGHT))
TANK2_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','Tank_Orange.png')),(P_WIDTH,P_HEIGHT))
ENEMY_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','Tank_Red.png')),(E_WIDTH,E_HEIGHT))
P1_BULLET_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','P1_Bullet.png')),(B_WIDTH,B_HEIGHT))
P2_BULLET_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','P2_Bullet.png')),(B_WIDTH,B_HEIGHT))
E_BULLET_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','E_Bullet.png')),(B_WIDTH,B_HEIGHT))

#SFX and BGM
BGM = os.path.join('Assets','BGM','Boss10.wav')
lost_music = os.path.join('Assets','BGM','Boss15.wav')
pygame.mixer.music.load(BGM)
pygame.mixer.music.play(-1)
hit_sound = pygame.mixer.Sound(os.path.join('Assets','SFX','hit.wav'))
explode_sound = pygame.mixer.Sound(os.path.join('Assets','SFX','explosion.wav'))
launch_sound = pygame.mixer.Sound(os.path.join('Assets','SFX','launcher.wav'))

#Tank class
class Tank:
    COOLDOWN = 30
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
  
    def move_left(self):
        if self.x - self.speed > 0:
            self.angle = 90
            self.x -= self.speed

    def move_right(self):
        if self.x + self.speed + self.get_width() < WIDTH:
            self.angle = -90
            self.x += self.speed

    def move_up(self):
        if self.y - self.speed > 0:
            self.angle = 0
            self.y -= self.speed

    def move_down(self):
        if self.y + self.speed + self.get_height() < HEIGHT:
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
            if bullet.off_screen(HEIGHT,WIDTH):
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

#Player class 
class Player(Tank):
    def __init__(self, x, y, lives,tank_img, bullet_img):
        super().__init__(x, y, lives)
        self.tank_img = tank_img
        self.bullet_img = bullet_img
        self.mask = pygame.mask.from_surface(self.tank_img)
        self.max_lives = lives
        self.launch_sfx = launch_sound

    def move_bullet(self,objs):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(bullet.direction)
            if bullet.off_screen(HEIGHT,WIDTH):
                self.bullets.remove(bullet)
            else:
                for obj in objs[:]:
                    if bullet.collision(obj):
                        pygame.mixer.Sound.play(explode_sound)
                        objs.remove(obj)
                        if len(self.bullets) <= 0:
                            return
                        else:
                            self.bullets.remove(bullet)
    def lose_lives(self,amount):
        if self.max_lives == 0:
            pygame.mixer.Sound.play(explode_sound)
            self.destroy()
        else:
            pygame.mixer.Sound.play(hit_sound)
            self.max_lives -= amount

class Enemy(Tank):
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

    def move_bullet(self,objs):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(bullet.direction)
            if bullet.off_screen(HEIGHT,WIDTH):
                self.bullets.remove(bullet)
            else:
                for obj in objs:
                    if bullet.collision(obj):
                        if obj.max_lives == 0:
                            objs.remove(obj)
                        else:
                            obj.lose_lives(1)
                            self.bullets.remove(bullet)
            
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

def check_collision(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def check_direction(angle):
    if angle == 0 or angle == 180:
        return True
    else: 
        return False
    

def main():
    clock=pygame.time.Clock()
    run = True
    player_1=Player(200,350,3,TANK1_IMAGE,P1_BULLET_IMAGE)
    player_2=Player(450,350,3,TANK2_IMAGE,P2_BULLET_IMAGE)
    main_font = pygame.font.SysFont("comicsans",30)
    notif_font = pygame.font.SysFont("comicsans",70)
    lost = False
    level = 0
    lost_timer = 0
    bullet_speed = 4
    enemies = []
    players = [player_1,player_2]
    def redraw_window():
        WIN.blit(BG_IMAGE,(0,0))

        #draw text
        lives_label_1 = main_font.render(f"P1 Lives:{player_1.max_lives}",1, P1_COLOR)
        lives_label_2 = main_font.render(f"P2 Lives:{player_2.max_lives}",1, P2_COLOR)
        lives_label_3 = main_font.render(f"Remaining:{len(enemies)}",1, DARK_RED)
        lives_label_4 = main_font.render(f"Level {level}",1, LEVEL_COLOR)
        WIN.blit(lives_label_1,(20,10))
        WIN.blit(lives_label_2,(900,10))
        WIN.blit(lives_label_3,(630,10))
        WIN.blit(lives_label_4,(330,10))

        #draw component
        for player in players:
            player.draw(WIN)

        for enemy in enemies:
            enemy.draw(WIN)

        if lost:
            lost_label = notif_font.render("MISSION FAILED",1,LOSE_COLOR)
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 310))

        pygame.display.update()

    # main game loop
    while run:
        clock.tick(FPS)
        redraw_window()
        if len(enemies)==0:
            level +=1
            for player in players:
                player.max_lives+=1
            for i in range(ENEMY_COUNT):
                enemy = Enemy(random.randrange(0, WIDTH,700),random.randrange(0,HEIGHT,700),1,ENEMY_IMAGE,E_BULLET_IMAGE)
                enemies.append(enemy)
        if player_1.max_lives == 0 and player_2.max_lives == 0:
            lost = True
            lost_timer += 1
        if lost:
            pygame.mixer.music.stop()
            if lost_timer > FPS * 3:
                run = False
            else:
                continue
        for player in players:
            if player.max_lives ==0:
                players.remove(player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Handle movement
        keys = pygame.key.get_pressed()
        #Player1 movement
        if keys[pygame.K_a]:
            player_1.move_left()
        elif keys[pygame.K_d]:
            player_1.move_right()
        elif keys[pygame.K_w]:
            player_1.move_up()
        elif keys[pygame.K_s]:
            player_1.move_down()
        if keys[pygame.K_SPACE]:
            player_1.shoot(bullet_speed)
            

            #Player2 movement
        if keys[pygame.K_LEFT]:
            player_2.move_left()
        elif keys[pygame.K_RIGHT]:
            player_2.move_right()
        elif keys[pygame.K_UP]: 
            player_2.move_up()
        elif keys[pygame.K_DOWN]:
            player_2.move_down()
        if keys[pygame.K_RSHIFT]:
            player_2.shoot(bullet_speed)

        #Enemies movement    
        for enemy in enemies[:]:
                enemy.random_move()
                enemy.shoot(bullet_speed)
                enemy.move_bullet(players)

        player_1.move_bullet(enemies)
        player_2.move_bullet(enemies)
        pygame.display.flip()

if __name__ == '__main__':
    main()      