"""
Activity 1: 2D Animation Principles & Kinematics Engine
Based on the supplied laboratory manual.

Features:
- Linear tweening with LERP
- Triangle-to-quadrilateral morphing using equal vertex correspondence
- Bouncing ball using Euler integration + restitution
- Keys 1/2/3 switch modes
"""

import math
import sys
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Activity 1 - Tweening, Morphing & Dynamics")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
small = pygame.font.Font(None, 24)

WHITE = (245, 245, 245)
BLUE = (60, 130, 230)
GREEN = (80, 190, 120)
RED = (225, 80, 80)
YELLOW = (245, 205, 60)
BG = (28, 32, 42)

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_point(p1, p2, t):
    return (lerp(p1[0], p2[0], t), lerp(p1[1], p2[1], t))

def ease_in_out(t):
    # Smoothstep ease-in/ease-out.
    return t * t * (3 - 2 * t)

# Equal-count polygon correspondence.
# The original triangle has been subdivided so both keyframes use 4 vertices.
poly_start = [
    (180, 130),
    (250, 230),
    (320, 330),
    (120, 330)
]
poly_end = [
    (160, 120),
    (360, 160),
    (320, 340),
    (120, 300)
]

def morph_polygon(t):
    return [lerp_point(a, b, t) for a, b in zip(poly_start, poly_end)]

mode = 1
elapsed = 0.0

ball_x, ball_y = 600.0, 100.0
ball_vx, ball_vy = 2.0, 0.0
gravity = 0.5
restitution = 0.78
floor_y = 500

running = True
while running:
    dt = clock.tick(60) / 1000.0
    elapsed += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_1:
                mode = 1
            elif event.key == pygame.K_2:
                mode = 2
            elif event.key == pygame.K_3:
                mode = 3

    screen.fill(BG)

    if mode == 1:
        # Multi-point path tweening.
        points = [(100, 450), (250, 180), (450, 400), (680, 180)]
        segment_duration = 1.4
        total = segment_duration * (len(points) - 1)
        t_total = elapsed % total
        seg = min(int(t_total / segment_duration), len(points) - 2)
        local_t = (t_total - seg * segment_duration) / segment_duration
        smooth_t = ease_in_out(local_t)
        pos = lerp_point(points[seg], points[seg + 1], smooth_t)

        pygame.draw.lines(screen, (100, 105, 125), False, points, 3)
        for p in points:
            pygame.draw.circle(screen, WHITE, p, 7)

        pygame.draw.circle(screen, BLUE, (int(pos[0]), int(pos[1])), 22)
        title = "1 — Linear Tweening / Ease-In-Out"

    elif mode == 2:
        t = (math.sin(elapsed * 1.5) + 1) / 2
        poly = morph_polygon(t)
        pygame.draw.polygon(screen, GREEN, poly)
        pygame.draw.polygon(screen, WHITE, poly, 3)
        for p in poly:
            pygame.draw.circle(screen, YELLOW, (int(p[0]), int(p[1])), 5)
        title = "2 — Triangle-to-Quadrilateral Morph"

    else:
        # Euler integration.
        ball_y += ball_vy
        ball_x += ball_vx
        ball_vy += gravity

        if ball_y >= floor_y:
            ball_y = floor_y
            ball_vy = -ball_vy * restitution

        if ball_x < 30 or ball_x > WIDTH - 30:
            ball_vx *= -1

        pygame.draw.line(screen, WHITE, (40, floor_y + 25), (760, floor_y + 25), 3)
        pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), 25)
        title = "3 — Bouncing Dynamics"

    screen.blit(font.render(title, True, WHITE), (20, 20))
    screen.blit(small.render("Keys: 1 Tweening   2 Morphing   3 Dynamics   ESC Quit", True, WHITE), (20, 55))
    pygame.display.flip()

pygame.quit()
sys.exit()
