import cv2
from random import randint
import numpy as np
import math

points = []
triangles = []
WIN_WIDTH = 800
WIN_HEIGHT = 800
RANDOMNESS = 10
GAP = 20

def generate_points():
    odd_row = False
    for y in range(0, img_height + GAP * 2, GAP):
        points.append([])
        if not odd_row:
            for x in range(-GAP, img_width + GAP, GAP):
                points[y // GAP].append((x, y))
            odd_row = True
        else:
            for x in range(-GAP // 2, img_width + GAP, GAP):
                points[y // GAP].append((x, y))
            odd_row = False

def create_triangles():
    for i in range(len(points) - 1):
        if i % 2 == 0:
            for j in range(len(points[i]) - 1):
                triangles.append([points[i][j], points[i][j + 1], points[i + 1][j]])
                if i > 0:
                    triangles.append([points[i][j], points[i][j + 1], points[i - 1][j]])

        else:
            for j in range(len(points[i]) - 1):
                triangles.append([points[i - 1][j + 1], points[i][j], points[i][j + 1]])
                triangles.append([points[i][j], points[i][j + 1], points[i + 1][j + 1]])

def move_points():
    for i in range(len(points)):
        for j in range(len(points[i])):
            if points[i][j][0] < img_width - GAP and points[i][j][0] > 0 + GAP and points[i][j][1] < img_height - GAP and points[i][j][1] > 0:
                points[i][j] = tuple((points[i][j][0] + int(randint(-RANDOMNESS, RANDOMNESS)), points[i][j][1] + int(randint(-RANDOMNESS, RANDOMNESS))))

def triangle_center(triangle):
    return ((triangle[0][0] + triangle[1][0] + triangle[2][0]) // 3, (triangle[0][1] + triangle[1][1] + triangle[2][1]) // 3)

def in_image(point):
    return point[0] < img_width and point[0] > 0 and point[1] < img_height and point[0] > 0

def get_center(triangle):
    for attempt in range(100):
        center = triangle_center(triangle)
        if not in_image(center):
            for point in triangle:
                if in_image(point):
                    return point
                else:
                    continue
        else:
            return center
    return None

def main():
    global points, img_width, img_height
    img = cv2.imread('../images/cat.jpg')
    img_height, img_width, channels = img.shape
    canvas = np.zeros((img_height, img_width, 3), dtype='uint8')

    generate_points()
    move_points()
    create_triangles()

    for triangle in triangles:
        center = get_center(triangle)
        if center is None:
            continue
        color = tuple(map(int, img[center[1]][center[0]])) 
        cv2.fillPoly(canvas, np.array([triangle]), color)

    # for row in points:
        # for point in row:
            # cv2.circle(canvas, point, 2, (255, 255, 255), -1)

    while True:
        cv2.imshow('Triangular mesh', canvas)
        if cv2.waitKey(1) == 27:
            break

main()
cv2.destroyAllWindows()
