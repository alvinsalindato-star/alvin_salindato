"""
Activity 2: Interactive Game Architecture
Features:
- pygame.sprite.Sprite subclasses
- sprite.Group
- keyboard steering
- screen boundary clamping
- spritecollide collision detection
- score and health HUD
- translucent impact particles
"""

import random
import sys
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Activity 2 - Sprite Collision Arena")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (44, 94, 138), (20, 20), 20)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Strict boundary clamping.
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, HEIGHT)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((220, 50, 50))
        self.rect = self.image.get_rect(
            center=(random.randint(40, WIDTH - 40),
                    random.randint(40, HEIGHT - 40))
        )
        self.vx = random.choice([-2, -1, 1, 2])
        self.vy = random.choice([-2, -1, 1, 2])

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vy *= -1

class Particle:
    def __init__(self, x, y):
        self.x, self.y = float(x), float(y)
        self.life = 255
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 8

    def draw(self, target):
        if self.life <= 0:
            return
        surface = pygame.Surface((14, 14), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 210, 50, int(self.life)), (7, 7), 7)
        target.blit(surface, (int(self.x - 7), int(self.y - 7)))

player = Player()
obstacles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(player)

for _ in range(10):
    obj = Obstacle()
    obstacles.add(obj)
    all_sprites.add(obj)

particles = []
score = 0
health = 100

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Update game state.
    all_sprites.update()

    hits = pygame.sprite.spritecollide(player, obstacles, True)
    if hits:
        score += len(hits)
        health = max(health - 10 * len(hits), 0)
        for hit in hits:
            for _ in range(12):
                particles.append(Particle(hit.rect.centerx, hit.rect.centery))

        # Respawn destroyed obstacles.
        for _ in hits:
            obj = Obstacle()
            obstacles.add(obj)
            all_sprites.add(obj)

    for p in particles:
        p.update()
    particles = [p for p in particles if p.life > 0]

    # Render stage — drawing is intentionally kept outside update().
    screen.fill((24, 28, 38))
    all_sprites.draw(screen)

    for p in particles:
        p.draw(screen)

    hud = font.render(
        f"Score: {score}   Health: {health}   FPS: {clock.get_fps():.0f}",
        True, (245, 245, 245)
    )
    screen.blit(hud, (20, 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
