# script for lane tracking in GTA SA

import cv2 as cv
import utilis
from time import time, sleep
from window_capture import CaptureWindow

GAME_NAME = 'GTA: San Andreas'
game_screen = CaptureWindow(GAME_NAME)

# count to 4 before launch algorithm
for i in list(range(4)):
    print(i+1)
    sleep(1)


def main():
    while True:
        # loop_time = time()
        img = game_screen.capture()
        output_img, lines = utilis.process_img(img)
        utilis.steering_vehicle(output_img, lines)
        # print('FPS:{}'.format(1 / (time() - loop_time)))

        cv.imshow('Output', output_img)
        if cv.waitKey(1) == 27:
            break

    cv.destroyAllWindows()


main()