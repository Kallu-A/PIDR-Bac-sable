import math

from global_var import set_coordinate_aruco, get_coordinate_aruco, get_pixels_xy, get_cells_xy, set_cells_x, set_cells_y, set_pixels_y, set_pixels_x, get_begin_point, get_end_point, set_end_point, set_begin_point


# convert the case i,j (in meters) in coordinate (middle pixel) x,y in the image (pixel)
def convert_meters_to_pixels(i, j, scaleX, scaleY):
    # scaleX = realMeasureX / number of pixels X (m/px)
    # scaleY = realMeasureY / number of pixels Y (m/px)
    x = i / scaleX
    y = j / scaleY
    return x, y


# convert the pixel x,y in the image to case i,j (in real world)
def convert_pixels_to_meters(x, y, scaleX, scaleY):
    # scaleX = realMeasureX / number of pixels X (m/px)
    # scaleY = realMeasureY / number of pixels Y (m/px)
    i = x * scaleX
    j = y * scaleY
    return i, j


# convert the case i,j in coordinate x,y in the image (pixel)
def convert_case_to_pixel(i, j):
    cellsX, cellsY = get_cells_xy()
    pixelsX, pixelsY = get_pixels_xy()
    tabX = discretization_X()
    tabY = discretization_Y()
    if tabX[i] == tabX[-1]:
        x = (pixelsX - 1 + tabX[i]) // 2
    else:
        x = (tabX[i] + tabX[i + 1]) // 2

    if tabY[j] == tabY[-1]:
        y = (pixelsY - 1 + tabY[j]) // 2
    else:
        y = (tabY[j] + tabY[j + 1]) // 2

    return x, y


# convert the pixel x,y in the image to case i,j
def convert_pixel_to_case(x, y):
    cellsX, cellsY = get_cells_xy()
    pixelsX, pixelsY = get_pixels_xy()
    tabX = discretization_X()
    tabY = discretization_Y()
    i = 0
    j = 0


    while not tabX[i] <= x < tabX[i + 1]:
        i += 1
        if x >= tabX[i] and tabX[i] == tabX[-1]:
            break

    while not tabY[j] <= y < tabY[j + 1]:
        j += 1
        if y >= tabY[j] and tabY[j] == tabY[-1]:
            break

    return i, j


def discretization_X(isROI=False):
    begin_point = get_begin_point()
    # cellsX : number of cells wanted for X axis
    # pixelsX : number of pixels for the X axis (horizontal)

    cellsX, cellsY = get_cells_xy()
    pixelsX, pixelsY = get_pixels_xy()

    tabX = [0] # will contain indexes of the first pixel of separation between cells, for X axis
    if cellsX > pixelsX:
        print("discretization error : cellsX > pixelsX")
        return

    if cellsX == 0:
        print("The number of cells on X axis can't be 0")
        return

    if pixelsX == 0:
        print("The number of pixels on X axis can't be 0")
        return

    if cellsX == pixelsX:
        return [i for i in range(cellsX)]

    pixNb = 0
    for i in range(cellsX):
        pixNb += pixelsX // cellsX
        tabX.append(pixNb)

    if get_end_point()[0] - tabX[-1] > 0:
        toAdd = 0
        for i in range(len(tabX)):
            tabX[i] += toAdd
            if toAdd < (pixelsX - tabX[-1]):
                toAdd += 1

    if tabX[-1] == pixelsX:
        tabX.pop()

    if not isROI:
        for i in range(len(tabX)):
            tabX[i] = tabX[i] + get_begin_point()[0]
    return tabX


def discretization_Y(isROI=False):
    begin_point = get_begin_point()
    # cellsY : number of cells wanted for Y axis
    # pixelsY : number of pixels for the Y axis (horizontal)
    cellsX, cellsY = get_cells_xy()
    pixelsX, pixelsY = get_pixels_xy()
    tabY = [0]  # will contain indexes of the first pixel of separation between cells, for X axis
    if cellsY > pixelsY:
        print("discretization error : cellsY > pixelsY")
        return

    if cellsY == 0:
        print("The number of cells on Y axis can't be 0")
        return

    if pixelsY == 0:
        print("The number of pixels on Y axis can't be 0")
        return

    if cellsY == pixelsY:
        return [i for i in range(cellsY)]

    pixNb = 0
    for i in range(cellsY):
        pixNb += pixelsY // cellsY
        tabY.append(pixNb)

    if get_end_point()[1] - tabY[-1] > 0:
        toAdd = 0
        for i in range(len(tabY)):
            tabY[i] += toAdd
            if toAdd < (pixelsY - tabY[-1]):
                toAdd += 1
    if tabY[-1] == pixelsY:
        tabY.pop()

    if not isROI:
        for i in range(len(tabY)):
            tabY[i] = tabY[i] + get_begin_point()[1]
    return tabY


def discretization_table():
    # return the discretization grid initialized with 0
    cellsX, cellsY = get_cells_xy()
    table = [[False for col in range(cellsX)] for row in range(cellsY)]
    return table


def is_robot_in_case(case_x_goal, case_y_goal):
    current_position_x, current_position_y, current_position_rot = get_coordinate_aruco()
    position_case_x, position_case_y = convert_pixel_to_case(int(current_position_x), int(current_position_y))
    decal = 1
    #return position_case_x == case_x_goal and position_case_y == case_y_goal
    return position_case_x in range(case_x_goal - decal, case_x_goal + decal) and position_case_y in range(case_y_goal - decal, case_y_goal + decal)


def is_robot_too_far(case_x_goal, case_y_goal):
    current_position_x, current_position_y, rot = get_coordinate_aruco()
    position_case_x, position_case_y = convert_pixel_to_case(int(current_position_x), int(current_position_y))
    return math.sqrt((position_case_x - case_x_goal) * (position_case_x - case_x_goal)
                     + (position_case_y - case_y_goal) * (position_case_y - case_y_goal)) >= 2




if __name__ == "__main__":
     set_pixels_x(100)
     set_pixels_y(200)
     set_cells_x(10)
     set_cells_y(9)
     set_begin_point((100, 100))
     set_end_point((200, 400))
     tabX = discretization_X()
     tabY = discretization_Y()
     print(len(tabX), len(tabY))
     print(tabX)
     print(tabY)
     print(discretization_table())
     #print(convert_pixel_to_case(99, 90))
     #print(convert_case_to_pixel(7,9))
