import numpy as np
import cv2 as cv
from game_control import *


def get_lines_center(image, line_1, line_2):
    try:
        x_l1, y_l1, x_l2, y_l2 = line_1
        x_r1, y_r1, x_r2, y_r2 = line_2

        left_slope = (y_l2 - y_l1) / (x_l2 - x_l1)
        right_slope = (y_r2 - y_r1) / (x_r2 - x_r1)

        # find mid X point both left and right line
        center_lx = (x_l2 - x_l1) / 2 + x_l1
        center_rx = (x_r2 - x_r1) / 2 + x_r1
        lanes_cnt = int(center_rx - (center_rx - center_lx) / 2)

        cv.circle(image, (int(center_lx), 400), 10, [255, 0, 0], -1)
        cv.circle(image, (int(center_rx), 400), 10, [255, 0, 0], -1)
        cv.circle(image, (lanes_cnt, 400), 10, [255, 255, 0], -1)

        return lanes_cnt, center_lx, center_rx

    except Exception:
        pass


def calc_avg_line(lines):
    left_line = []
    right_line = []

    try:
        # calculate average left and right line
        if lines is not None:
            for i in range(0, len(lines)):
                line = lines[i][0]
                x1, y1, x2, y2 = line
                # calc line slope; slope = y2-y1/x2-x1
                slope = (y2 - y1) / (x2 - x1)
                if slope == 0:
                    continue
                elif slope < 0:
                    left_line.append([x1, y1, x2, y2])
                elif slope > 0:
                    right_line.append([x1, y1, x2, y2])

            left_avg = np.int16(np.average(left_line, axis=0))
            right_avg = np.int16(np.average(right_line, axis=0))

            return left_avg, right_avg

    except Exception:
        pass


def draw_lines(image, lines):

    try:
        left_avg, right_avg = calc_avg_line(lines)

        # draw left,right average line and central point
        cv.line(image, (left_avg[0], left_avg[1]), (left_avg[2], left_avg[3]), [0, 255, 0], 6, cv.LINE_AA)
        cv.line(image, (right_avg[0], right_avg[1]), (right_avg[2], right_avg[3]), [0, 255, 0], 6, cv.LINE_AA)

        # draw fix central image line
        draw_image_cnt_line(image)

        # get center point between lines and draw edge points between two of them
        lanes_cnt, center_lx, center_rx = get_lines_center(image, left_avg, right_avg)
        cv.circle(image, (int(center_lx), 400), 10, [255, 0, 0], -1)
        cv.circle(image, (int(center_rx), 400), 10, [255, 0, 0], -1)
        cv.circle(image, (lanes_cnt, 400), 10, [255, 255, 0], -1)

    except Exception:
        pass


def roi(image, vertices):
    mask = np.zeros_like(image)
    cv.fillPoly(mask, vertices, [255,255,255])
    roi_img = cv.bitwise_and(image, mask)
    return roi_img


def draw_image_cnt_line(image):
    w, h = image.shape[1], image.shape[0]
    # cv.circle(image, (int(w/2), int(h/2 + 100)), 10, [0, 0, 255], -1)
    cv.line(image, (int(w/2), int(h/2)),(int(w/2), int(h/2) + 100), [0, 0, 255], 4, cv.LINE_AA)
    return image


def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensity
    median = np.median(image)
    # apply automatic canny edge detection
    lower = int(max(0, (1.0 - sigma) * median))
    upper = int(min(255, (1.0 - sigma) * median))
    canny = cv.Canny(image, lower, upper)

    return canny


def process_img(src_img):
    gray = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    canny = auto_canny(blur)

    vertices = np.array([[250, 350], [600, 350], [800, 600], [0, 600]])
    roi_img = roi(canny, [vertices])
    lines = cv.HoughLinesP(roi_img, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=20)
    draw_lines(src_img, lines)

    return src_img, lines


def steering_vehicle(image, lines):
    fixed_central = image.shape[1] / 2
    # steering

    try:
        # steering
        left_avg, right_avg = calc_avg_line(lines)
        lanes_cnt, center_lx, center_rx = get_lines_center(image, left_avg, right_avg)
        print('lanes cnt:{0}, fixed_central: {1}'.format(lanes_cnt, fixed_central))

        if (fixed_central < lanes_cnt - 30) and (fixed_central > lanes_cnt - 80):
            turn_right()

        elif (fixed_central > lanes_cnt + 30) and (fixed_central < lanes_cnt + 80):
            turn_left()

        elif (fixed_central > lanes_cnt - 50) and (fixed_central < lanes_cnt + 50):
            move_forward()

        else:
            slow_down()

    except Exception:
        slow_down()
