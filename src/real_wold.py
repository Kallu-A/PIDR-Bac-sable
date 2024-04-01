from global_var import get_path_find

cellsX = 8
cellsY = 10
pixelsX = 100
pixelsY = 100

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
    tabX = discretization_X()
    tabY = discretization_Y()
    i = 0
    j = 0
    if x >= pixelsX:
        print("Pixel x not in the image")
        return

    if y >= pixelsY:
        print("Pixel y not in the image")
        return

    while not tabX[i] <= x < tabX[i + 1]:
        i += 1
        if x >= tabX[i] and tabX[i] == tabX[-1]:
            break

    while not tabY[j] <= y < tabY[j + 1]:
        j += 1
        if y >= tabY[j] and tabY[j] == tabY[-1]:
            break

    return i, j


def discretization_X():
    global cellsX, pixelsX
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
        if pixNb != pixelsX:
            tabX.append(pixNb)

    if pixelsX - tabX[-1] < cellsX:
        toAdd = 0
        for i in range(len(tabX)):
            tabX[i] += toAdd
            if toAdd < (pixelsX - tabX[-1]):
                toAdd += 1
    if tabX[-1] == pixelsX:
        tabX.pop()

    return tabX


def discretization_Y():
    global cellsY, pixelsY
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
        if pixNb != pixelsY:
            tabY.append(pixNb)

    if pixelsY - tabY[-1] < cellsY:
        toAdd = 0
        for i in range(len(tabY)):
            tabY[i] += toAdd
            if toAdd < (pixelsY - tabY[-1]):
                toAdd += 1
    if tabY[-1] == pixelsY:
        tabY.pop()
    return tabY


def discretization_table():
    global cellsX, pixelsX, cellsY, pixelsY
    # return the discretization grid initialized with 0
    tabX = discretization_X()
    tabY = discretization_Y()
    nbCellsX = len(tabX)
    nbCellsY = len(tabY)
    table = [[0 for col in range(nbCellsX)] for row in range(nbCellsY)]
    return table


if __name__ == "__main__":
     tabX = discretization_X()
     tabY = discretization_Y()
     print(tabX)
     print(tabY)
     print(discretization_table())
     print(convert_pixel_to_case(99, 90))
     print(convert_case_to_pixel(7,9))
