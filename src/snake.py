import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Snake settings
snake_pos = [(100, 50)]  # The snake starts with one block
snake_body = [(100, 50)]  # The snake body is initially one block long
snake_speed = 10
snake_direction = "RIGHT"  # Snake's initial direction

# Food settings
food_pos = (random.randint(0, width // snake_speed - 1) * snake_speed, random.randint(0, height // snake_speed - 1) * snake_speed)
food_color = red

# Game over flag
game_over = False

# Initialize the clock for controlling game speed
clock = pygame.time.Clock()

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            # Prevent the snake from going in the opposite direction
            if event.key == pygame.K_UP and snake_direction != "DOWN":
                snake_direction = "UP"
            elif event.key == pygame.K_DOWN and snake_direction != "UP":
                snake_direction = "DOWN"
            elif event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                snake_direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                snake_direction = "RIGHT"

    # Move the snake
    if snake_direction == "UP":
        new_head = (snake_pos[0][0], snake_pos[0][1] - snake_speed)
    elif snake_direction == "DOWN":
        new_head = (snake_pos[0][0], snake_pos[0][1] + snake_speed)
    elif snake_direction == "LEFT":
        new_head = (snake_pos[0][0] - snake_speed, snake_pos[0][1])
    elif snake_direction == "RIGHT":
        new_head = (snake_pos[0][0] + snake_speed, snake_pos[0][1])

    snake_pos.insert(0, new_head)
    snake_body.insert(0, list(new_head))  # Add the new head to the body

    if snake_pos[0] == food_pos:
        # Food eaten, generate new food position
        food_pos = (random.randint(0, width // snake_speed - 1) * snake_speed, random.randint(0, height // snake_speed - 1) * snake_speed)
        # Ensure the food doesn't spawn on the snake
        while food_pos in snake_pos:
            food_pos = (random.randint(0, width // snake_speed - 1) * snake_speed, random.randint(0, height // snake_speed - 1) * snake_speed)
    else:
        # Remove the last segment of the snake body
        snake_body.pop()
        snake_pos.pop()

    # Check for collisions with boundaries
    if snake_pos[0][0] < 0 or snake_pos[0][0] >= width or snake_pos[0][1] < 0 or snake_pos[0][1] >= height:
        game_over = True

    # Check for collisions with itself
    if snake_pos[0] in snake_pos[1:]:
        game_over = True

    # Draw everything
    screen.fill(black)
    for pos in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], snake_speed, snake_speed))
    pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], snake_speed, snake_speed))

    # Update the display
    pygame.display.flip()

    # Set the speed of the game
    clock.tick(15)  # Adjust speed by changing this value

# Quit Pygame properly
pygame.quit()
