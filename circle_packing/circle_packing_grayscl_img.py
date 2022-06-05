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
MIN_RADIUS = 1
MAX_RADIUS = 50
MAX_ENTITIES = 500
ATTEMPTS = 100

class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

def distance(circle1, circle2):
    return math.sqrt(math.pow(circle1.x - circle2.x, 2) + math.pow(circle1.y - circle2.y, 2))

def myround(x, base=5):
    return base * round(x/base)

def is_colliding(circle):
    for other_circle in circles:
        if distance(circle, other_circle) <= circle.r + other_circle.r:
            return True

    if myround(img[circle.y - 1][circle.x - 1], 255) == 0:
        return True

    if circle.x + circle.r >= img_width or circle.x - circle.r <= 0:
        return True
    
    if circle.y + circle.r >= img_height or circle.y - circle.r <= 0:
        return True

    return False


def compute_new_circle():
    safe = False

    for attempt in range(ATTEMPTS):
        new_circle = Circle(randint(0, img_width), randint(0, img_height), MIN_RADIUS)

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
    global img, img_height, img_width
    img = cv2.imread('../images/2017.png', 0)
    img_height, img_width = img.shape
    canvas = np.zeros((img_height, img_width, 3), np.uint8)
    while True:

        if len(circles) <= MAX_ENTITIES:
            compute_new_circle()

        for circle in circles:
            cv2.circle(canvas, (circle.x, circle.y), circle.r, (200, 200, 200), 1)

        cv2.imshow('Circle packing', canvas)
        if cv2.waitKey(1) == 27:
            break

main()
cv2.destroyAllWindows()
