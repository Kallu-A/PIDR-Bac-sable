import multiprocessing

from global_var import get_path_find
from trajectoryTracking import follow_trajectory


def process_tracking():
    multiprocessing.Process(target=runtime_loop_tracking, args=()).start()

def runtime_loop_tracking():
    path = get_path_find()

    pathx = []
    pathy = []
    size = []
    orientations = []
    size_counter = 1
    for i in range(0, len(path)):
        if (path[i] == -1):
            break
        if i < len(path) - 1 and i - 1 >= 0 :
            if path[i][2] == path[i+1][2] and path[i][2] == orientations[len(orientations) - 1]:
                size_counter += 1
                continue


        pathx.append(path[i][0])
        pathy.append(path[i][1])
        orientations.append(path[i][2])
        size.append(size_counter)
        size_counter = 1



    follow_trajectory(pathx, pathy, orientations, size)