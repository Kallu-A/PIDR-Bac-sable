import cv2

from aruco_function import detect_aruco
from process_data import process
from global_var import size, windowName, get_coordinate_aruco, set_destination, get_destination


# handle the click event
def click_event(event, x, y, flags, params):
    global frame_global
    # checking for left mouse clicks

    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        destina = get_destination();
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
    cv2.line(frame, (x - size, y + size), ( x + size, y - size), (0, 0, 255), 5)
    return frame


def open_camera():
    global destination, frame_global
    camera = cv2.VideoCapture(0)  # ouvrir la cam

    if not camera.isOpened():  # gestion erreur si elle ne l'est pas
        print("Erreur : Impossible d'ouvrir la webcam")
        exit()

    print("Veuillez sélectionner la destination et appuyer sur entrée")

    while True:
        # lecture en continu des images pour former un flux vidéo avec arrêt si lecture impossible ou touche 'q'
        retour, frame = camera.read()  # lis chaque image, si elle n'y est pas : erreur, sinon on l'affiche

        if not retour:
            print("Erreur : Impossible d'ouvrir le flux vidéo")
            break

        frame = exec_cam(frame)
        cv2.imshow(windowName, frame)
        frame_global = frame
        cv2.setMouseCallback(windowName, click_event)
        if get_destination() is not None:
            destina = get_destination()
            cv2.imshow(windowName, draw_cross(frame, destina[0], destina[1]))



        if cv2.waitKey(1) & 0xFF == ord('\r'):
            if get_destination is None:
                print("Veuillez sélectionner une destination")
                continue

            if get_coordinate_aruco() is None:
                print("Aucun robot détecté")
                continue


            process()

        if cv2.getWindowProperty(windowName, cv2.WND_PROP_VISIBLE) < 1:
            break

    camera.release()
    cv2.destroyAllWindows()

    # Modify this function to do some stuff on the camera
def exec_cam(frame):
   return detect_aruco(frame)


if __name__ == '__main__':
    open_camera()
