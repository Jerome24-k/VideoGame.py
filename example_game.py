import pygame
import random
import sys
import time
import os
import platform

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
ENEMY_SIZE = 50
PLAYER_SPEED = 7
ENEMY_SPEED = 5
MAX_ENEMY_SPEED = 40

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)

# Initial player position
PLAYER_POS = [WIDTH // 2, HEIGHT - 2 * PLAYER_SIZE]

# Score and block tracking
score = 0
blocks_passed = 0

# Font setup
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Game elements
screen = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

# Enemy list
enemy_list = []

# Timers
speed_increase_time = time.time()

# Function to play collision sound
def play_collision_sound():
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 500)  # Frequency 1000 Hz for 500 ms
    else:
        os.system('echo -e "\a"')  # System beep for Linux/Mac

# Function to drop enemies
def drop_enemies():
    if len(enemy_list) < min(10 + score // 20, 30):
        enemy_list.append([random.randint(0, WIDTH - ENEMY_SIZE), 0])

# Function to draw enemies
def draw_enemies():
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], ENEMY_SIZE, ENEMY_SIZE))

# Collision detection
def detect_collision(PLAYER_POS, ENEMY_POS):
    p_x, p_y = PLAYER_POS
    e_x, e_y = ENEMY_POS
    return (e_x < p_x + PLAYER_SIZE and e_x + ENEMY_SIZE > p_x and
            e_y < p_y + PLAYER_SIZE and e_y + ENEMY_SIZE > p_y)

# Main game loop
def main_game_loop():
    global score, blocks_passed, ENEMY_SPEED, speed_increase_time, enemy_list

    moving_left = False
    moving_right = False
    game_over = False

    while not game_over:
        screen.fill(BACKGROUND_COLOR)

        # Increase enemy speed over time
        if time.time() - speed_increase_time >= 7:
            ENEMY_SPEED = min(MAX_ENEMY_SPEED, ENEMY_SPEED + 0.3)
            speed_increase_time = time.time()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moving_left = True
                elif event.key == pygame.K_RIGHT:
                    moving_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    moving_left = False
                elif event.key == pygame.K_RIGHT:
                    moving_right = False

        # Move player
        if moving_left:
            PLAYER_POS[0] = max(0, PLAYER_POS[0] - PLAYER_SPEED)
        if moving_right:
            PLAYER_POS[0] = min(WIDTH - PLAYER_SIZE, PLAYER_POS[0] + PLAYER_SPEED)

        # Drop and update enemies
        drop_enemies()

        new_enemy_list = []
        for enemy in enemy_list:
            enemy[1] += ENEMY_SPEED
            if enemy[1] < HEIGHT:
                new_enemy_list.append(enemy)
            else:
                blocks_passed += 1
                score += 1
                if score == 100:
                    print("DAMN A 100 DOWN!!")
        enemy_list = new_enemy_list

        draw_enemies()

        # Check for collision
        for enemy in enemy_list:
            if detect_collision(PLAYER_POS, enemy):
                play_collision_sound()  # ✅ Play beep sound on collision
                screen.fill(BACKGROUND_COLOR)
                game_over_text = big_font.render("TOUGH LUCK", True, WHITE)
                screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
                passed_text = font.render(f"Blocks Passed: {blocks_passed}", True, WHITE)
                screen.blit(passed_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
                pygame.display.update()
                time.sleep(2)
                pygame.quit()
                sys.exit()

        # Draw player
        pygame.draw.rect(screen, RED, (PLAYER_POS[0], PLAYER_POS[1], PLAYER_SIZE, PLAYER_SIZE))
 
        # Display score and speed
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        speed_text = font.render(f"Speed: {round(ENEMY_SPEED, 1)}", True, WHITE)
        screen.blit(speed_text, (10, 40))

        pygame.display.update()
        CLOCK.tick(30)

main_game_loop()

