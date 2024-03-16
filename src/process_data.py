import math

from movement_control import rotate_robot, get_rotate_needed
from global_var import get_destination, get_coordinate_aruco


# d_?  -> destination coordinate
# c_?  -> robot coordinate  c_rotation rotation robot in deg
def process():
    destination = get_destination()
    coordinate = get_coordinate_aruco()
    c_x =  coordinate[0]
    c_y = coordinate[1]
    c_rotation = coordinate[2]
    d_x = destination[0]
    d_y = destination[1]
    print("process algo with:")
    print("c_x:" + str(c_x) + " c_y:" + str(c_y)  + "c_rotation:" + str(c_rotation) + " d_x:" + str(d_x) + " d_y:" + str(d_y))
    print("degree " + str(math.degrees(get_rotate_needed(c_x, c_y, d_x, d_y))))

    #rotate_robot(c_rotation, 0)