import cv2

id = 100
dic = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
path = "aruco_code.png"
windowName = "Camera"


frame_global = None
size = 15
destination = None
coordinate_aruco = None


def set_coordinate_aruco(value):
    global coordinate_aruco
    coordinate_aruco = value


def get_coordinate_aruco():
    global coordinate_aruco
    return coordinate_aruco
