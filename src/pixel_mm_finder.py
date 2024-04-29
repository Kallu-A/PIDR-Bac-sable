import cv2
import numpy as np

from global_var import set_ratio_pixel_cm, size_circle_cm, get_robot_size_in_cm, get_ratio_pixel_cm


# detect a circle
def detect_circle(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    gray = cv2.medianBlur(gray, 3)

    # Apply thresholding to create a binary image
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # Apply morphological operations to enhance the circle's edges
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # Detect circles
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=2, param1=160, param2=70, minRadius=3,
                               maxRadius=1000)

    if circles is not None:
        circles = np.uint16(np.around(circles))
    else:
        return None, None
    for i in circles[0, :]:
        center = (i[0], i[1])
    # circle center
    cv2.circle(frame, center, 1, (0, 100, 100), 3)
    # circle outline
    radius = i[2]
    cv2.circle(frame, center, radius, (255, 0, 255), 3)

    return (frame, radius)


# calculate the ratio pixel/cm
def calculate_px_mm_ratio(frame):
    (frame, radius) = detect_circle(frame)
    if frame is None:
        print("Aucun rond detecté")
        return None
    cv2.imshow("Detection du temoin", frame)
    set_ratio_pixel_cm(size_circle_cm / (radius * 2))
    print("Ratio pixel/cm configuré " + str(get_ratio_pixel_cm()))


# return the size of the robot in pixel
def get_size_in_pixel_of_robot():
    return get_robot_size_in_cm() / get_ratio_pixel_cm()


if __name__ == '__main__':
    img = cv2.imread("res/round_detection.png")
    cv2.imshow("img", img)
    (frame, radius) = detect_circle(img)
    if frame is None:
        print("No round detected")
    else:
        cv2.imshow("detected circles", frame)
        print("Size of the circle " + str(radius * 2) + " in px")
    cv2.waitKey(0)