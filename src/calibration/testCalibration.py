# Deuxième tentative de calibration pour s'assurer des résultats

import numpy as np
import cv2
import os


def calibrate():
    taille_damier = (6,5)

    objp = np.zeros((taille_damier[0]*taille_damier[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:taille_damier[0], 0:taille_damier[1]].T.reshape(-1,2)

    objpoints = []
    imgpoints = []

    dossierCalibration = "src/calibration/images/"
    nomImages = [f for f in os.listdir(dossierCalibration) if f.endswith('.png')]
    nomImages.sort()
    print(nomImages)
    images = [os.path.join(dossierCalibration, image) for image in nomImages]
    print(images)

    for nom in images : 
        print(nom)
        img = cv2.imread(nom)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        retour, coins = cv2.findChessboardCorners(gray, taille_damier, None)
    
        if retour == True :
            objpoints.append(objp)
            imgpoints.append(coins)
        
            img = cv2.drawChessboardCorners(img, taille_damier, coins, retour)
            cv2.imshow('img', img)
            cv2.waitKey(0)
        else:
            print("nope")

    retour, matrice, distorsion, rvec, tvec = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    print(matrice)
    print(distorsion)

    np.save('2cameraMatrice.npy', matrice)
    np.save('2distorsionVecteur.npy', distorsion)

    cv2.destroyAllWindows()

def main():
    calibrate()

if __name__ == '__main__':
    main()