# script for lane tracking in GTA SA

import cv2 as cv
import numpy as np
import os
from time import time, sleep
from window_capture import CaptureWindow
from game_control import press_key, release_key, W, A, S, D
import pydirectinput


def draw_lines(image, lines):
    if lines is not None:
        for i in range(0, len(lines)):
            line = lines[i][0]
            cv.line(image, (line[0], line[1]), (line[2], line[3]), (0, 0, 255), 3, cv.LINE_AA)
    return image


def roi(image, vertices):
    mask = np.zeros_like(image)
    cv.fillPoly(mask, vertices, [255,255,255])
    roi_img = cv.bitwise_and(image, mask)
    return roi_img


def process_img(src_img):
    vertices = np.array([[150, 300], [650, 300], [800, 800], [0, 800]])
    roi_img = roi(src_img, [vertices])
    gray = cv.cvtColor(roi_img, cv.COLOR_BGR2GRAY)
    blur = cv.blur(gray, (3, 3))
    canny = cv.Canny(blur, 50, 130)
    lines = cv.HoughLinesP(canny, 1, np.pi/180, 100, minLineLength=120, maxLineGap=5)
    draw_lines(src_img, lines)
    return src_img


game_screen = CaptureWindow('GTA: San Andreas')
# # count to 4
# for i in list(range(4)):
#     print(i+1)
#     sleep(1)

# print('press W')
# pydirectinput.keyDown('w')
# sleep(2)
# pydirectinput.keyUp('w')
# print('press S')
# pydirectinput.keyDown('s')
# sleep(2)
# pydirectinput.keyUp('s')


def main():
    while True:
        loop_time = time()
        img = game_screen.capture()
        res = process_img(img)
        print('FPS:{}'.format(1 / (time() - loop_time)))

        cv.imshow('Result', res)
        if cv.waitKey(1) == 27:
            break
    cv.destroyAllWindows()


main()