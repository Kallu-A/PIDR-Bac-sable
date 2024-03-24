from global_var import get_path_find


# convert the case i,j (in meters) in coordinate x,y in the image (pixel)
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

