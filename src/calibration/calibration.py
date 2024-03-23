import numpy as np
import cv2 as cv
import glob
import pickle


chessboardSize = (5,4)
frameSize = (640,480)

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

size_of_chessboard_squares_mm = 30
objp = objp * size_of_chessboard_squares_mm

objpoints = [] # stockage des points dans le repère monde
imgpoints = [] # stockage des points dans le repère de l'image (plan 2D)


images = glob.glob('images/*.png')

for image in images:

    img = cv.imread(image)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Trouver les coins du damier
    ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)

    if ret == True:

        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)

        cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(1000)


cv.destroyAllWindows()


ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frameSize, None, None)

# Sauvegarde des résultats obtenus 
pickle.dump((cameraMatrix, dist), open( "calibration.pkl", "wb" ))
pickle.dump(cameraMatrix, open( "matriceCamera.pkl", "wb" ))
pickle.dump(dist, open( "VecteurDistorsion.pkl", "wb" ))

