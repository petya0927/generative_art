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
MAX_RADIUS = 30
MAX_ENTITIES = 20000
ATTEMPTS = 100
OFFSET = 0

class Circle:
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

def distance(circle1, circle2):
    return math.sqrt(math.pow(circle1.x - circle2.x, 2) + math.pow(circle1.y - circle2.y, 2))

def is_colliding(circle):
    for other_circle in circles:
        if distance(circle, other_circle) <= circle.r + other_circle.r + OFFSET:
            return True

    if circle.x + circle.r >= img_width or circle.x - circle.r <= 0:
        return True
    
    if circle.y + circle.r >= img_height or circle.y - circle.r <= 0:
        return True

    return False


def compute_new_circle():
    safe = False

    for attempt in range(ATTEMPTS):
        x = randint(0, img_width)
        y = randint(0, img_height)
        color = (int(img[y - 1][x - 1][0]), int(img[y - 1][x - 1][1]), int(img[y - 1][x - 1][2]))
        new_circle = Circle(x, y, MIN_RADIUS, tuple(color))

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
    img = cv2.imread('../images/cat.jpg')
    img_height, img_width, channels = img.shape
    canvas = np.zeros((img_height, img_width, 3), np.uint8)
    while True:

        if len(circles) <= MAX_ENTITIES:
            compute_new_circle()

        for circle in circles:
            cv2.circle(canvas, (circle.x, circle.y), circle.r, circle.color, -1)

        cv2.imshow('Circle packing', canvas)
        if cv2.waitKey(1) == 27:
            break

main()
cv2.destroyAllWindows()
