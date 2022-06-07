import pygame
from random import randint
import image_processing

WINDOW_WIDTH = 1305
WINDOW_HEIGHT = 768
START_SIZE = 800
TILE_SIZE = 50

def get_section(start_x, start_y):
    # print((start_x, start_y), (start_x, start_y + 1), (start_x + 1, start_y), (start_x + 1, start_y + 1))
    return [
        [sections[start_y][start_x], sections[start_y][start_x + 1]],
        [sections[start_y + 1][start_x], sections[start_y + 1][start_x + 1]]
    ]

# return (-1, -1) or (-1, 0) or (-1, 1) or (0, -1) or (0, 0) or (0, 1) or (1, -1) or (1, 0) or (1, 1)
# we have to return the steps
def get_direction(section):
    # if all(section[i][j] == 255 for i in range(len(section)) for j in range(len(section[i]))):
    #     return (0, 0), 1
    # elif all(i == 0 for i in section):
    #     return (0, 0), 5

    if not any(0 in i for i in section):
        return (0, 0), 1
    elif not any(255 in i for i in section):
        return (0, 0), 7
    else:
        offset_x = 0
        offset_y = 0
        for y in range(0, len(section)):
            for x in range(0, len(section[y])):
                if section[y][x] == 255:
                    if y < len(section) // 2:
                        offset_y += 1
                    else:
                        offset_y -= 1

                    if x < len(section[y]) // 2:
                        offset_x += 1
                    else:
                        offset_x -= 1

        if offset_x < -1: offset_x = -1
        elif offset_x > 1: offset_x = 1
        if offset_y < -1 : offset_y = -1
        elif offset_y > 1: offset_y = 1

        return (offset_x, offset_y), 7

def create_square(size, steps, start_x, start_y, direction):
    # direction1 = round(randint(-1, 1))
    # direction2 = round(randint(-1, 1))
    direction_x, direction_y = direction
    for i in range(0, size, size // steps // 2):
        rect = pygame.Rect(i + (i // 2) * direction_x + start_x, i + (i // 2) * direction_y + start_y, size - i * 2, size - i * 2)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1)
        

def main():
    global screen, sections

    sections = image_processing.main()
    running = True

    pygame.init()
    screen = pygame.display.set_mode(((len(sections[0]) - 1) * 25, (len(sections) - 1) * 25))
    screen.fill((255, 255, 255))

    for y in range(0, len(sections) // 2, 1):
        for x in range(0, len(sections[y]) // 2, 1):
            # print(sections[y][x])
            section = get_section(x * 2, y * 2)
            direction, steps = get_direction(section)
            create_square(50, steps, x * 50, y * 50, direction)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()