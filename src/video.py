import time
from multiprocessing import freeze_support

import cv2

from aruco_function import detect_aruco, size_arena, draw_path
from global_var import (size, windowName, get_coordinate_aruco, set_destination, get_destination, get_thread,
                        set_thread, set_pixels_x, set_pixels_y, get_obstacles, CAMERA_INDICE, set_end_point,
                        get_begin_point, get_end_point, get_newly_obstacles,
                        set_newly_obstacles, get_path_find)
from pixel_mm_finder import calculate_px_mm_ratio
from process_data import process
from real_wold import discretization_X, discretization_Y
from threshold import get_obstacles_position_grid_from_frame

show_dis = False

# handle the click event
def click_event(event, x, y, flags, params):
    global frame_global
    # checking for left mouse clicks

    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        destina = get_destination()
        if destina is not None:
            if destina[0] - size < x < destina[0] + size:
                if destina[1] - size < y < destina[1] + size:
                    set_destination(None)
                    return

        # print("button clicked: x:" + str(x) + " y:" + str(y))
        if frame_global is not None:
            set_destination((x, y))


def draw_cross(frame, x, y):
    cv2.line(frame, (x - size, y - size), (x + size, y + size), (0, 0, 255), 5)
    cv2.line(frame, (x - size, y + size), (x + size, y - size), (0, 0, 255), 5)
    return frame

def get_indice_line():
    return [i * size for i in range(1, int(size / 2))]

def get_indice_column():
    return [i * size for i in range(1, int(size / 2))]


def draw_discretisation(frame):
    dis_X = discretization_X()
    dis_Y = discretization_Y()
    begin_point = get_begin_point()
    end_point = get_end_point()
    for i in range(len(dis_X)):
        if i != 0:
            cv2.line(frame, (int(dis_X[i]), begin_point[1]), (int(dis_X[i]), end_point[1]), (0, 0, 0), 1)

    for i in range(len(dis_Y)):
        if i != 0:
            cv2.line(frame, (begin_point[0], int(dis_Y[i])), (end_point[0], int(dis_Y[i])), (0, 0, 0), 1)

    return fill_obstacle(frame)
    #return frame


def fill_obstacle(frame):
    obstacles = get_obstacles()
    dis_X = discretization_X()
    dis_Y = discretization_Y()
    color = (0, 0, 255)
    for i in range(len(obstacles)):
            for j in range(len(obstacles[0])):
                if obstacles[i][j] == 1:
                    x = dis_X[j]
                    y = dis_Y[i]
                    if (j + 1 >= len(obstacles[0])):
                        max_X = get_end_point()[0]
                    else:
                        max_X = dis_X[j + 1]
                    if (i + 1 >= len(obstacles)):
                        max_Y = get_end_point()[1]
                    else:
                        max_Y = dis_Y[i + 1]
                    cv2.rectangle(frame, (int(x), int(y)), (int(max_X), int(max_Y)), color, 2)
                    #cv2.line(frame, (int(x), int(y)), (int(max_X), int(max_Y)), color, 1)
                    #cv2.line(frame, (int(max_X), int(y)), (int(x), int(max_Y)), color, 1)
    return frame


def open_camera():
    global destination, frame_global, thread, show_dis
    camera = cv2.VideoCapture(CAMERA_INDICE)  # opening the camera

    width = camera.get(3)  # float `width`
    height = camera.get(4)  # float `height`
    set_end_point((int(width), int(height)))
    print("size : " + str(width) + "," + str(height))
    set_pixels_y(get_end_point()[1] - get_begin_point()[1])
    set_pixels_x(get_end_point()[0] - get_begin_point()[0])


    if not camera.isOpened():  # error if the camera is impossible to find
        print("Erreur : impossible d'ouvrir la webcam")
        exit()

    print("Veuillez sélectionner la destination et appuyer sur entrée")
    print("Pour arrêter le robot si il est lancé appuyer sur 'q'")
    print("Pour afficher/cacher la discrétisation appuyer sur 'd'")
    print("Pour capturer une frame (détection obstacle) appuyer sur 'o'")
    print("Pour définir la taille de l'arène appuyer sur 'a'")
    print("Pour configurer le ratio pixel / cm placer le témoin et appuyer sur 'r'")


    cv2.namedWindow(windowName)
    cv2.setMouseCallback(windowName, click_event)
    start_time = time.time()
    while True:
        """
        reading the frames without interruptions in order to make a video
        stop only if reading is impossible or if we press "q"
        """
        retour, frame = camera.read()  # acquiring the image
        
        # error if it is impossible
        if not retour:
            print("Erreur : impossible d'ouvrir le flux vidéo")
            break

        framecopy = frame.copy()

        frame = exec_cam(frame)
        if (get_begin_point() != (0, 0)) or (get_end_point() != (width, height)):
            cv2.rectangle(frame, get_begin_point(), get_end_point(), (0, 255, 0), thickness=1)


        frame_global = frame

        if len(get_path_find()) > 0:
            frame = draw_path(frame)

        if get_destination() is not None:
            destina = get_destination()

            cv2.imshow(windowName, draw_cross(frame, destina[0], destina[1]))


        if show_dis:
            cv2.imshow(windowName, draw_discretisation(frame))
        else:
            cv2.imshow(windowName, frame)

        if get_newly_obstacles():
            obstacles = get_obstacles()
            for i in range(len(obstacles)):
                print("| ", end="")
                for j in range(len(obstacles[0])):
                    if obstacles[i][j] == 1:
                        print("1 ", end="")
                    else:
                        print("0 ", end="")
                print("|")
            print()
            set_newly_obstacles(False)

        if time.time() - start_time >= 5:
            # Perform the operation every 5 seconds
            get_obstacles_position_grid_from_frame(framecopy.copy(), False)
            start_time = time.time()

        key = cv2.waitKey(1) & 0xFF

        if key == ord('d'):
            show_dis = not show_dis

        if key == ord('a'):
            if get_thread() is not None:
                print("Impossible de redéfinir l'arène pendant que l'algorithme tourne")
                continue
            size_arena(framecopy.copy(), width, height)

        if key == ord('\r'):
            if get_destination is None:
                print("Veuillez sélectionner une destination")
                continue

            if get_coordinate_aruco() is None:
                print("Aucun robot détecté")
                continue

            process()

        if key == ord('r'):
            calculate_px_mm_ratio(framecopy.copy())


        if key == ord('q'):
            if get_thread() is not None:
                print("Arrêt de l'algorithme")
                get_thread().stop()
                set_thread(None)
                continue
            else:
                print("Aucun algorithme en cours d'exécution")
                continue

        if key == ord('o'):
            get_obstacles_position_grid_from_frame(framecopy.copy(), True)


        if cv2.getWindowProperty(windowName, cv2.WND_PROP_VISIBLE) < 1:
            break

        # showing the video with each acquisition
        cv2.imshow(windowName, frame)

    # closing the connection with the camera
    camera.release()
    
    # closing the open reading app
    cv2.destroyAllWindows()
    

    # Modify this function to do some stuff on the camera
def exec_cam(frame):
    return detect_aruco(frame)

def main():
    freeze_support()
    open_camera()

if __name__ == '__main__':
    main()
