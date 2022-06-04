import cv2
from random import randint
import numpy as np
import math

points = []
triangles = []
WIN_WIDTH = 800
WIN_HEIGHT = 800
RANDOMNESS = 0
GAP = 20

def generate_points():
    odd_row = False
    for y in range(0, WIN_HEIGHT + 1, GAP):
        points.append([])
        if not odd_row:
            for x in range(0, WIN_WIDTH + 1, GAP):
                points[y // GAP].append((x, y))
            odd_row = True
        else:
            for x in range(GAP // 2, WIN_WIDTH + 1, GAP):
                points[y // GAP].append((x, y))
            odd_row = False

def create_triangles():
    for i in range(len(points) - 1):
        if i % 2 == 0:
            for j in range(len(points[i]) - 1):
                triangles.append([points[i][j], points[i][j + 1], points[i + 1][j]])
                if i > 0:
                    triangles.append([points[i][j], points[i][j + 1], points[i - 1][j]])
                if i == 0:
                    triangles.append([points[i - 1][j], points[i - 1][j + 1], points[i - 2][j]])

        else:
            for j in range(len(points[i]) - 1):
                triangles.append([points[i - 1][j + 1], points[i][j], points[i][j + 1]])
                triangles.append([points[i][j], points[i][j + 1], points[i + 1][j + 1]])

def move_points():
    for i in range(len(points)):
        for j in range(len(points[i])):
            points[i][j] = tuple((points[i][j][0] + int(randint(-RANDOMNESS, RANDOMNESS)), points[i][j][1] + int(randint(-RANDOMNESS, RANDOMNESS))))

def main():
    global points
    canvas = np.ones((WIN_WIDTH, WIN_HEIGHT, 3), dtype='uint8')
    canvas.fill(255)

    generate_points()
    move_points()
    create_triangles()

    # for row in points:
    #     for point in row:
    #         cv2.circle(canvas, point, 5, (0, 0, 0), -1)

    for triangle in triangles:
        cv2.fillPoly(canvas, np.array([triangle]), (randint(0, 255), randint(0, 255), randint(0, 255)))

    while True:
        cv2.imshow('Triangular mesh', canvas)
        if cv2.waitKey(1) == 27:
            break

main()
cv2.destroyAllWindows()