import pygame

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Paddle settings
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_VEL = 5

# Ball settings
BALL_WIDTH = 20
BALL_VEL_X = 5
BALL_VEL_Y = 5

# Initialize the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Font for score
font = pygame.font.SysFont('comicsans', 30)

# Player class for paddles
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0

    def update(self):
        # Update paddle position
        self.rect.y += self.vel_y

        # Prevent paddles from moving off-screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_WIDTH, BALL_WIDTH))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - BALL_WIDTH // 2
        self.rect.y = HEIGHT // 2 - BALL_WIDTH // 2
        self.vel_x = BALL_VEL_X
        self.vel_y = BALL_VEL_Y

    def update(self):
        # Move the ball
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Bounce the ball off top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vel_y = -self.vel_y

# Initialize paddles and ball
left_paddle = Paddle(30, HEIGHT // 2 - PADDLE_HEIGHT // 2)
right_paddle = Paddle(WIDTH - 50, HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball()

# Create sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(left_paddle, right_paddle, ball)

# Score variables
left_score = 0
right_score = 0

# Main game loop
running = True
while running:
    clock.tick(FPS)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                left_paddle.vel_y = -PADDLE_VEL
            if event.key == pygame.K_s:
                left_paddle.vel_y = PADDLE_VEL
            if event.key == pygame.K_UP:
                right_paddle.vel_y = -PADDLE_VEL
            if event.key == pygame.K_DOWN:
                right_paddle.vel_y = PADDLE_VEL
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                left_paddle.vel_y = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                right_paddle.vel_y = 0

    # Update all sprites
    all_sprites.update()

    # Ball collision with paddles
    if pygame.sprite.collide_rect(ball, left_paddle) or pygame.sprite.collide_rect(ball, right_paddle):
        ball.vel_x = -ball.vel_x

    # Ball out of bounds (score point)
    if ball.rect.left <= 0:
        right_score += 1
        ball.rect.x = WIDTH // 2 - BALL_WIDTH // 2
        ball.rect.y = HEIGHT // 2 - BALL_WIDTH // 2
        ball.vel_x = -ball.vel_x
    if ball.rect.right >= WIDTH:
        left_score += 1
        ball.rect.x = WIDTH // 2 - BALL_WIDTH // 2
        ball.rect.y = HEIGHT // 2 - BALL_WIDTH // 2
        ball.vel_x = -ball.vel_x

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Draw the score
    score_text = font.render(f"{left_score} - {right_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
