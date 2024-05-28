import time

from utility.movement_control import get_rotate_needed
from global_var import get_destination, get_coordinate_aruco, get_thread, set_thread
from utility.stoppable_process import StoppableProcess
from dStarLite import dstar_algo




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
    dstar_algo()
