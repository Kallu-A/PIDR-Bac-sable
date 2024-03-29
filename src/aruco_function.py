import cv2
import numpy as np

from global_var import path, dic, set_coordinate_aruco, get_path_find
from movement_control import get_point_from_angle
from real_wold import convert_case_to_pixel

color_path = (102, 73, 52)
color = (85, 94, 235)



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

            corners0 = corners[0][0]

            # Calculate the Euclidean distance between the top-left and bottom-right corners
            distance = np.linalg.norm(corners0[0] - corners0[2])

            # The size of the marker is the distance between the opposite corners
            marker_size = distance

            (rvec - tvec).any()  # get rid of that nasty numpy value array error
            cv2.aruco.drawDetectedMarkers(image_copy, corners)  # Draw A square around the markers
            #cv2.drawFrameAxes(image_copy, camera_matrix, dist_coeffs, rvec, tvec, 0.01) # Draw axis

            c_x = (corners[i][0][0][0] + corners[i][0][1][0] + corners[i][0][2][0] + corners[i][0][3][
                0]) / 4  # X coordinate of marker's center
            c_y = (corners[i][0][0][1] + corners[i][0][1][1] + corners[i][0][2][1] + corners[i][0][3][
                1]) / 4  # Y coordinate of marker's center
            # print("center aruco x:" + str(c_x) + " y:" + str(c_y))
            R, _ = cv2.Rodrigues(rvecs)
            _, _, _, _, _, _, euler_angles = cv2.decomposeProjectionMatrix(np.hstack((R, tvecs.reshape(3, 1))))
            yaw = convert_rotation(euler_angles[2][0])

            new_x, new_y = get_point_from_angle(c_x, c_y, yaw, marker_size * 0.7)
            #cv2.arrowedLine(image_copy, (int(c_x), int(c_y)), (int(new_x), int(new_y)), color, max(int(marker_size / 40), 3))

            set_coordinate_aruco((c_x, c_y, yaw))

    if len(get_path_find()) > 0:
        draw_path(image_copy)
    return image_copy


def draw_path(img):
    # draw a line between each point
    (older_x, older_y) = (None, None)
    path_find = get_path_find()
    for index in range(0, len(path_find)):
        i, j = path_find[index]
        if index == 0:
            x, y = convert_case_to_pixel(i, j)
            older_x = x
            older_y = y
            continue
        x, y = convert_case_to_pixel(i, j)
        cv2.line(img, (older_x, older_y), (x, y), color_path, 3)
        (older_x, older_y) = (x, y)





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