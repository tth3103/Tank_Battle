import pygame, sys, os, random
from Player import Player
from Enemy import Enemy
pygame.init()

# DISPLAY SETUP
WIDTH, HEIGHT = 680,550
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tank Battle')
P_WIDTH, P_HEIGHT = 48,60
E_WIDTH, E_HEIGHT = 40,48
B_WIDTH, B_HEIGHT = 12,12
BT_WIDTH, BT_HEIGHT = 200,78
BT_PLAY_X = (WIDTH - BT_WIDTH) //2
BT_PLAY_Y = HEIGHT - 300
BT_QUIT_X = (WIDTH - BT_WIDTH) //2
BT_QUIT_Y = HEIGHT - 185

# DEFINE COLOR CONSTANT
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (0,102,102)
DARK_RED =(153,0,0)
LOSE_COLOR = (25,0,51)
LEVEL_COLOR = (255,51,51)
P1_COLOR = (102,204,0)

# DEFINE GAME SETTINGS
FPS = 60
ENEMY_COUNT = 2

# LOADING ASSETS
BG_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','background_4.png')),(WIDTH,HEIGHT))
MENU_BG_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','menu_bg.png')),(WIDTH,HEIGHT))
TANK_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','Tank_Green.png')),(P_WIDTH,P_HEIGHT))
ENEMY_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','Tank_Red.png')),(E_WIDTH,E_HEIGHT))
P_BULLET_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','P1_Bullet.png')),(B_WIDTH,B_HEIGHT))
E_BULLET_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','E_Bullet.png')),(B_WIDTH,B_HEIGHT))
BT_PLAY_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','BT_Play.png')),(BT_WIDTH,BT_HEIGHT))
BT_QUIT_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','BT_Quit.png')),(BT_WIDTH,BT_HEIGHT))

#SFX & BGM
BGM = os.path.join('Assets','BGM','Boss10.wav')
BGM_MENU = os.path.join('Assets','BGM','Boss27.wav')
BGM_LOST = os.path.join('Assets','BGM','Boss15.wav')
hit_sound = pygame.mixer.Sound(os.path.join('Assets','SFX','hit.wav'))
explode_sound = pygame.mixer.Sound(os.path.join('Assets','SFX','explosion.wav'))
launch_sound = pygame.mixer.Sound(os.path.join('Assets','SFX','launcher.wav'))  
main_font = pygame.font.SysFont("comicsans",30,True)
tittle_font = pygame.font.SysFont("comicsans",80,True)
notif_font = pygame.font.SysFont("comicsans",70,True)

def main_game_loop():
    pygame.mixer.music.load(BGM)
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    run = True
    player=Player(200,350,2,TANK_IMAGE,P_BULLET_IMAGE,launch_sound,hit_sound,explode_sound)
    bgm_changed = False
    lost = False
    day = 0
    lost_timer = 0
    bullet_speed = 6
    enemies = []

    def redraw_window():
        WIN.blit(BG_IMAGE,(0,0))
#--------------------------------------------------DRAW GAME OBJECT--------------------------------------------------#
        player.draw(WIN)

        for enemy in enemies:
            enemy.draw(WIN)
#--------------------------------------------------DRAW UI LABEL--------------------------------------------------#
        lives_label_1 = main_font.render(f"Lives:{player.max_lives}",1, P1_COLOR)
        remaining_label = main_font.render(f"Remaining:{len(enemies)}",1, WHITE)
        days_label = main_font.render(f"Day {day}",1, LEVEL_COLOR)
        WIN.blit(lives_label_1,(10,10))
        WIN.blit(remaining_label,(WIDTH/2 - remaining_label.get_width()/2, 10))
        WIN.blit(days_label,(WIDTH - days_label.get_width()-20, 10))
#--------------------------------------------------DRAW LOST LABEL--------------------------------------------------#
        if lost:
            lost_label = notif_font.render("YOU LOST",1,LOSE_COLOR)
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2))

        pygame.display.update()

#----------------------------------------------------GAME LOOP-----------------------------------------------------#
    while run:
        clock.tick(FPS)
        redraw_window()
        if len(enemies) == 0:
            day +=1
            if player.max_lives <5:
                player.max_lives+=1

            for i in range(ENEMY_COUNT+day):
                enemy = Enemy(random.randrange(10, WIDTH-30,60),random.randrange(10,HEIGHT-30,60),1,ENEMY_IMAGE,E_BULLET_IMAGE)
                enemies.append(enemy)
        if player.max_lives == 0:
            lost = True
            lost_timer += 1
        
        #LOST HANDLE
        if lost:
            if not bgm_changed:
                pygame.mixer.music.load(BGM_LOST)
                pygame.mixer.music.play(-1)
                bgm_changed = True
            if lost_timer > FPS * 5:
                run = False
            else:
                continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # PLAYER MOVEMENT HANDLE
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.move_left()
        elif keys[pygame.K_d]:
            player.move_right()
        elif keys[pygame.K_w]:
            player.move_up()
        elif keys[pygame.K_s]:
            player.move_down()
        if keys[pygame.K_SPACE]:
            player.shoot(bullet_speed)
            
        #ENEMIES AI CONTROLLER    
        for enemy in enemies[:]:
                enemy.random_move()
                enemy.shoot(bullet_speed)
                enemy.move_bullet(player)
      
        player.collide_with_enemy(enemies)
        player.move_bullet(enemies)
        pygame.display.flip()
    pygame.mixer.music.load(BGM_MENU)
    pygame.mixer.music.play(-1)
#--------------------------------------------------MENU SCREEN-------------------------------------------------#
def game_start_loop():
    pygame.mixer.music.load(BGM_MENU)
    pygame.mixer.music.play(-1)
    while True:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pygame.Rect(BT_PLAY_X, BT_PLAY_Y, BT_WIDTH, BT_HEIGHT).collidepoint(pos):
                    main_game_loop()
                elif pygame.Rect(BT_QUIT_X, BT_QUIT_Y, BT_WIDTH, BT_HEIGHT).collidepoint(pos):
                    sys.exit()
        pygame.display.update()

#--------------------------------------------------DRAW MENU SCREEN---------------------------------------------#
def draw_menu():
    WIN.blit(MENU_BG_IMAGE,(0,0))
    tittle_label = tittle_font.render(f"TANK BATTLE",1, WHITE)
    WIN.blit(tittle_label,(WIDTH//2-tittle_label.get_width()/2,60))
    WIN.blit(BT_PLAY_IMAGE,(BT_PLAY_X,BT_PLAY_Y))
    WIN.blit(BT_QUIT_IMAGE,(BT_QUIT_X,BT_QUIT_Y))
    

if __name__ == '__main__':
    game_start_loop()      