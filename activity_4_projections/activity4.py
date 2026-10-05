"""
Activity 4: 3D Projection Engine
Projection modes:
1 Orthographic
2 Cavalier Oblique
3 Cabinet Oblique
4 One-Point Perspective

Important: the supplied manual's theory specifies 45° Cavalier and
63.4° Cabinet. This implementation follows those stated angles.
"""

import math
import sys
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Activity 4 - 3D Projection Engine")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

cube_vertices = [
    [-100, -100, -100], [100, -100, -100],
    [100, 100, -100], [-100, 100, -100],
    [-100, -100, 100], [100, -100, 100],
    [100, 100, 100], [-100, 100, 100]
]

cube_edges = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

def rotate_xyz(v, rx, ry, rz):
    x, y, z = v

    # X rotation
    cx, sx = math.cos(rx), math.sin(rx)
    y, z = y*cx - z*sx, y*sx + z*cx

    # Y rotation
    cy, sy = math.cos(ry), math.sin(ry)
    x, z = x*cy + z*sy, -x*sy + z*cy

    # Z rotation
    cz, sz = math.cos(rz), math.sin(rz)
    x, y = x*cz - y*sz, x*sz + y*cz

    return x, y, z

def project_orthographic(x, y, z):
    return int(x + 400), int(y + 300)

def project_oblique(x, y, z, mode):
    if mode == "cavalier":
        L1 = 1.0
        phi_deg = 45.0
    else:
        L1 = 0.5
        phi_deg = 63.4

    phi = math.radians(phi_deg)
    xp = x + z * L1 * math.cos(phi)
    yp = y + z * L1 * math.sin(phi)
    return int(xp + 400), int(yp + 300)

def project_perspective(x, y, z, D=400):
    distance = z + D
    if abs(distance) < 0.001:
        distance = 0.001
    xp = (x * D) / distance
    yp = (y * D) / distance
    return int(xp + 400), int(yp + 300)

mode = 1
rx = ry = rz = 0.0

names = {
    1: "Orthographic",
    2: "Cavalier Oblique",
    3: "Cabinet Oblique",
    4: "One-Point Perspective"
}

running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                mode = int(event.unicode)
            elif event.key == pygame.K_x:
                rx += math.radians(10)
            elif event.key == pygame.K_y:
                ry += math.radians(10)
            elif event.key == pygame.K_z:
                rz += math.radians(10)

    # Continuous gentle rotation.
    ry += dt * 0.6

    projected = []
    for v in cube_vertices:
        x, y, z = rotate_xyz(v, rx, ry, rz)

        if mode == 1:
            p = project_orthographic(x, y, z)
        elif mode == 2:
            p = project_oblique(x, y, z, "cavalier")
        elif mode == 3:
            p = project_oblique(x, y, z, "cabinet")
        else:
            p = project_perspective(x, y, z)

        projected.append(p)

    screen.fill((25, 29, 40))

    for a, b in cube_edges:
        pygame.draw.line(screen, (220, 230, 245), projected[a], projected[b], 3)

    for p in projected:
        pygame.draw.circle(screen, (245, 190, 60), p, 5)

    title = font.render(
        f"Mode {mode}: {names[mode]}",
        True, (245,245,245)
    )
    controls = font.render(
        "1-4 Switch Projection | X/Y/Z Rotate | ESC Quit",
        True, (220,220,220)
    )

    screen.blit(title, (20, 20))
    screen.blit(controls, (20, 52))
    pygame.display.flip()

pygame.quit()
sys.exit()
