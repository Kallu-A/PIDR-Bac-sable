import ctypes
import multiprocessing

import cv2

CAMERA_INDICE = 0
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

newly_obstacles = False  # if obstacles have been newly modifed
newly_updated_obstacles = multiprocessing.Value('b', False)  # if obstacles have been newly modifed

# perimeter of the arena
beginPoint = (0, 0)
endPoint = (0, 0)

robot_size_in_cm = 11
ratio_pixel_cm = 1.0  # ratio calculated to convert pixel to cm


## CAN BE CHANGED

cells_x = 10  # number of cells wanted for x axis discretization
cells_y = 10  # number of cells wanted for y axis discretization
pixels_x = 0  # number of pixels on x axis
pixels_y = 0  # number of pixels on y axis

size_circle_cm = 3.9  # size of the circle in cm



thread = None
obstacles = multiprocessing.Array(ctypes.c_bool, cells_x * cells_y)


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


def get_cells_xy():
    global cells_x, cells_y
    return cells_x, cells_y


def set_cells_x(value):
    global cells_x
    if value is None:
        cells_x = INVALID_VALUE
        return None
    cells_x = value


def set_cells_y(value):
    global cells_y
    if value is None:
        cells_y = INVALID_VALUE
        return None
    cells_y = value


def get_pixels_xy():
    global pixels_x, pixels_y
    return pixels_x, pixels_y


def set_pixels_x(value):
    global pixels_x
    if value is None:
        pixels_x = INVALID_VALUE
        return None
    pixels_x = value


def set_pixels_y(value):
    global pixels_y
    if value is None:
        pixels_y = INVALID_VALUE
        return None
    pixels_y = value


def set_obstacles(obs_grid):
    global obstacles
    obstacles_np = get_obstacles()
    for i in range(cells_x):
        for j in range(cells_y):
            obstacles_np[i][j] = obs_grid[i][j]


def get_obstacles():
    global obstacles
    import numpy as np
    obstacles_np = np.frombuffer(obstacles.get_obj(), dtype=np.bool_).reshape(
        (cells_x, cells_y))

    return obstacles_np


def get_begin_point():
    global beginPoint
    return beginPoint


def get_end_point():
    global endPoint
    return endPoint


def set_begin_point(value):
    global beginPoint
    beginPoint = value


def set_end_point(value):
    global endPoint
    endPoint = value


def get_newly_obstacles():
    global newly_obstacles
    return newly_obstacles


def set_newly_obstacles(value):
    global newly_obstacles
    newly_obstacles = value


def get_robot_size_in_cm():
    global robot_size_in_cm
    return robot_size_in_cm


def get_updated_obstacles():
    global newly_updated_obstacles
    return newly_updated_obstacles.value


def set_updated_obstacles(value):
    global newly_updated_obstacles
    newly_updated_obstacles.value = value


def get_distance_camera():
    global distance_camera
    return distance_camera


def set_distance_camera(value):
    global distance_camera
    distance_camera = value


def get_ratio_pixel_cm():
    global ratio_pixel_cm
    return ratio_pixel_cm


def set_ratio_pixel_cm(value):
    global ratio_pixel_cm
    ratio_pixel_cm = value
