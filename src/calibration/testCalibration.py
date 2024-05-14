"""
Second calibration to make sure of the results.
The matrix and distorsion work better when compared so this version is the official one.
Note : the difference with the flux without calibration is not huge,
       need to check if it is worth it for each acquisition of images.
"""

import numpy as np
import cv2
import os


def calibrate():
    # size of the chosen image mesauring 6 by 5 squares 
    taille_damier = (6,5)

    # Initialization with the size of the chessboard
    objp = np.zeros((taille_damier[0]*taille_damier[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:taille_damier[0], 0:taille_damier[1]].T.reshape(-1,2)

    objpoints = []
    imgpoints = []

    # The images of 'caliCaptureImages' are taken here
    dossierCalibration = "src/calibration/images/"  # the folder where the images are
    # We only proceed with images that are in the png format
    nomImages = [f for f in os.listdir(dossierCalibration) if f.endswith('.png')]
    nomImages.sort()
    # Previous check to see if they were well taken
    #print(nomImages)
    images = [os.path.join(dossierCalibration, image) for image in nomImages]
    #print(images)

    # iteration on each image so that the calibration gets better
    for nom in images : 
        # To see which images are calibrated
        print(nom)
        img = cv2.imread(nom)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        # OpenCV functions that gets the corners of the images thanks to the lines and color contrasts
        retour, coins = cv2.findChessboardCorners(gray, taille_damier, None)
    
        if retour == True :
            objpoints.append(objp)
            imgpoints.append(coins)
        
            # OpenCV function that return the image with the corners circled and the lines drawn
            img = cv2.drawChessboardCorners(img, taille_damier, coins, retour)
            
            # Visual check of the calibration process on the image
            cv2.imshow('img', img)
            cv2.waitKey(0)
        else:
            print("La calibration n'a pas pu être faite")
            # Allows to see which images are a problem due to luminosity or sharpness

    """ 
    OpenCV funtion that returns the matrix and vector needed in order to calibrate the camera
    instantly and not going through this process again.
    """
    retour, matrice, distorsion, rvec, tvec = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    # Checkpoint to see if the saving was done well
    print(matrice)
    print(distorsion)

    # Files that will be read in the future functions of trajectory
    np.save('2cameraMatrice.npy', matrice)
    np.save('2distorsionVecteur.npy', distorsion)

    # End of the video capture
    cv2.destroyAllWindows()



def main():
    calibrate()


# Linux adaptation
if __name__ == '__main__':
    main()
    
    