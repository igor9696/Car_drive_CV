# script for lane tracking in GTA SA

import cv2 as cv
import numpy as np
import utilis
from time import time, sleep
from window_capture import CaptureWindow
from game_control import press_key, release_key, W, A, S, D
import pydirectinput


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

game_screen = CaptureWindow('GTA: San Andreas')

# img = game_screen.capture()
# res = utilis.process_img(img)
# cv.imshow('Result', res)
# cv.waitKey(0)
# cv.destroyAllWindows()


def main():
    while True:
        loop_time = time()
        img = game_screen.capture()
        res = utilis.process_img(img)
        print('FPS:{}'.format(1 / (time() - loop_time)))

        cv.imshow('Result', res)
        if cv.waitKey(1) == 27:
            break
    cv.destroyAllWindows()

main()