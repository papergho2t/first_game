import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
SETTINGS_BUTTON_FONT = pygame.font.SysFont('comicsans', 20)
SETTINGS_FONT = pygame.font.SysFont('comicsans', 40)

FPS = 60
VEL = 5
BULLET_VEL = 7
CHARGED_BULLET_VEL = 3

MAX_BULLETS = 3
MAX_CHARGED_BULLETS = 5


SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 55 # we end up rotating these by 90 degrees so they end up swaping later, ie, width = 55 and height = 40 after the rotation

YELLOW_HIT = pygame.USEREVENT + 1
CHARGED_YELLOW_HIT = pygame.USEREVENT + 10

RED_HIT = pygame.USEREVENT + 2
CHARGED_RED_HIT = pygame.USEREVENT + 20

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, bullet_list_count):
    #WIN.fill(WHITE)
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_charged_count = bullet_list_count[0]
    yellow_charged_count = bullet_list_count[1]
    
    red_health_text = HEALTH_FONT.render('Health: ' + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render('Health: ' + str(yellow_health), 1, WHITE)
    red_charged_bullet_text = HEALTH_FONT.render('Charged Shots: ' + str(red_charged_count), 1, WHITE)
    yellow_charged_bullet_text = HEALTH_FONT.render('Charged Shots: ' + str(yellow_charged_count), 1, WHITE)
    settings_button_text = SETTINGS_BUTTON_FONT.render('settings: esc key', 1, WHITE)


    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10,10))
    
    WIN.blit(red_charged_bullet_text, (WIDTH - red_charged_bullet_text.get_width() - 10, red_health_text.get_height() + 10))
    WIN.blit(yellow_charged_bullet_text, (10, yellow_health_text.get_height() + 10))

    WIN.blit(settings_button_text, (WIDTH//2 - settings_button_text.get_width()//2, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet_item in red_bullets:
        bullet = bullet_item[0]
        pygame.draw.rect(WIN, RED, bullet)

    for bullet_item in yellow_bullets:
        bullet = bullet_item[0]
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def draw_settings():
    WIN.blit(SPACE, (0,0))
   
    yellow_controls_text = SETTINGS_FONT.render('Yellow Ship Controls', 1, WHITE)
    red_controls_text = SETTINGS_FONT.render('Red Ship Controls', 1, WHITE)

    yellow_movement_text = SETTINGS_FONT.render('Movement: WASD', 1, WHITE)
    red_movement_text = SETTINGS_FONT.render('Movement: Arrow Keys', 1, WHITE)

    yellow_fire_text = SETTINGS_FONT.render('Bullet: Left Ctrl, Charged Bullet: z', 1, WHITE)
    red_fire_text = SETTINGS_FONT.render('Bullet: Right Ctrl, Charged Bullet: /', 1, WHITE)

    WIN.blit(yellow_controls_text, (10, 10))
    WIN.blit(yellow_movement_text, (10, yellow_movement_text.get_height() + 10))
    WIN.blit(yellow_fire_text, (10, 2*yellow_fire_text.get_height() + 10))
    
    WIN.blit(red_controls_text, (10, 4*red_controls_text.get_height() + 10))
    WIN.blit(red_movement_text, (10, 5*red_movement_text.get_height() + 10))
    WIN.blit(red_fire_text, (10, 6*red_fire_text.get_height() + 10))

    pygame.display.update()
    pygame.time.delay(8000) # 1000 miliseconds = 1 second

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # left movement key
        yellow.x -= VEL 
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # right movement key
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # up movement key
        yellow.y -= VEL 
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: # down movement key
        yellow.y += VEL
        
        
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # left movement key
        red.x -= VEL 
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # right movement key
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # up movement key
        red.y -= VEL 
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: # down movement key
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet_item in yellow_bullets:
        bullet = bullet_item[0]
        bullet.x += BULLET_VEL
        
        # here we handle if getting hit by a regular or charged bullet. 0 = regular, 1 = charged
        if red.colliderect(bullet) and bullet_item[1] == 0:
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet_item)
        elif red.colliderect(bullet) and bullet_item[1] == 1:
            pygame.event.post(pygame.event.Event(CHARGED_RED_HIT))
            yellow_bullets.remove(bullet_item)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet_item)

    for bullet_item in red_bullets:
        bullet = bullet_item[0]
        bullet.x -= BULLET_VEL
        
        # here we handle if getting hit by a regular or charged bullet. 0 = regular, 1 = charged
        if yellow.colliderect(bullet) and bullet_item[1] == 0:
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet_item)
        elif yellow.colliderect(bullet) and bullet_item[1] == 1:
            pygame.event.post(pygame.event.Event(CHARGED_YELLOW_HIT))
            red_bullets.remove(bullet_item)
        elif bullet.x < 0:
            red_bullets.remove(bullet_item)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1 ,WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2 , HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000) # 5000 miliseconds

def main():

    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
   
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10
    
    charged_bullet_counter_red = MAX_CHARGED_BULLETS
    charged_bullet_counter_yellow = MAX_CHARGED_BULLETS

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                
                if len(yellow_bullets) < MAX_BULLETS:
                    # regular bullet
                    if event.key == pygame.K_LCTRL:
                        bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                        yellow_bullets.append([bullet, 0]) # 0 = regular bullet ID
                        BULLET_FIRE_SOUND.play()
                    
                    # charged bullet
                    if (event.key == pygame.K_z) and (charged_bullet_counter_yellow > 0):
                        charged_bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 30, 15)
                        yellow_bullets.append([charged_bullet, 1]) # 1 = charged bullet ID
                        charged_bullet_counter_yellow -= 1
                        BULLET_FIRE_SOUND.play()
                
                if len(red_bullets) < MAX_BULLETS:
                    # regular bullet
                    if event.key == pygame.K_RCTRL:
                        bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                        red_bullets.append([bullet, 0]) # 0 = regular bullet ID
                        BULLET_FIRE_SOUND.play()

                    # charged bullet
                    if (event.key == pygame.K_SLASH) and (charged_bullet_counter_red > 0):
                        charged_bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 30, 15)
                        red_bullets.append([charged_bullet, 1]) # 1 = charged bullet ID
                        charged_bullet_counter_red -= 1
                        BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_ESCAPE:
                    draw_settings()

        
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == CHARGED_RED_HIT:
                red_health -= 2
                BULLET_HIT_SOUND.play()
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == CHARGED_YELLOW_HIT:
                yellow_health -= 2
                BULLET_HIT_SOUND.play()
        
        winner_text = ''
        if red_health <= 0:
            winner_text = 'Yellow Wins!'

        if yellow_health <= 0:
            winner_text = 'Red Wins!'

        if winner_text != '':
            draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, bullet_count_list)
            draw_winner(winner_text)
            break

        bullet_count_list = [charged_bullet_counter_red, charged_bullet_counter_yellow]
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, bullet_count_list)
   
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

    #main()

if __name__ == "__main__":
    while True:
        main()
