import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('3D Cube Game')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Cube vertices (3D coordinates)
vertices = [
    [1, 1, -1],  # Front top right
    [1, -1, -1], # Front bottom right
    [-1, -1, -1],# Front bottom left
    [-1, 1, -1], # Front top left
    [1, 1, 1],   # Back top right
    [1, -1, 1],  # Back bottom right
    [-1, -1, 1], # Back bottom left
    [-1, 1, 1],  # Back top left
]

# Define edges that connect the vertices
edges = [
    [0, 1], [1, 2], [2, 3], [3, 0],  # Front face
    [4, 5], [5, 6], [6, 7], [7, 4],  # Back face
    [0, 4], [1, 5], [2, 6], [3, 7]   # Connecting front and back faces
]

# Function to project 3D coordinates to 2D space
def project_3d_to_2d(x, y, z, width, height, fov=256, viewer_distance=4):
    factor = fov / (viewer_distance + z)
    x_2d = int(x * factor + width // 2)
    y_2d = int(-y * factor + height // 2)
    return x_2d, y_2d

# Player settings
player_pos = [0, 0, 2]  # Starting position (z is positive to be in front of the cube)
player_speed = 0.1

# Game settings
angle = 0
game_over = False
clock = pygame.time.Clock()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Handle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] += player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] -= player_speed

    # Rotate the cube around the Y-axis
    rotated_vertices = []
    for vertex in vertices:
        # Rotate around Y-axis
        x = vertex[0] * math.cos(angle) - vertex[2] * math.sin(angle)
        z = vertex[0] * math.sin(angle) + vertex[2] * math.cos(angle)
        y = vertex[1]
        rotated_vertices.append([x, y, z])

    # Project 3D vertices to 2D
    projected_vertices = []
    for vertex in rotated_vertices:
        projected_vertices.append(project_3d_to_2d(vertex[0], vertex[1], vertex[2], width, height))

    # Draw everything
    screen.fill(black)

    # Draw the cube
    for edge in edges:
        start, end = edge
        pygame.draw.line(screen, white, projected_vertices[start], projected_vertices[end], 2)

    # Draw the player (a small circle to represent the player in 2D)
    player_x, player_y = project_3d_to_2d(player_pos[0], player_pos[1], player_pos[2], width, height)
    pygame.draw.circle(screen, red, (player_x, player_y), 10)

    # Check for boundaries (player falling off the screen)
    if player_pos[0] > 2 or player_pos[0] < -2 or player_pos[1] > 2 or player_pos[1] < -2:
        game_over = True

    # Update the display
    pygame.display.flip()

    # Increase the angle to animate the rotation
    angle += 0.01

    # Set the game speed
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
