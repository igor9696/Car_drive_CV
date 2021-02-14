import numpy as np
import cv2 as cv
import win32gui
import mss


class CaptureWindow:
    def __init__(self, window_name):
        """Find coordinates of window_name"""
        self.hwnd = win32gui.FindWindow(None, window_name)
        self.left, self.top, self.right, self.bot = win32gui.GetWindowRect(self.hwnd)
        self.width = self.right - self.left
        self.height = self.bot - self.top

    def capture(self):
        with mss.mss() as sct:
            # Part of the screen to capture
            # monitor = {'top': 40, 'left': 0, 'width': 800, 'height': 640}
            monitor = {'top': self.top, 'left': self.left, 'width': self.width, 'height': self.height}
            img = np.array(sct.grab(monitor))
            return img
