import multiprocessing

from global_var import get_path_find
from trajectoryTracking import follow_trajectory


def process_tracking():
    multiprocessing.Process(target=runtime_loop_tracking, args=()).start()

def runtime_loop_tracking():
    path = get_path_find()

    pathx = []
    pathy = []
    orientations = []
    for i in range(0, len(path)):
        if (path[i] == -1):
            break
        pathx.append(path[i][0])
        pathy.append(path[i][1])
        orientations.append(path[i][2])

    follow_trajectory(pathx, pathy, orientations)