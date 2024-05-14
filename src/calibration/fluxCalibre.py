import cv2
import pickle
import numpy as np

from global_var import CAMERA_INDICE


"""
This file was made to compare the video without calibration and the video with calibration.
The point is to know if the result is coherent as first.
Then, we have to decide if the calibration is required or not for our progam to work efficiently.
"""


def flux():
    """
    The different versions of the calibration matrix have been kept for a demonstration of the previous results
    if asked for. The pictures have been deleted but can been found in previous commits.
    Previous results were sometimes realy differents as a small amount of pictures were actually calibrated
    due to luminosity or sharpness.
    """
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
    
    
    """
    Same thing for the distorsion vector.
    """

#with open('VecteurDistorsion.pkl', 'rb') as f:
#    vecDis = pickle.load(f)
    vecDis = np.array([[ 0.0888467 , -0.27385257 , 0.00293004 , 0.00122426 , 0.24195861]])
    
    #[[ 0.03372539, -0.16027559 ,-0.00416367, -0.00029969  ,0.22869658]])
    
    #[[ 0.79402254, -2.64382624,  0.01011316, -0.01501461 , 4.39716902]])

    #[[0.49662178,-0.95387139,-0.0028333,-0.02729056,0.9270895]])

    # Opening the camera
    camera = cv2.VideoCapture(CAMERA_INDICE)  

    if not camera.isOpened() :  
        # Throwing an error if the opening is not posiible
        print("Erreur : Impossible d'ouvrir la webcam")
        exit()

    # Constant reading of the acquired images in order to make a video
    while True:     
        # Acquisition of the images from the camera
        retour , frame = camera.read()     

        # If nothing comes from the function, we stop the program
        if not retour :
            print("Erreur : Impossible d'ouvrir le flux vidéo")
            break
            
        """
        The first channel will show the frame we usually have.
        The second channel shows the undistorted frames.
        The channels are put side by side for the comparison.
        """
        
        frameSansDistorsion = cv2.undistort(frame, matCam, vecDis)
        cv2.imshow('Image de base', frame)
        cv2.imshow('Image calibrée sans distorsion', frameSansDistorsion)

        # If the keyboard touch 'q' is pressed, we quit the video.
        if cv2.waitKey(1) & 0xFF == ord('q'):    
            break


        if cv2.getWindowProperty('Image de base', cv2.WND_PROP_VISIBLE) < 1:
            break


    # Closing the connection with the camera
    camera.release()
    
    # Closing both channels
    cv2.destroyAllWindows()


def main():
    flux()


# Linux adaptation 
if __name__ == '__main__':
    main()

