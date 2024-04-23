import cv2
import pickle
import numpy as np

from global_var import CAMERA_INDICE


def flux():
#with open('matriceCamera.pkl', 'rb') as f:
#    matCam = pickle.load(f)
    matCam = np.array([[506.17650794 ,  0.    ,     310.76688925],
    [  0.  ,       510.5011209 , 259.53913951],
    [  0.     ,      0.     ,      1.        ]])
    
    #[[550.96720104,   0.  ,       307.89267498],
    #  [  0.     ,    554.23214227 ,250.58523174],
    #   [  0.     ,      0.     ,      1.        ]])
    
    #[[721.38482411,   0. ,        385.51215386],
    #  [  0.  ,       672.89222574, 238.31929405],
    #   [  0.  ,         0.    ,       1.        ]])

    #[[572.19233691, 0, 406.86429133],
    #      [0, 543.70244244, 253.51979463],
    #      [0, 0, 1,]])

#with open('VecteurDistorsion.pkl', 'rb') as f:
#    vecDis = pickle.load(f)
    vecDis = np.array([[ 0.0888467 , -0.27385257 , 0.00293004 , 0.00122426 , 0.24195861]])
    
    #[[ 0.03372539, -0.16027559 ,-0.00416367, -0.00029969  ,0.22869658]])
    
    #[[ 0.79402254, -2.64382624,  0.01011316, -0.01501461 , 4.39716902]])

    #[[0.49662178,-0.95387139,-0.0028333,-0.02729056,0.9270895]])

    camera = cv2.VideoCapture(CAMERA_INDICE)  # ouvrir la cam

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
        cv2.imshow('Image calibrée sans distorsion', frameSansDistorsion)

        if cv2.waitKey(1) & 0xFF == ord('q'):    # waitKey 1 ms et touche 'q' pour quitter
            break


        if cv2.getWindowProperty('Image de base', cv2.WND_PROP_VISIBLE) < 1:
            break



    camera.release()
    cv2.destroyAllWindows()


def main():
    flux()

if __name__ == '__main__':
    main()
