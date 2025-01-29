import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Window settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Aim Trainer")

# Game variables
score = 0
target_radius = 30  # Radius of the target
targets = []  # List of targets
total_time = 0  # Total time spent hitting targets
hit_count = 0  # Number of targets hit
target_timer = 2  # Seconds before a target disappears if not hit
time_limit = 2  # Time after which target disappears
last_target_time = time.time()  # Keep track of the last target creation time

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Font for displaying score and average time
font = pygame.font.SysFont('Arial', 30)

# Function to draw the score
def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Function to draw the average time to hit a target
def draw_avg_time():
    if hit_count > 0:
        avg_time = total_time / hit_count
        avg_time_text = font.render(f"Avg Time: {avg_time:.2f}s", True, WHITE)
        screen.blit(avg_time_text, (width - 200, 10))

# Function to create a new target
def create_target():
    x = random.randint(target_radius, width - target_radius)
    y = random.randint(target_radius, height - target_radius)
    start_time = time.time()  # Start the timer for the target
    return (x, y, start_time)

# Function to draw the targets
def draw_targets():
    for target in targets:
        pygame.draw.circle(screen, RED, (target[0], target[1]), target_radius)

# Check if the mouse click hits any target
def check_hit(mouse_pos):
    global score, total_time, hit_count
    for target in targets:
        target_x, target_y, start_time = target
        distance = ((mouse_pos[0] - target_x) ** 2 + (mouse_pos[1] - target_y) ** 2) ** 0.5
        if distance <= target_radius:
            targets.remove(target)
            targets.append(create_target())  # Add new target at random location
            score += 1
            # Calculate time taken to hit the target
            time_taken = time.time() - start_time
            total_time += time_taken
            hit_count += 1
            break

# Function to draw the arrow pointing to the mouse position
def draw_arrow():
    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.line(screen, GREEN, (width // 2, height // 2), mouse_pos, 5)

# Function to remove expired targets (those that have been up for more than 2 seconds)
def remove_expired_targets():
    current_time = time.time()
    global targets
    # Remove expired targets
    targets = [target for target in targets if current_time - target[2] <= time_limit]

# Main game loop
running = True
targets.append(create_target())  # Create initial target
while running:
    screen.fill(BLACK)  # Fill the screen with black

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            check_hit(mouse_pos)  # Check if the click hits any target

    # Remove expired targets and create a new target if necessary
    remove_expired_targets()

    # Ensure a new target is created every 2 seconds
    if time.time() - last_target_time >= time_limit:
        targets.append(create_target())  # Add new target
        last_target_time = time.time()  # Update the last target creation time

    # Draw targets, arrow, score, and average time
    draw_targets()
    draw_arrow()
    draw_score()
    draw_avg_time()

    # Update the display
    pygame.display.flip()
    pygame.time.wait(16)  # To make it run at ~60 FPS

pygame.quit()
sys.exit()
