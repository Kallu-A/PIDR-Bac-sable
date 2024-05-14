import cv2


"""
This file aims to save picture of the printed chessboard in order to have several vues and make the calibration.
The process id as follows : 
- opening the camera we use for the whole project
- take several pictures with the same numbers of boxes
- change the point of view to exploit every angle distorsion
- save the pics for the calibration program.
"""

    
# Opening the camera
camera = cv2.VideoCapture(1)  

# Counter for the number of pictures saved
n = 0

# Throwing an error and quitting if the camera does not open
if not camera.isOpened() :  
    print("Erreur : Impossible d'ouvrir la webcam")
    exit()


# Constant reading of the frames in order to make a video
while True:     
    
    # reading of each frame
    retour , frame = camera.read()     

    k=cv2.waitKey(5)
    
    # Error message if no frame comes out of the reading
    if not retour :
        print("Erreur : Impossible d'ouvrir le flux vidéo")
        break
    
    if k == 27:
        break
    elif k == ord('s'):
        cv2.imwrite('src/calibration/images/frame' +str(n)+ '.png', frame)
        print("Image sauvegardée")
        n+=1
        
        """
        If the keyboard touch 's' is pressed, we save the frame as a picture.
        The process is automatic thanks to the counters that allow the saving to be entitled frameX.png 
        with the number incrementating each time.
        
        The counter is increased after each saving so that the names are always differents and do not 
        erase the previous one.
        """

    # Showing the video
    cv2.imshow('Webcam', frame)

    c1,c2,_ = frame.shape
    #print("size : " + str(c2) + ","+ str(c1))
    #if cv2.waitKey(1) & 0xFF == ord('q'):    # waitKey 1 ms et touche 'q' pour quitter
    #    break

# Stopping the connection with the camera
camera.release()

# Closing the video window
cv2.destroyAllWindows()


"""
This program was not adaptated for Linux as it only needs to be done once.
"""


