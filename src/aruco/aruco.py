import cv2

id = 100
dic = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
path = "aruco_code.png"

# generate the aruco code to identifie
def generate_aruco():
    tag = cv2.aruco.generateImageMarker(dic, id, 300)
    cv2.imwrite(path, tag)
    cv2.imshow("ArUCo Tag", tag)
    cv2.waitKey(0)


def detect_aruco(img):
    image = cv2.imread(img)
    if image is None:
        print("Error: Could not read the image.")
    else:
        print("Image shape:", image.shape)
    cv2.namedWindow("out", cv2.WINDOW_NORMAL)
    cv2.imshow("out", image)

    imageCopy = image.copy()
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(image, dic)

    if ids is not None and len(ids) > 0:
        cv2.aruco.drawDetectedMarkers(imageCopy, corners, ids)

    while 1 == 1:

        cv2.imshow("out", imageCopy)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # waitKey 1 ms et touche 'q' pour quitter
            break

    cv2.destroyAllWindows()


"""    image = cv2.imread(img)
    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)

    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(image, arucoDict)

    if ids is not None and len(ids) > 0:
        cv2.aruco.drawDetectedMarkers(image, corners, ids)

    cv2.imshow("out", image)
"""

if __name__ == '__main__':
    detect_aruco("img/test.png")