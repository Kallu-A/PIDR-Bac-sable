import time

import cv2
import pickle

if __name__ == '__main__':


    with open('src/calibration/matriceCamera.pkl', 'rb') as f:
        matCam = pickle.load(f)

    with open('src/calibration/VecteurDistorsion.pkl', 'rb') as f:
        vecDis = pickle.load(f)

    camera = cv2.VideoCapture(0)  # ouvrir la cam

    if not camera.isOpened() :  # gestion erreur si elle ne l'est pas
        print("Erreur : Impossible d'ouvrir la webcam")
        exit()

    while True:     # lecture en continu des images pour former un flux vidéo avec arrêt si lecture impossible ou touche 'q'
        retour , frame = camera.read()     # lis chaque image, si elle n'y est pas : erreur, sinon on l'affiche

        if not retour :
            print("Erreur : Impossible d'ouvrir le flux vidéo")
            break

        frameSansDistorsion = cv2.undistort(frame, matCam, vecDis)
        cv2.imshow('Image de base', frame)
        cv2.imshow('Image calibree sans distorsion', frameSansDistorsion)

        if cv2.waitKey(1) & 0xFF == ord('q'):    # waitKey 1 ms et touche 'q' pour quitter
            break


        if cv2.getWindowProperty('Image de base', cv2.WND_PROP_VISIBLE) < 1:
            break

        if cv2.getWindowProperty('Image calibree sans distorsion', cv2.WND_PROP_VISIBLE) < 1:
            break


        time.sleep(2)

    camera.release()
    cv2.destroyAllWindows()