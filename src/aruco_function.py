import cv2
import numpy as np

from global_var import path, dic, set_coordinate_aruco, get_path_find, set_begin_point, set_end_point, get_end_point, \
    get_begin_point, set_pixels_y, set_pixels_x
from utility.movement_control import get_point_from_angle
from real_wold import convert_case_to_pixel

color_path = (102, 73, 52)
color = (85, 94, 235)



# generate the camera code to identifie
def generate_aruco(id):
    tag = cv2.aruco.generateImageMarker(dic, id , 200)
    cv2.imwrite(path, tag)
    cv2.imshow("Aruco Tag", tag)
    cv2.waitKey(0)


def detect_aruco(img):
    global coordinate_aruco
    if img is None:
        print("Error: Could not read the image.")

    image_copy = img.copy()

    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(image_copy, dic)

    """ with open('src/matriceCamera.pkl', 'rb') as f:
        camera_matrix = pickle.load(f)
    with open('src/VecteurDistorsion.pkl', 'rb') as f:
        dist_coeffs = pickle.load(f) """


    camera_matrix = np.load('src/calibration/2cameraMatrice.npy')
    dist_coeffs = np.load('src/calibration/2distorsionVecteur.npy')

    set_coordinate_aruco(None)
    if ids is not None and len(ids) > 0:
        for i in range(0, len(ids)):

            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, camera_matrix,
                                                                       dist_coeffs)

            #rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05, camera_matrix, dist_coeffs)

            corners0 = corners[0][0]

            # Calculate the Euclidean distance between the top-left and bottom-right corners
            distance = np.linalg.norm(corners0[0] - corners0[2])

            # The size of the marker is the distance between the opposite corners
            marker_size = distance

            (rvec - tvec).any()  # get rid of that nasty numpy value array error

            cv2.aruco.drawDetectedMarkers(image_copy, corners)  # Draw A square around the markers

            if (ids[i] != 100):
                continue

            cv2.drawFrameAxes(image_copy, camera_matrix, dist_coeffs, rvec, tvec, 0.01) # Draw axis

            c_x = (corners[i][0][0][0] + corners[i][0][1][0] + corners[i][0][2][0] + corners[i][0][3][
                0]) / 4  # X coordinate of marker's center
            c_y = (corners[i][0][0][1] + corners[i][0][1][1] + corners[i][0][2][1] + corners[i][0][3][
                1]) / 4  # Y coordinate of marker's center

            R, _ = cv2.Rodrigues(rvec)
            _, _, _, _, _, _, euler_angles = cv2.decomposeProjectionMatrix(np.hstack((R, tvec.reshape(3, 1))))
            yaw = convert_rotation(euler_angles[2][0])

            new_x, new_y = get_point_from_angle(c_x, c_y, yaw, marker_size * 0.7)
            cv2.arrowedLine(image_copy, (int(c_x), int(c_y)), (int(new_x), int(new_y)), color, max(int(marker_size / 40), 3))

            set_coordinate_aruco((c_x, c_y, yaw))

           

    if len(get_path_find()) > 0:
        draw_path(image_copy)
    return image_copy

def size_arena(frame, width, height):
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dic)
    if ids is not None and len(ids):
        if len(ids) == 1 or len(ids) > 2:
            print("Erreur: il faut 2 code aruco")
            return

        i = 0
        first_x = int((corners[i][0][0][0] + corners[i][0][1][0] + corners[i][0][2][0] + corners[i][0][3][
            0]) / 4)  # X coordinate of marker's center
        first_y = int((corners[i][0][0][1] + corners[i][0][1][1] + corners[i][0][2][1] + corners[i][0][3][
            1]) / 4)  # Y coordinate of marker's center

        i = 1
        second_x = int((corners[i][0][0][0] + corners[i][0][1][0] + corners[i][0][2][0] + corners[i][0][3][
            0]) / 4)  # X coordinate of marker's center
        second_y= int((corners[i][0][0][1] + corners[i][0][1][1] + corners[i][0][2][1] + corners[i][0][3][
            1]) / 4)  # Y coordinate of marker's center

        set_begin_point((min(first_x, second_x), min(first_y, second_y)) )
        set_end_point((max(first_x, second_x), max(first_y, second_y)) )
        set_pixels_y(get_end_point()[1] - get_begin_point()[1])
        set_pixels_x(get_end_point()[0] - get_begin_point()[0])
        return

    if (get_begin_point() == (0, 0) and get_end_point() == (width, height)):
        return

    print("Réinitialisation de l'arène")
    set_begin_point((0, 0))
    set_end_point((int(width), int(height)))
    set_pixels_y(get_end_point()[1] - get_begin_point()[1])
    set_pixels_x(get_end_point()[0] - get_begin_point()[0])


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
        return 90 - rotation
    if 90 < rotation <= 180:
        return - (rotation - 90)
    if -90 <= rotation < 0:
        return 90 + (rotation * -1)
    if -180 <= rotation < -90:
        return -(270 + rotation)




if __name__ == '__main__':
    generate_aruco(100)
