import cv2
import pickle

with open('matriceCamera.pkl', 'rb') as f:
    matCam = pickle.load(f)
    
with open('VecteurDistorsion.pkl', 'rb') as f:
    vecDis = pickle.load(f)

camera = cv2.VideoCapture(1)  # ouvrir la cam

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

camera.release()
cv2.destroyAllWindows()