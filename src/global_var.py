import ctypes
import multiprocessing

import cv2

INVALID_VALUE = -404

id = 100
dic = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
path = "aruco_code.png"
windowName = "Camera"
manager = multiprocessing.Manager()


path_find = manager.list()
frame_global = None
size = 15
destination = multiprocessing.Array(ctypes.c_int, [INVALID_VALUE, INVALID_VALUE])
coordinate_aruco = multiprocessing.Array(ctypes.c_float, [INVALID_VALUE, INVALID_VALUE, INVALID_VALUE])
obstacles_position = []  # TODO


thread = None


def get_path_find():
    global path_find
    return path_find


def set_path_find(path):
    global path_find
    path_find = path


def get_thread():
    global thread
    return thread


def set_thread(value):
    global thread
    thread = value


def set_coordinate_aruco(value):
    global coordinate_aruco
    if value is None:
        coordinate_aruco[0] = INVALID_VALUE
        coordinate_aruco[1] = INVALID_VALUE
        coordinate_aruco[2] = INVALID_VALUE
        return
    coordinate_aruco[0] = value[0]
    coordinate_aruco[1] = value[1]
    coordinate_aruco[2] = value[2]


def get_coordinate_aruco():
    global coordinate_aruco
    if coordinate_aruco[0] == coordinate_aruco[1] == INVALID_VALUE == coordinate_aruco[2]:
        return None
    return coordinate_aruco


def set_destination(value):
    global destination
    if value is None:
        destination[0] = INVALID_VALUE
        destination[1] = INVALID_VALUE
        return
    destination[0] = value[0]
    destination[1] = value[1]


def get_destination():
    global destination
    if destination[0] == destination[1] == INVALID_VALUE:
        return None
    return destination
    # return 50, 50


def get_obstacles_position():
    # TODO : the limits of the image should be obstacles
    global obstacles_position
    ox = []
    oy = []
    for i in range(-10, 60):
        ox.append(i)
        oy.append(-10.0)
    for i in range(-10, 60):
        ox.append(60.0)
        oy.append(i)
    for i in range(-10, 61):
        ox.append(i)
        oy.append(60.0)
    for i in range(-10, 61):
        ox.append(-10.0)
        oy.append(i)
    for i in range(-10, 40):
        ox.append(20.0)
        oy.append(i)
    for i in range(0, 40):
        ox.append(40.0)
        oy.append(60.0 - i)
    obstacles_position = zip(ox, oy)
    return obstacles_position


