import numpy as np
import cv2 as cv
import glob
import pickle


"""
Former version of the calibration inspired by an existing repository in order to understand
how the calibration process works.

The official calibration we use for this project is in the file 'testCalibration.py'
"""

# Number of squares that need to be found on the picture.
chessboardSize = (5,4)

# Size of the picture with the number of squares indicated.
frameSize = (640,480)

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Initialization
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

# Real world size of the squares on the picture.
size_of_chessboard_squares_mm = 30
objp = objp * size_of_chessboard_squares_mm

# Made to store the points from the real world mark
objpoints = [] 

# Made to store the points from the image (in 2D)
imgpoints = [] 

# Made to get the images captured previously in 'caliCaptureImages.py'.
images = glob.glob('images/*.png')

# Iteration on each image saved
for image in images:

    img = cv.imread(image)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Made to find the corners of the chessboard
    ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)

    # If the image could be analyzed, and the corners found :
    if ret == True:

        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)

        # Made to show the result with drawn corners and lines between them
        cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
        cv.imshow('img', img)
        
        # Long waitkey because there were no results in the beginnig
        #cv.waitKey(1000)
        
        cv.waitKey(10)


# Stopping the video
cv.destroyAllWindows()


# Calibration with all the points saved in both spaces (3D and 2D)
ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frameSize, None, None)


# Saving of the results in pkl format
pickle.dump((cameraMatrix, dist), open( "calibration.pkl", "wb" ))
pickle.dump(cameraMatrix, open("../matriceCamera.pkl", "wb"))
pickle.dump(dist, open("../VecteurDistorsion.pkl", "wb"))



