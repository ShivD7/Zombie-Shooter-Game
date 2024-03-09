#ENHANCEMENTS
'''
Include nice-looking graphics (png files are good for this) (0.5)
Use a custom pygame program icon (not the snake) (0.5)
Use lists to help make your program (0.5)
Use functions to help make your program (0.5)
Include sound (music / sfx) (1)
Use a timer (1)
'''
import pygame
import sys
import random
from pygame import mixer

pygame.init()
mixer.init()
mixer.music.load('song.mp3')


programIcon = pygame.image.load('zombie.png')
pygame.display.set_icon(programIcon)

WIDTH, HEIGHT = 800, 500
PLAYER_SPEED = 5
BULLET_SPEED = 7
ZOMBIE_SPEED = 2
ZOMBIE_SPAWN_DELAY = 60
WHITE = (255, 255, 255)
PLAYER_HEALTH = 50
ZOMBIE_HEALTH = 100
SCORE = 0
game_state = "start"

frame_count = 0
frame_rate = 60
start_time = -1

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie shooter game")

background = pygame.image.load("background.webp")
background = pygame.transform.scale(background, [800, 500])
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, [78, 123])
zombie_image = pygame.image.load("zombie.png")
zombie_image = pygame.transform.scale(zombie_image, [76, 124])

player = pygame.Rect(WIDTH//2 - 50, HEIGHT - 100, 100, 100)

bullets = []
zombies = []

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

running = True
player_health = PLAYER_HEALTH

def collisionDetection():
    global SCORE
    global player_health
    for bullet in bullets:
        for zombie in zombies:
            if bullet.colliderect(zombie):
                bullets.remove(bullet)
                zombies.remove(zombie)
                SCORE += 10
    
    for zombie in zombies:
        if zombie.colliderect(player):
            player_health -= 10
            zombies.remove(zombie) 
mixer.music.play()
while running:
    if game_state != "start":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(player.centerx-5, player.top, 10, 20)
                    bullets.append(bullet)
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player.x += PLAYER_SPEED

        for bullet in bullets:
            bullet.y -= BULLET_SPEED
            if bullet.y < 0:
                bullets.remove(bullet)
        
        if random.randint(0, ZOMBIE_SPAWN_DELAY) == 0:
            zombie = pygame.Rect(random.randint(0, WIDTH-100),0,100,10)
            zombies.append(zombie)
        
        for zombie in zombies:
            zombie.y += ZOMBIE_SPEED
            if zombie.y > HEIGHT:
                zombies.remove(zombie)
        
        collisionDetection() 
            
        screen.fill(WHITE)
        screen.blit(background, (0,0))

        screen.blit(player_image, player)
        for zombie in zombies:
            screen.blit(zombie_image, zombie)
        
        for bullet in bullets:
            pygame.draw.rect(screen, (255,0,0), bullet)
        
        total_seconds = frame_count // frame_rate
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        total_seconds += 1
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        frame_count += 1  
        
        time_text = "Time played: {0:02}:{1:02}".format(minutes, seconds)
        time_text = font.render(time_text, True, WHITE)
        health_text = font.render(f"Health: {player_health}", True, (255,0,0))
        score_text = font.render(f"Score: {SCORE}", True, (0,0,255))
        screen.blit(health_text, (10,10))
        screen.blit(score_text, (10,50))
        screen.blit(time_text,(10, 90))


        if player_health <= 0:
            running = False
        
        pygame.display.flip()
        clock.tick(60)
    else:
        screen.blit(background, (0,0))
        starting_text = "Zombie Shooter"
        starting_text2 = "CLICK TO PLAY!"
        screen.blit(zombie_image, (192, 205))
        screen.blit(zombie_image, (492, 205))
        starting_text = font.render(starting_text, True, WHITE)
        starting_text2 = font.render(starting_text2, True, WHITE)
        screen.blit(starting_text, (WIDTH//2-109, HEIGHT//2 - 20))
        screen.blit(starting_text2, (WIDTH//2-109, HEIGHT//2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game_state = "playing"
        pygame.display.flip()


if game_state != "start":
    game_over_text = font.render(f"Game OVER ! Score: {SCORE}", True, (0, 255, 0) )
    screen.blit(game_over_text, (WIDTH//2-137, HEIGHT//2 - 20))
    pygame.display.flip()
                




pygame.time.delay(1000)
pygame.quit()
sys.exit()