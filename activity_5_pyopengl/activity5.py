"""
Activity 5: Hardware Graphics Pipeline & Shading using PyOpenGL
Features:
- Pygame OpenGL double-buffered context
- gluPerspective
- GL_DEPTH_TEST
- colored cube with GL_QUADS
- glPushMatrix/glPopMatrix hierarchy
- continuous rotation
- alpha blending
"""

import sys
import pygame
from pygame.locals import DOUBLEBUF, OPENGL, QUIT, KEYDOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption("Activity 5 - Hardware Graphics Pipeline")

gluPerspective(45, display[0] / display[1], 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

glEnable(GL_DEPTH_TEST)

vertices = [
    ( 1,-1,-1), ( 1, 1,-1), (-1, 1,-1), (-1,-1,-1),
    ( 1,-1, 1), ( 1, 1, 1), (-1,-1, 1), (-1, 1, 1)
]

colors = [
    (1,0,0), (0,1,0), (0,0,1), (1,1,0),
    (1,0,1), (0,1,1), (1,1,1), (0.5,0.5,0.5)
]

surfaces = [
    (0,1,2,3), (3,2,7,6), (6,7,5,4),
    (4,5,1,0), (1,5,7,2), (4,0,3,6)
]

def draw_colored_cube(alpha=1.0):
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex_idx in surface:
            r,g,b = colors[vertex_idx]
            glColor4f(r, g, b, alpha)
            glVertex3fv(vertices[vertex_idx])
    glEnd()

clock = pygame.time.Clock()
angle_x = angle_y = 0.0
transparent = False
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_LEFT:
                angle_y -= 5
            elif event.key == K_RIGHT:
                angle_y += 5
            elif event.key == K_UP:
                angle_x -= 5
            elif event.key == K_DOWN:
                angle_x += 5
            elif event.key == K_SPACE:
                transparent = not transparent

    # Clear both required buffers every frame.
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if transparent:
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        alpha = 0.45
    else:
        glDisable(GL_BLEND)
        alpha = 1.0

    glPushMatrix()
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)
    draw_colored_cube(alpha)
    glPopMatrix()

    pygame.display.flip()

pygame.quit()
sys.exit()
