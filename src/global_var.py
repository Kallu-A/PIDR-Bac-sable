import ctypes
import multiprocessing

import cv2


INVALID_VALUE = -404

id = 100
dic = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
path = "aruco_code.png"
windowName = "Camera"

frame_global = None
size = 15
destination = multiprocessing.Array(ctypes.c_int, [INVALID_VALUE, INVALID_VALUE])
coordinate_aruco = multiprocessing.Array(ctypes.c_float, [INVALID_VALUE, INVALID_VALUE, INVALID_VALUE])
path_find = []

thread = None

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    path_find = manager.list()


def get_path_find():
    global path_find
    return path_find


def set_path_find(path_found):
    global path_find
    path_find = path_found


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


