import cv2
import numpy as np

from global_var import path, dic, set_coordinate_aruco

# generate the camera code to identifie
def generate_aruco():
    tag = cv2.aruco.generateImageMarker(dic, id, 300)
    cv2.imwrite(path, tag)
    cv2.imshow("Aruco Tag", tag)
    cv2.waitKey(0)


def detect_aruco(img):
    global coordinate_aruco
    if img is None:
        print("Error: Could not read the image.")

    image_copy = img.copy()
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(image_copy, dic)

    #TODO to modify when camera is configure
    camera_matrix = np.array([[1.0, 0.0, image_copy.shape[1] / 2],
                              [0.0, 1.0, image_copy.shape[0] / 2],
                              [0.0, 0.0, 1.0]], dtype=np.float32)
    dist_coeffs = np.zeros((4, 1), dtype=np.float32)

    set_coordinate_aruco(None)
    if ids is not None and len(ids) > 0:
        for i in range(0, len(ids)):
            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, camera_matrix,
                                                                       dist_coeffs)

            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05, camera_matrix, dist_coeffs)

            """for rvec, tvec in zip(rvecs, tvecs):
                print("Rotation Vector:", rvec)
                print("Translation Vector:", tvec)"""
            (rvec - tvec).any()  # get rid of that nasty numpy value array error
            cv2.aruco.drawDetectedMarkers(image_copy, corners)  # Draw A square around the markers

            #cv2.drawFrameAxes(image_copy, camera_matrix, dist_coeffs, rvec, tvec, 0.01)  # Draw axis

            c_x = (corners[i][0][0][0] + corners[i][0][1][0] + corners[i][0][2][0] + corners[i][0][3][
                0]) / 4  # X coordinate of marker's center
            c_y = (corners[i][0][0][1] + corners[i][0][1][1] + corners[i][0][2][1] + corners[i][0][3][
                1]) / 4  # Y coordinate of marker's center
            # print("center aruco x:" + str(c_x) + " y:" + str(c_y))
            R, _ = cv2.Rodrigues(rvecs)
            _, _, _, _, _, _, euler_angles = cv2.decomposeProjectionMatrix(np.hstack((R, tvecs.reshape(3, 1))))
            yaw = convert_rotation(euler_angles[2][0])
            yaw_str = "{:.2f}".format(np.round(yaw, 2).item())
            cv2.putText(image_copy, "id" + str(ids[i]) + " rotation: " + yaw_str+" deg", (int(c_x), int(c_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 0, 0), 2)

            set_coordinate_aruco((c_x, c_y, yaw))

    return image_copy


"""    image = cv2.imread(img)
    arucoDict = cv2.camera.getPredefinedDictionary(cv2.camera.DICT_6X6_50)

    corners, ids, rejectedImgPoints = cv2.camera.detectMarkers(image, arucoDict)

    if ids is not None and len(ids) > 0:
        cv2.camera.drawDetectedMarkers(image, corners, ids)

    cv2.imshow("out", image)
"""

# convertion the rotation value in classic trigonometric value
def convert_rotation(rotation):
    if 0 <= rotation <= 90:
        return  90 - rotation
    if 90 < rotation <= 180:
        return - (rotation - 90)
    if -90 <= rotation < 0:
        return 90 + (rotation * -1)
    if -180 <= rotation < -90:
        return -(270 + rotation)