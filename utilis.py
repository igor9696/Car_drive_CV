import numpy as np
import cv2 as cv


def draw_lines(image, lines):
    if lines is not None:
        for i in range(0, len(lines)):
            line = lines[i][0]
            # cv.line(image, (line[0], line[1]), (line[2], line[3]), (0, 0, 255), 3, cv.LINE_AA)
    return image


def draw_avg_line(image, lines):
    left_line = []
    right_line = []

    if lines is not None:
        for i in range(0, len(lines)):
            line = lines[i][0]
            x1, y1, x2, y2 = line
            # calc line slope; slope = y2-y1/x2-x1
            slope = (y2 - y1)/(x2 - x1)
            if slope == 0:
                continue
            elif slope > 0:
                left_line.append([x1, y1, x2, y2])
            elif slope < 0:
                right_line.append([x1, y1, x2, y2])

        # print('left line: ', left_line)
        # print('right line', right_line)

        left_avg = np.int16(np.average(left_line, axis=0))
        right_avg = np.int16(np.average(right_line, axis=0))

        # print('L AVG', left_avg)
        # print('R AVG', right_avg)

        # draw left and right average line
        try:
            cv.line(image, (left_avg[0], left_avg[1]), (left_avg[2], left_avg[3]), [0, 255, 0], 4)
            cv.line(image, (right_avg[0], right_avg[1]), (right_avg[2], right_avg[3]), [0, 255, 0], 4)

        except Exception:
            pass

        return image


def roi(image, vertices):
    mask = np.zeros_like(image)
    cv.fillPoly(mask, vertices, [255,255,255])
    roi_img = cv.bitwise_and(image, mask)
    return roi_img


def process_img(src_img):
    gray = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (3, 3), 0)
    canny = cv.Canny(blur, 50, 130)

    vertices = np.array([[350, 300], [450, 300], [800, 550], [0, 550]])
    roi_img = roi(canny, [vertices])

    lines = cv.HoughLinesP(roi_img, 1, np.pi/180, 100, minLineLength=120, maxLineGap=5)
    output_img = draw_lines(src_img, lines)
    draw_avg_line(output_img, lines)
    return output_img
