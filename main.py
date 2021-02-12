# script for autonomous driving in EuroTruckSimulator game

import cv2 as cv
import numpy as np
import os
import pyautogui
import win32gui
from PIL import ImageGrab


def grab_screen(window_title=None):
    """ Grab screen from window with specified title and return image as numpy array """
    if window_title:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            # get coordinates
            win32gui.SetForegroundWindow(hwnd)
            x, y, x2, y2 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            x2, y2 = win32gui.ClientToScreen(hwnd, (x2 - x, y2 - y))

            # grab and process image
            captured_img = ImageGrab.grab(bbox=(x, y, x2, y2))
            captured_img = np.array(captured_img)
            captured_img = cv.cvtColor(captured_img, cv.COLOR_RGB2BGR)
            return captured_img

    else:
        print('Window file not found!')


while True:
    img = grab_screen(window_title='Euro Truck Simulator 2')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    cv.imshow('Game window', gray)
    if cv.waitKey(5) & 0xFF == 27:
        break


cv.destroyAllWindows()