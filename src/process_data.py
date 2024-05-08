import time

from utility.movement_control import get_rotate_needed
from global_var import get_destination, get_coordinate_aruco, get_thread, set_thread
from utility.stoppable_process import StoppableProcess




# d_?  -> destination coordinate
# c_?  -> robot coordinate  c_rotation rotation robot in deg
def process():

    if get_thread() is not None:
        #robot = Robot()
        get_thread().stop()
        set_thread(None)
        #robot.stop()

    set_thread(StoppableProcess(runtime_loop))
    get_thread().start()


def runtime_loop():
    while 1 == 1:
        destination = get_destination()
        coordinate = get_coordinate_aruco()
        if destination is None or coordinate is None:
            time.sleep(0.1)
            continue

        c_x = int(coordinate[0])
        c_y = int(coordinate[1])
        c_rotation = coordinate[2]
        d_x = destination[0]
        d_y = destination[1]
        print("process algo with:")
        print("c_x:" + str(c_x) + " c_y:" + str(c_y) + " c_rotation:" + str(c_rotation) + " d_x:" + str(d_x) + " d_y:" + str(
            d_y))
        print("degree " + str(get_rotate_needed(c_x, c_y, d_x, d_y)))
        time.sleep(1)

    # rotate_robot(c_rotation, 0)