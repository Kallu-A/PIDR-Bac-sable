import threading

import cv2

from global_var import get_cells_xy, get_pixels_xy, set_cells_y, set_cells_x, set_pixels_x, set_pixels_y, get_end_point, \
    set_end_point, set_begin_point, set_obstacles, set_newly_obstacles, get_obstacles
from real_wold import discretization_Y, discretization_X, discretization_table



def threshold_from_frame(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    assert img_hsv is not None, "file could not be read, check with os.path.exists()"
    # hist = cv2.calcHist([img],[0],None,[256],[0,256])
    # plt.hist(img.ravel(),256,[0,256]); plt.show()

    # Gen lower mask (0-5) and upper mask (175-180) of RED
    mask1 = cv2.inRange(img_hsv, (0, 50, 20), (5, 255, 255))
    mask2 = cv2.inRange(img_hsv, (175, 50, 20), (180, 255, 255))

    # Merge the mask and crop the red regions
    mask = cv2.bitwise_or(mask1, mask2)
    croped = cv2.bitwise_and(img, img, mask=mask)

    # # Display
    # cv2.imshow("mask", mask)
    # cv2.imshow("croped", croped)
    # cv2.waitKey()

    return croped



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


# Make the obstacle detection in a process
def get_obstacles_position_grid_from_frame(image, flags):
    threading.Thread(target=runtime_calcul_loop, args=(image, flags)).start()


def runtime_calcul_loop(image, flags):
    # obstacles[i] = 1 if obstacle in obstacles[i]
    croped_image = threshold_from_frame(image)
    pixelsX, pixelsY = get_pixels_xy()
    cellsX, cellsY = get_cells_xy()
    obstacles = discretization_table()
    dis_X = discretization_X()
    dis_Y = discretization_Y()
    dis_X.append(get_end_point()[0])
    dis_Y.append(get_end_point()[1])


    for y in range(cellsY):
        for x in range(cellsX):
            for pix_y in range(dis_Y[y], dis_Y[y + 1]):
                if obstacles[y][x] == True:
                    break
                for pix_x in range(dis_X[x], dis_X[x + 1]):
                    k = croped_image[pix_y, pix_x]
                    if k[0] != 0 and k[1] != 0 and k[2] != 0:
                        obstacles[y][x] = True
                        break

    #obstacles = dilatation(obstacles)

    set_obstacles(obstacles)
    if flags == True:
        set_newly_obstacles(True)


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
    img = cv2.imread("src/threshold/barre-rouge.jpg")
    rows, cols, _ = img.shape
    print(rows, cols)

    set_pixels_x(cols)
    set_pixels_y(rows)
    set_begin_point((0, 0))
    set_end_point((cols, rows))

    # #print(get_obstacles_pixels_position(image_path))
    # #print(get_obstacles_position_grid("threshold/rond_rouge.jpg"))
    # print(get_obstacles_coordinate_grid("threshold/rond_rouge.jpg"))
    runtime_calcul_loop(img, False)
    for i in get_obstacles():
        print(i)

    print("dilatation")
    dil = dilatation(get_obstacles())
    for i in dil:
        print(i)






