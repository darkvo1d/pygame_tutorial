import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("New Stuff")
FPS = 60
VEL = 5
BULLET_VEL = 10
BULLET_CD = 5
SS_WIDTH, SS_HEIGHT = 55, 40
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

BULLETS_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLETS_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

RED_HIT = pygame.USEREVENT + 1
YEL_HIT = pygame.USEREVENT + 2

YEL_SS_IMG = pygame.image.load(os.path.join("Assets", 'spaceship_yellow.png'))
YEL_SS = pygame.transform.rotate(pygame.transform.scale(YEL_SS_IMG, (SS_WIDTH, SS_HEIGHT)), -90)
RED_SS_IMG = pygame.image.load(os.path.join("Assets", 'spaceship_red.png'))
RED_SS = pygame.transform.rotate(pygame.transform.scale(RED_SS_IMG, (SS_WIDTH, SS_HEIGHT)), 90)
BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))


def draw_window(red, yel, red_bullets, yel_bullets, red_health, yel_health):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render(f"Health :{red_health}", 1, WHITE)
    yel_health_text = HEALTH_FONT.render(f"Health :{yel_health}", 1, WHITE)
    WIN.blit(red_health_text, (15, 10))
    WIN.blit(yel_health_text, (WIDTH - yel_health_text.get_width() - 15, 10))
    WIN.blit(YEL_SS, (yel.x, yel.y))
    WIN.blit(RED_SS, (red.x, red.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yel_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


def draw_winner(text):
    winner_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(winner_text, (WIDTH/2 - winner_text.get_width()/2, HEIGHT/2 - winner_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def handle_red(keys_pressed, red):
    if keys_pressed[pygame.K_w] and red.y - VEL > 0:  # Up
        red.y -= VEL
    if keys_pressed[pygame.K_a] and red.x - VEL > 0:  # Left
        red.x -= VEL
    if keys_pressed[pygame.K_s] and red.y + VEL < HEIGHT - SS_HEIGHT - 15:   # Down
        red.y += VEL
    if keys_pressed[pygame.K_d] and red.x + VEL < WIDTH/2 - 5 - SS_WIDTH:  # Right
        red.x += VEL


def handle_yellow(keys_pressed, yel):
    if keys_pressed[pygame.K_UP] and yel.y - VEL > 0:  # Up
        yel.y -= VEL
    if keys_pressed[pygame.K_LEFT] and yel.x - VEL > WIDTH/2 + 5:  # Left
        yel.x -= VEL
    if keys_pressed[pygame.K_DOWN] and yel.y + VEL < HEIGHT - SS_HEIGHT - 15:  # Down
        yel.y += VEL
    if keys_pressed[pygame.K_RIGHT] and yel.x + VEL < WIDTH - SS_WIDTH:  # Right
        yel.x += VEL


def handle_bullets(red, yel, red_bullets, yel_bullets):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if yel.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YEL_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)
    for bullet in yel_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yel_bullets.remove(bullet)
        elif bullet.x < 0:
            yel_bullets.remove(bullet)

def main():
    red = pygame.Rect(100, 205, SS_WIDTH, SS_HEIGHT)
    yel = pygame.Rect(760, 205, SS_WIDTH, SS_HEIGHT)
    red_health, yel_health = 10, 10
    red_bullets, yel_bullets = [], []


    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < BULLET_CD:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLETS_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(yel_bullets) < BULLET_CD:
                    bullet = pygame.Rect(yel.x - yel.width, yel.y + yel.height//2 - 2, 10, 5)
                    yel_bullets.append(bullet)
                    BULLETS_FIRE_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLETS_HIT_SOUND.play()
            if event.type == YEL_HIT:
                yel_health -= 1
                BULLETS_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "YELLOW WINS!!!"
        if yel_health <= 0:
            winner_text = "RED WINS!!!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_red(keys_pressed, red)
        handle_yellow(keys_pressed, yel)
        handle_bullets(red, yel, red_bullets, yel_bullets)
        draw_window(red, yel, red_bullets, yel_bullets, red_health, yel_health)
    main()


if __name__ == '__main__':
    main()
