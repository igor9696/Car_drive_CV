# script for lane tracking in GTA SA

import cv2 as cv
import numpy as np
import os
from time import time
from window_capture import CaptureWindow


def process_img(src_img):
    gray = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)
    canny = cv.Canny(gray, 120, 200)
    return canny


game_screen = CaptureWindow('GTA: San Andreas')
while True:
    loop_time = time()
    img = game_screen.capture()
    res = process_img(img)
    print('FPS:{}'.format(1 / (time()-loop_time)))

    cv.imshow('Result', res)
    if cv.waitKey(1) == 27:
        break

cv.destroyAllWindows()

