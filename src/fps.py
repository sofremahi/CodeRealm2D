import pygame
import sys
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Initialize Pygame
pygame.init()

# Window settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Shooting Game")

# Initialize OpenGL
glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (width / height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

# Cursor Fix
pygame.mouse.set_visible(True)

# Game Variables
bullets = []
enemy_position = [0, 0, -5]
player_x = 0

# Custom Cube Renderer
def draw_cube():
    vertices = [
        [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5],
        [0.5,  0.5, -0.5], [-0.5,  0.5, -0.5],
        [-0.5, -0.5,  0.5], [0.5, -0.5,  0.5],
        [0.5,  0.5,  0.5], [-0.5,  0.5,  0.5]
    ]
    edges = [
        (0,1), (1,2), (2,3), (3,0),
        (4,5), (5,6), (6,7), (7,4),
        (0,4), (1,5), (2,6), (3,7)
    ]
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Function to draw the enemy
def draw_enemy():
    glPushMatrix()
    glTranslatef(*enemy_position)
    glColor3f(1, 0, 0)
    draw_cube()  
    glPopMatrix()

# Function to draw bullets (Fixed Sphere)
def draw_bullets():
    global bullets
    new_bullets = []
    for bullet in bullets:
        bullet[2] -= 0.2  # Move bullet forward
        if bullet[2] > -10:
            new_bullets.append(bullet)
            glPushMatrix()
            glTranslatef(*bullet)
            glColor3f(1, 1, 0)
            quadric = gluNewQuadric()
            gluSphere(quadric, 0.1, 10, 10)  # Fixed
            glPopMatrix()
    bullets = new_bullets

# Main loop
running = True
while running:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(player_x, 0, 2, player_x, 0, -5, 0, 1, 0)  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:  # Shoot a bullet
                bullets.append([player_x, 0, 1])
            elif event.key == K_LEFT:
                player_x -= 0.2
            elif event.key == K_RIGHT:
                player_x += 0.2

    draw_enemy()
    draw_bullets()

    pygame.display.flip()
    pygame.time.wait(16)

pygame.quit()
