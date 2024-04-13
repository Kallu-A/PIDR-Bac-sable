import cv2
import numpy as np
from matplotlib import pyplot as plt
from real_wold import discretization_Y, discretization_X, convert_pixel_to_case, discretization_table
from global_var import get_cells_xy, get_pixels_xy, set_cells_y, set_cells_x, set_pixels_x, set_pixels_y


def threshold(image_file_name):
    img = cv2.imread(image_file_name)
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


def get_obstacles_pixels_position(image_path):
    croped_image = threshold(image_path)
    rows, cols, _ = croped_image.shape
    obstacles = []
    for i in range(rows):
        for j in range(cols):
            k = croped_image[i, j] # k = pixels color rgb
            if k[0] != 0 and k[1] != 0 and k[2] != 0:
                obstacles.append((i, j))
    return obstacles


def get_obstacles_position_grid(image_path):
    # obstacles[i] = 5 if obstacle in obstacles[i]
    croped_image = threshold(image_path)
    rows, cols, _ = croped_image.shape
    pixelsX, pixelsY = get_pixels_xy()
    cellsX, cellsY = get_cells_xy()
    obstacles = discretization_table()
    dis_X = discretization_X()
    dis_Y = discretization_Y()
    dis_X.append(pixelsX)
    dis_Y.append(pixelsY)
    for y in range(cellsY):
        for x in range(cellsX):
            for pix_y in range(dis_Y[y], dis_Y[y + 1]):
                if obstacles[y][x] == 1:
                    break
                for pix_x in range(dis_X[x], dis_X[x + 1]):
                    if obstacles[y][x] == 1:
                        break
                    k = croped_image[pix_y, pix_x]  # k = pixels color rgb
                    if k[0] != 0 and k[1] != 0 and k[2] != 0:
                        obstacles[y][x] = 1
    return obstacles


def get_obstacles_coordinate_grid(image_path):
    grid = get_obstacles_position_grid(image_path)
    obstacles_coordinate_grid = []
    for i in range(len(grid)): # number of rows
        for j in range(len(grid[0])): # number of cols
            if grid[i][j] == 1:
                obstacles_coordinate_grid.append((j, i))
    return obstacles_coordinate_grid


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


def get_obstacles_position_grid_from_frame(image):
    # obstacles[i] = 1 if obstacle in obstacles[i]
    croped_image = threshold_from_frame(image)
    pixelsX, pixelsY = get_pixels_xy()
    cellsX, cellsY = get_cells_xy()
    obstacles = discretization_table()
    dis_X = discretization_X()
    dis_Y = discretization_Y()
    dis_X.append(pixelsX)
    dis_Y.append(pixelsY)
    for y in range(cellsY):
        for x in range(cellsX):
            for pix_y in range(dis_Y[y], dis_Y[y+1]):
                if obstacles[y][x] == 1:
                    break
                for pix_x in range(dis_X[x], dis_X[x+1]):
                    if obstacles[y][x] == 1:
                        break
                    k = croped_image[pix_y, pix_x] # k = pixels color rgb
                    if k[0] != 0 and k[1] != 0 and k[2] != 0:
                        obstacles[y][x] = 1
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
    img = cv2.imread("threshold/horizontal-rouge.png")
    rows, cols, _ = img.shape
    set_pixels_x(cols)
    set_pixels_y(rows)
    set_cells_y(30)
    set_cells_x(30)
    # #print(get_obstacles_pixels_position(image_path))
    # #print(get_obstacles_position_grid("threshold/rond_rouge.jpg"))
    # print(get_obstacles_coordinate_grid("threshold/rond_rouge.jpg"))
    for i in get_obstacles_position_grid_from_frame(img):
        print(i)



