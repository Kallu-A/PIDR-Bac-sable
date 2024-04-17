from multiprocessing import freeze_support

import time
import cv2

from aruco_function import detect_aruco, size_arena
from global_var import (size, windowName, get_coordinate_aruco, set_destination, get_destination, get_thread,
                        set_thread, set_pixels_x, set_pixels_y, get_obstacles, set_obstacles, \
                        CAMERA_INDICE, set_end_point, get_begin_point, get_end_point, get_newly_obstacles,
                        set_newly_obstacles)
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
    return frame


def open_camera():
    global destination, frame_global, thread, show_dis
    camera = cv2.VideoCapture(CAMERA_INDICE)  # ouvrir la cam

    width = camera.get(3)  # float `width`
    height = camera.get(4)  # float `height`
    set_end_point((int(width), int(height)))
    set_pixels_y(get_end_point()[1] - get_begin_point()[1])
    set_pixels_x(get_end_point()[0] - get_begin_point()[0])


    if not camera.isOpened():  # gestion erreur si elle ne l'est pas
        print("Erreur : Impossible d'ouvrir la webcam")
        exit()

    print("Veuillez sélectionner la destination et appuyer sur entrée")
    print("Pour arrêter le robot si il est lancé appuyer sur 'q'")
    print("Pour afficher/cacher la discrétisation appuyer sur 'd'")
    print("Pour capturer une frame (détection obstacle) appuyer sur 'o'")
    print("Pour définir la taille de l'arène appuyer sur 'a'")


    cv2.namedWindow(windowName)
    cv2.setMouseCallback(windowName, click_event)
    while True:
        # lecture en continu des images pour former un flux vidéo avec arrêt si lecture impossible ou touche 'q'
        retour, frame = camera.read()  # lis chaque image, si elle n'y est pas : erreur, sinon on l'affiche

        if not retour:
            print("Erreur : Impossible d'ouvrir le flux vidéo")
            break

        framecopy = frame.copy()

        frame = exec_cam(frame)
        if (get_begin_point() != (0, 0)) or (get_end_point() != (width, height)):
            cv2.rectangle(frame, get_begin_point(), get_end_point(), (0, 255, 0), thickness=1)


        frame_global = frame

        if get_destination() is not None:
            destina = get_destination()

            cv2.imshow(windowName, draw_cross(frame, destina[0], destina[1]))

        if show_dis:
            cv2.imshow(windowName, draw_discretisation(frame))
        else:
            cv2.imshow(windowName, frame)

        if get_newly_obstacles():
            for i in get_obstacles():
                print(i)
            print("\n")
            set_newly_obstacles(False)


        key = cv2.waitKey(1) & 0xFF

        if key == ord('d'):
            show_dis = not show_dis

        if key == ord('a'):
            if get_thread() is not None:
                print("Impossible de redéfinir l'arène pendant que l'algorithme tourne")
                continue
            size_arena(framecopy, width, height)

        if key == ord('\r'):
            if get_destination is None:
                print("Veuillez sélectionner une destination")
                continue

            if get_coordinate_aruco() is None:
                print("Aucun robot détecté")
                continue

            process()

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
            get_obstacles_position_grid_from_frame(frame)


        if cv2.getWindowProperty(windowName, cv2.WND_PROP_VISIBLE) < 1:
            break

        cv2.imshow(windowName, frame)

    camera.release()
    cv2.destroyAllWindows()

    # Modify this function to do some stuff on the camera
def exec_cam(frame):
    return detect_aruco(frame)

def main():
    freeze_support()
    open_camera()

if __name__ == '__main__':
    main()
