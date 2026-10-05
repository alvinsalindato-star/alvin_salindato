"""
Activity 3: 3D Coordinate Geometry & Bounding Volumes
Includes:
- Point3D distance
- vector subtraction, dot and cross products
- Sphere3D
- AABB
- 100-object broad-phase stress test
"""

import math
import random
import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Activity 3 - 3D Geometry & Bounding Volumes")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

class Point3D:
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = x, y, z

    def __sub__(self, other):
        return Point3D(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Point3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def distance_to(self, other):
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )

    def __repr__(self):
        return f"Point3D({self.x}, {self.y}, {self.z})"

class Sphere3D:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def contains_point(self, p):
        return self.center.distance_to(p) <= self.radius

    def intersects_sphere(self, other):
        # Squared-distance test avoids sqrt in collision testing.
        dx = self.center.x - other.center.x
        dy = self.center.y - other.center.y
        dz = self.center.z - other.center.z
        dist_sq = dx*dx + dy*dy + dz*dz
        return dist_sq <= (self.radius + other.radius) ** 2

class AABB:
    def __init__(self, min_pt, max_pt):
        self.min_pt = min_pt
        self.max_pt = max_pt

    def intersects(self, other):
        return (
            self.min_pt.x <= other.max_pt.x and
            self.max_pt.x >= other.min_pt.x and
            self.min_pt.y <= other.max_pt.y and
            self.max_pt.y >= other.min_pt.y and
            self.min_pt.z <= other.max_pt.z and
            self.max_pt.z >= other.min_pt.z
        )

def example_verification():
    p = Point3D(2, -1, 7)
    q = Point3D(1, -3, 5)
    print("Example 3 distance:", p.distance_to(q))  # 3.0

    # x²+y²+z²+4x-6y+2z+6=0
    # => (x+2)²+(y-3)²+(z+1)²=8
    center = Point3D(-2, 3, -1)
    radius = math.sqrt(8)
    print("Example 5 center:", center)
    print("Example 5 radius:", radius)

def stress_test(n=100):
    spheres = []
    boxes = []

    for _ in range(n):
        x, y, z = [random.uniform(-100, 100) for _ in range(3)]
        r = random.uniform(2, 10)
        center = Point3D(x, y, z)
        spheres.append(Sphere3D(center, r))
        boxes.append(AABB(
            Point3D(x-r, y-r, z-r),
            Point3D(x+r, y+r, z+r)
        ))

    sphere_hits = 0
    aabb_hits = 0
    for i in range(n):
        for j in range(i + 1, n):
            if spheres[i].intersects_sphere(spheres[j]):
                sphere_hits += 1
            if boxes[i].intersects(boxes[j]):
                aabb_hits += 1

    return sphere_hits, aabb_hits

example_verification()
sphere_hits, aabb_hits = stress_test()

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                sphere_hits, aabb_hits = stress_test()

    screen.fill((25, 29, 40))
    lines = [
        "Activity 3 — 3D Coordinate Geometry",
        "Example 3: distance P(2,-1,7) to Q(1,-3,5) = 3.0",
        "Example 5: center = (-2,3,-1), radius = sqrt(8) = 2.828",
        f"100-object broad phase: sphere hits = {sphere_hits}",
        f"100-object broad phase: AABB hits = {aabb_hits}",
        "Press R to rerun the 100-object test. ESC to quit."
    ]

    for i, line in enumerate(lines):
        screen.blit(font.render(line, True, (240,240,240)), (30, 40+i*55))

    pygame.display.flip()

pygame.quit()
sys.exit()
