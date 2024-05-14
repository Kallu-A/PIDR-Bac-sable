import math

# In order to convert pixels location to real world location thanks to the sizes and the coordinates
def px_to_mm3(coord_px, size_px, size_mm):
    coord_mm = (coord_px * size_mm) / size_px
    return coord_mm

# In order to convert pixels to millimeters through the resolution
def px_to_mm2(dist_px, res_px_mm_data):
    dist_mm = dist_px / res_px_mm_data
    return dist_mm

# In order to convert millimeters to pixels through the resolution
def mm_to_px2(dist_mm, res_ppmm_data):
    dist_px = dist_mm * res_ppmm_data
    return dist_px
    
# In order to get the camera resolution
def res_px_mm(px, mm):
    res = px/mm  
    return res  

# In order to estimate the resolution of the camera with measures
def estimation_cam():
    # 11mm seems to be the size of the sensor
    rayon = 5.5
    # formula to switch to the area
    area_capt = math.pi * (rayon**2)
    res_width = 1920
    res_height= 1080
    res_cam = (res_width * res_height) / area_capt
    return res_cam
    
def main():
    dist_px = 100
    dist_mm = 10
    res_px_mm_data = 0.1
    #px_to_mm3(coord_px, size_px, size_mm)
    print(str(dist_px) + " pixels valent " + str(px_to_mm2(dist_px, res_px_mm_data)) + " mm")
    print(str(dist_mm) + " mm valent " + str(mm_to_px2(dist_mm, res_px_mm_data)) + " pixels")
    
    """
    properties of the camera : 
    name : Logitech 180p
    acquisition in width : 1920px
    acquisition in height : 1080px
    """
    
    width_px = 1920
    height_px = 1080
    width_mm = 3401
    height_mm = 190
    
    """
    Resolutions can be different in width and height due to the number of pixels or their size, we have to check both
    """
    res_width = res_px_mm(width_px, width_mm)
    res_height = res_px_mm(height_px, height_mm)
    
    print("Résolution en largeur : " + str(res_width) + ", \nRésolution en hauteur : " + str(res_height))

    print("Estimation de la résolution de la caméra : " + str(estimation_cam()))
    
    
# adaptated part for Linux
if __name__ == '__main__':
    main()
    
