import cv2
import numpy as np

def myround(x, base=255):
    return base * round(x/base)

# PIXEL COLOR AVERAGE IN A GIVEN SIZE
def avg(image, x, y):
    return (int(image[y][x]) + int(image[y][x + 3]) + int(image[y + 3][x]) + int(image[y + 3][x + 3])) // 4

# GET THE AVERAGE COLOR (EITHER 0 or 255) 
def break_into_sections(image, lst):
    for y in range(0, len(image) - 1, 25):
        lst.append([])
        for x in range(0, len(image[y]) - 1, 25):
            lst[-1].append(myround(avg(image, x, y)))

def main(DRAW=False):
    sections = []

    image = cv2.imread('../images/cat.jpg', 0)
    # image = cv2.addWeighted(image, .5, np.zeros(image.shape, image.dtype), .5, 0)
    image_height, image_width = image.shape
    break_into_sections(image, sections)

    # DRAW
    if DRAW:
        canvas = np.zeros((image_height, image_width))
        for y in range(0, len(sections) - 1, 1):
            for x in range(0, len(sections[y]) - 1, 1):
                pt1 = (x * 25, y * 25)
                pt2 = (x * 25 + 25, y  * 25 + 25)
                color = sections[y][x]
                if color == 0:
                    cv2.rectangle(canvas, pt1, pt2, (255, 255, 255))
                else:
                    cv2.rectangle(canvas, pt1, pt2, color, -1)

        while True:
            cv2.imshow('Canvas', canvas)
            if cv2.waitKey(1) == 27:
                break

        cv2.destroyAllWindows()

    return sections

if __name__ == '__main__':
    main(DRAW=True)