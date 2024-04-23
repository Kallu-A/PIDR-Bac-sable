import threading

import cv2
import numpy as np

from global_var import get_cells_xy, set_pixels_x, set_pixels_y, get_end_point, \
    set_end_point, set_begin_point, set_obstacles, set_newly_obstacles, get_obstacles, set_updated_obstacles, \
    get_begin_point, get_robot_size_in_pixel
from real_wold import discretization_Y, discretization_X, discretization_table


# Threshold the image to get the obstacles in the image
def threshold_from_frame(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    assert img_hsv is not None, "file could not be read, check with os.path.exists()"

    # Gen lower mask (0-5) and upper mask (175-180) of RED
    mask1 = cv2.inRange(img_hsv, (1, 100, 100), (4, 255, 255))
    mask2 = cv2.inRange(img_hsv, (176, 100, 100), (179, 255, 255))

    # Merge the mask and crop the red regions
    mask = cv2.bitwise_or(mask1, mask2)
    _, thresholded = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)

    return thresholded


def dilate_image(image, size_robot):
    kernel = np.ones((size_robot, size_robot), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# Make the obstacle detection in a process
def get_obstacles_position_grid_from_frame(image, flags):
    threading.Thread(target=runtime_calcul_loop, args=(image, flags)).start()

def remove_small_objects(binary_image, min_area=100):
    # Perform morphological closing
    kernel = np.ones((3, 3), np.uint8)
    closed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)

    # Find connected components (labels)
    num_labels, labels_image, stats, centroids = cv2.connectedComponentsWithStats(closed_image, connectivity=8)

    # Filter out small objects based on their area
    filtered_labels = np.zeros(labels_image.shape, dtype=np.uint8)
    for label in range(1, num_labels):
        area = stats[label, cv2.CC_STAT_AREA]
        if area >= min_area:
            filtered_labels[labels_image == label] = 255

    return filtered_labels


def runtime_calcul_loop(image, flags):
    # ROI of the image
    image = image[get_begin_point()[1]:get_end_point()[1], get_begin_point()[0]:get_end_point()[0]]

    # the percentage of which the box has to be filled before being count as a obstacle
    percent_box = 7

    dis_X = discretization_X(True)
    dis_Y = discretization_Y(True)
    dis_X.append(0)
    dis_Y.append(0)
    threshold = ((dis_Y[1] - dis_Y[0]) + (dis_X[1] - dis_X[0]) * percent_box) / 100
    threshold_img = threshold_from_frame(image)
    size_robot = get_robot_size_in_pixel()

    linear = remove_small_objects(threshold_img, threshold)

    dilated_image = dilate_image(linear, size_robot)
    cellsX, cellsY = get_cells_xy()
    obstacles = discretization_table()

    for x in range(cellsX):
        for y in range(cellsY):
            # test the box if it contains an obstacle
            count = 0
            for pix_x in range(dis_X[x], dis_X[x + 1]):
                if obstacles[y][x] == True:
                    break
                for pix_y in range(dis_Y[y], dis_Y[y + 1]):
                    k = dilated_image[pix_y, pix_x]
                    if k != 0:
                        count += 1
                    if count >= threshold:
                        obstacles[y][x] = True
                        break


    if not equal_tab(obstacles, get_obstacles()):
        set_updated_obstacles(True)

    set_obstacles(obstacles)
    if flags == True:
        set_newly_obstacles(True)


def equal_tab(obstacle1, obstacle2):
    if len(obstacle1) != len(obstacle2):
        return False

    for i in range(len(obstacle1)):
        for j in range(len(obstacle1[0])):
            if obstacle1[i][j] != obstacle2[i][j]:
                return False
    return True


## Legacy -------------


def voisin_true(tableau, k, j):
    """
    Cette fonction vérifie si la case (k, j) a un voisin True.
    """
    # Coordonnées des huit voisins possibles
    offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    for dx, dy in offsets:
        x, y = k + dx, j + dy
        if 0 <= x < len(tableau) and 0 <= y < len(tableau[0]) and tableau[x][y]:
            return True
    return False


def dilatation(obstacles):
    # if a case have a neighbour that is True, case = true
    new_obstacles = obstacles.copy()
    for i in range(len(obstacles)):
        for j in range(len(obstacles[0])):
            if voisin_true(obstacles, i, j):
                new_obstacles[i][j] = True
    return new_obstacles


def get_obstacles_pixels_position_from_frame(image):
    croped_image = threshold_from_frame(image)
    rows, cols, _ = croped_image.shape
    obstacles = []
    for i in range(rows):
        for j in range(cols):
            k = croped_image[i, j] # k = pixels color rgb
            if k[0] != 0 and k[1] != 0 and k[2] != 0:
                obstacles.append((i, j))
    return obstacles


def get_obstacles_coordinate_grid_from_frame(image):
    grid = get_obstacles_position_grid_from_frame(image)
    obstacles_coordinate_grid = []
    for i in range(len(grid)): # number of rows
        for j in range(len(grid[0])): # number of cols
            if grid[i][j] == 1:
                obstacles_coordinate_grid.append((j, i))
    return obstacles_coordinate_grid


if __name__ == "__main__":
    # image_path = "threshold/rond_rouge.jpg"
    # croped_image = threshold(image_path)
    img = cv2.imread("src/threshold/arene.png")
    rows, cols, _ = img.shape
    print(rows, cols)

    set_pixels_x(cols)
    set_pixels_y(rows)
    set_begin_point((0, 0))
    set_end_point((cols, rows))

    res = threshold_from_frame(img)
    cv2.imshow("img", img)
    cv2.imshow("thresold", res)
    kernel = np.ones((5, 5), np.uint8)
    res2 = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel, iterations=1)
    cv2.imshow("remove small object", res2)
    res3 = dilate_image(res2, 5)
    cv2.imshow("dilate", res3)

    cv2.waitKey()

    # #print(get_obstacles_pixels_position(image_path))
    # #print(get_obstacles_position_grid("threshold/rond_rouge.jpg"))
    # print(get_obstacles_coordinate_grid("threshold/rond_rouge.jpg"))
    runtime_calcul_loop(img, False)
    for i in get_obstacles():
        print(i)



