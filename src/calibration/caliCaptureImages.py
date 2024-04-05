import cv2

camera = cv2.VideoCapture(1)  # ouvrir la cam

n = 0

if not camera.isOpened() :  # gestion erreur si elle ne l'est pas
    print("Erreur : Impossible d'ouvrir la webcam")
    exit()

while True:     # lecture en continu des images pour former un flux vidéo avec arrêt si lecture impossible ou touche 'q'
    retour , frame = camera.read()     # lis chaque image, si elle n'y est pas : erreur, sinon on l'affiche

    k=cv2.waitKey(5)
    
    if not retour :
        print("Erreur : Impossible d'ouvrir le flux vidéo")
        break
    
    if k == 27:
        break
    elif k == ord('s'):
        cv2.imwrite('src/calibration/images/frame' +str(n)+ '.png', frame)
        print("Image sauvegardée")
        n+=1

    cv2.imshow('Webcam', frame)

    c1,c2,_ = frame.shape
    #print("size : " + str(c2) + ","+ str(c1))
    #if cv2.waitKey(1) & 0xFF == ord('q'):    # waitKey 1 ms et touche 'q' pour quitter
    #    break

camera.release()
cv2.destroyAllWindows()