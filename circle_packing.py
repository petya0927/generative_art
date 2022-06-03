##################################################################

# Rules: 
# Create a new Circle
# Check to see if the circle collides with any other circles we have.
# If it doesn’t collide, we will grow it slightly, and then check again if it collides.
# Repeat these steps until we have a collision, or we reach a “max size”
# Create another circle and repeat x times.

##################################################################

import cv2
import numpy as np
from random import randint
import math

circles = []
WIN_WIDTH = 800
WIN_HEIGHT = 800
MIN_RADIUS = 10
MAX_RADIUS = 400
MAX_ENTITIES = 200
ATTEMPTS = 100

class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

def distance(circle1, circle2):
    return math.sqrt(math.pow(circle1.x - circle2.x, 2) + math.pow(circle1.y - circle2.y, 2))

def is_colliding(circle):
    for other_circle in circles:
        if distance(circle, other_circle) <= circle.r + other_circle.r:
            return True

    if circle.x + circle.r >= WIN_WIDTH or circle.x - circle.r <= 0:
        return True
    
    if circle.y + circle.r >= WIN_HEIGHT or circle.y - circle.r <= 0:
        return True

    return False

def compute_new_circle():
    safe = False

    for attempt in range(ATTEMPTS):
        new_circle = Circle(randint(0, WIN_WIDTH), randint(0, WIN_HEIGHT), MIN_RADIUS)

        if is_colliding(new_circle):
            continue
        else:
            safe = True
            break

    if not safe:
        return

    while new_circle.r < MAX_RADIUS:
        new_circle.r += 1
        if is_colliding(new_circle):
            new_circle.r -= 1
            break

    circles.append(new_circle)

def main():
    canvas = np.ones((WIN_WIDTH, WIN_HEIGHT), dtype='uint8')
    while True:

        if len(circles) <= MAX_ENTITIES:
            compute_new_circle()

        for circle in circles:
            cv2.circle(canvas, (circle.x, circle.y), circle.r, (200, 200, 200), 1)

        cv2.imshow('Canvas', canvas)
        if cv2.waitKey(1) == 27:
            break

main()
cv2.destroyAllWindows()
