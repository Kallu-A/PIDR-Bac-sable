import cv2

from aruco_function import detect_aruco, coordinate_aruco, get_coordinate_aruco
from process_data import process

windowName = "Camera"
frame_global = None
size = 15
destination = None


# handle the click event
def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    global destination
    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        if destination is not None:
            if destination[0] - size < x < destination[0] + size:
                if destination[1] - size < y < destination[1] + size:
                    destination = None
                    return

        # print("button clicked: x:" + str(x) + " y:" + str(y))
        if frame_global is not None:
            destination = (x, y)


def draw_cross(frame, x, y):
    cv2.line(frame, (x - size, y - size), (x + size, y + size), (0, 0, 255), 5)
    cv2.line(frame, (x - size, y + size), ( x + size, y - size), (0, 0, 255), 5)
    return frame


def open_camera():
    camera = cv2.VideoCapture(0)  # ouvrir la cam

    if not camera.isOpened():  # gestion erreur si elle ne l'est pas
        print("Erreur : Impossible d'ouvrir la webcam")
        exit()

    print("Veuillez sélectionner la destination et appuyer sur entrée")
    global frame_global

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
        if destination is not None:
            cv2.imshow(windowName, draw_cross(frame, destination[0], destination[1]))



        if cv2.waitKey(1) & 0xFF == ord('\r'):
            if destination is None:
                print("Veuillez sélectionner une destination")
                continue

            print(coordinate_aruco)
            if get_coordinate_aruco() is None:
                print("Aucun robot détecté")
                continue

            process(0, 0, destination[0], destination[1])

        if cv2.getWindowProperty(windowName, cv2.WND_PROP_VISIBLE) < 1:
            break

    camera.release()
    cv2.destroyAllWindows()

    # Modify this function to do some stuff on the camera
def exec_cam(frame):
   return detect_aruco(frame)


if __name__ == '__main__':
    open_camera()
