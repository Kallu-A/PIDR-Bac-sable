#from utility.movement_control import get_rotate_needed, rotate_robot
from robot import Robot
#from dStarLite import main as algoTrajectory
#from thymioserial import Thymio
import time

from global_var import get_coordinate_aruco, set_coordinate_aruco

""" 
We need a function that will take the trajectory given
by the dStarLite3d code and follow it using Thymio functions.
""" 

def follow_trajectory(pathx, pathy, orientations, size):
    robot = Robot()
    currentOrientation = get_coordinate_aruco()[2]
    #currentOrientation = 0
    #turnOrientation(robot,orientations[0],currentOrientation)
    print("currentOrientation : ",currentOrientation)
    print("pathx : ",pathx)
    print("pathy : ",pathy)
    print("orientations : ",orientations)
    print("size : ",size)

    """
    The trajectory will be a list of x_positions, y_positions and orientations.
    """
    
    for x, y, orientation in zip(pathx, pathy, orientations):
        # We need to know in which position the robot needs to be between the 8 defined
        '''
        if (orientation == 0):
            turnOrientation0(robot,currentOrientation)
            
        if (orientation == 45):
            turnOrientation1(robot,currentOrientation)
            
        if (orientation == 90):
            turnOrientation2(robot,currentOrientation)
            
        if (orientation == 135):
            turnOrientation3(robot,currentOrientation)
            
        if (orientation == 180):
            turnOrientation4(robot,currentOrientation) 
            
        if (orientation == -135):
            turnOrientation5(robot,currentOrientation)  
            
        if (orientation == -90):
            turnOrientation6(robot,currentOrientation)
            
        if (orientation == -45):
            turnOrientation7(robot,currentOrientation)
        '''
        turnOrientation(robot,orientation,currentOrientation)
        
        currentOrientation = orientation
        get_coordinate_aruco()
        goStraightForward(robot,60,60) # to be replaced with goStraightForward when operational
    
    """
    Once we have the coordinates one by one, we have to follow them.
    We first get the orientation needed,
    and then go the the x,y position.
    """
    
    robot.disconnet()
    
    return()



def goStraightForward(robot,speedLeft, speedRight):
    # Connection to our robot through Thymio Serial Port in the "Robot" folder
    #robot = Robot()
    
    """ 
    We have to give different speeds to right and left motors in case they do not work the same way.
    The test will be made with a straight line.
    Different speeds could also make the robot rotate with a curve instead of straight lines and a 
    fixed rotation.
    """
    robot.set_var("motor.left.target", speedLeft)
    robot.set_var("motor.right.target", speedRight)
    
    """
    We can define :
    - x,y positions to go to with a straight line
    - a time for the duration of the program
    """
    
    time.sleep(0.5) # the robot will go straight forward for 3 secondes
    
    robot.set_var("motor.left.target", 0)
    robot.set_var("motor.right.target", 0)
    
    #robot.disconnet()
    return()
    
 
def turnOrientation(robot,goalOrientation,currentOrientation):
    #robot = Robot()
    
    if (goalOrientation==-135):
        goalOrientation=225
    if (goalOrientation==-90):
        goalOrientation=270
    if (goalOrientation==-45):
        goalOrientation=315
        
    if (currentOrientation==-135):
        currentOrientation=225
    if (currentOrientation==-90):
        currentOrientation=270
    if (currentOrientation==-45):
        currentOrientation=315
        
    if (goalOrientation-currentOrientation == 0):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",0)
        
    if (goalOrientation-currentOrientation == 45 or goalOrientation-currentOrientation == -315):
        robot.set_var("motor.left.target",-30)
        robot.set_var("motor.right.target",30)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (goalOrientation-currentOrientation == -45 or goalOrientation-currentOrientation == 315):
        robot.set_var("motor.left.target",27)
        robot.set_var("motor.right.target",-27)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
    
    if (goalOrientation-currentOrientation == 90 or goalOrientation-currentOrientation == -270):
        robot.set_var("motor.left.target",-60)
        robot.set_var("motor.right.target",60)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (goalOrientation-currentOrientation == -90 or goalOrientation-currentOrientation == 270):
        robot.set_var("motor.left.target",50)
        robot.set_var("motor.right.target",-50)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (goalOrientation-currentOrientation == 135 or goalOrientation-currentOrientation == -225):
        robot.set_var("motor.left.target",-90)
        robot.set_var("motor.right.target",90)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
    
    if (goalOrientation-currentOrientation == -135 or goalOrientation-currentOrientation == 225):
        robot.set_var("motor.left.target",82)
        robot.set_var("motor.right.target",-82)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (goalOrientation-currentOrientation == 180 or goalOrientation-currentOrientation == -180):
        robot.set_var("motor.left.target",-150)
        robot.set_var("motor.right.target",150)
        time.sleep(3)
        robot.set_var("motor.left.target",-22)
        robot.set_var("motor.right.target",22)
        time.sleep(1)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
            
        
    #robot.disconnet()
    
    return()


"""
    These functions will give us the rotation mouvements of Thymio
    knowing his initial and final position in the dial.
    There are seven available positions : 
    - 0 (0°)
    - 1 (45°)
    - 2 (90°)
    - 3 (135°)
    - 4 (180°)
    - 5 (-135°)
    - 6 (-90°)
    - 7 (-45°) 
    
    Currently, the speeds still have to be checked with a test.
    Hint : the time.sleep could be inside each variation so that the robot sppeds more and the beginning
    and less in the end so that it stops correctly.
"""
    
def turnOrientation0(robot,initialOrientation):
    #robot = Robot()
    
    if (initialOrientation == 0):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",0)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",30)
        robot.set_var("motor.right.target",-30)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",60)
        robot.set_var("motor.right.target",-60)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",90)
        robot.set_var("motor.right.target",-90)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",150)
        robot.set_var("motor.right.target",-150)
        time.sleep(3)
        robot.set_var("motor.left.target",20)
        robot.set_var("motor.right.target",-20)
        time.sleep(1)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",-90)
        robot.set_var("motor.right.target",90)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",-60)
        robot.set_var("motor.right.target",60)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -45):
        robot.set_var("motor.left.target",-30)
        robot.set_var("motor.right.target",30)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    #robot.disconnet()
    
    return()
    
    
    
    
def turnOrientation1(robot,initialOrientation):
    #robot = Robot()
    
    if (initialOrientation == 0):
        robot.set_var("motor.left.target",-30)
        robot.set_var("motor.right.target",30)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",0)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",30)
        robot.set_var("motor.right.target",-30)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",60)
        robot.set_var("motor.right.target",-60)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",90)
        robot.set_var("motor.right.target",-90)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",150)
        robot.set_var("motor.right.target",-150)
        time.sleep(3)
        robot.set_var("motor.left.target",20)
        robot.set_var("motor.right.target",-20)
        time.sleep(1)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",-90)
        robot.set_var("motor.right.target",90)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -45):
        robot.set_var("motor.left.target",-60)
        robot.set_var("motor.right.target",60)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
                   
    #robot.disconnet()
    
    return()




def turnOrientation2(robot,initialOrientation):
    #robot = Robot()
    
    if (initialOrientation == 0):
        robot.set_var("motor.left.target",-60)
        robot.set_var("motor.right.target",60)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",-30)
        robot.set_var("motor.right.target",30)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",0)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",30)
        robot.set_var("motor.right.target",-30)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",60)
        robot.set_var("motor.right.target",-60)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",90)
        robot.set_var("motor.right.target",-90)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",150)
        robot.set_var("motor.right.target",-150)
        time.sleep(3)
        robot.set_var("motor.left.target",20)
        robot.set_var("motor.right.target",-20)
        time.sleep(1)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -45):
        robot.set_var("motor.left.target",-90)
        robot.set_var("motor.right.target",90)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
                     
    #robot.disconnet()
    
    return()




def turnOrientation3(robot,initialOrientation):
    #robot = Robot()
    
    if (initialOrientation == 0):
        robot.set_var("motor.left.target",-90)
        robot.set_var("motor.right.target",90)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",-60)
        robot.set_var("motor.right.target",60)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",-30)
        robot.set_var("motor.right.target",30)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",0)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",30)
        robot.set_var("motor.right.target",-30)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",60)
        robot.set_var("motor.right.target",-60)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",90)
        robot.set_var("motor.right.target",-90)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -45):
        robot.set_var("motor.left.target",150)
        robot.set_var("motor.right.target",-150)
        time.sleep(3)
        robot.set_var("motor.left.target",20)
        robot.set_var("motor.right.target",-20)
        time.sleep(1)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
               
    #robot.disconnet()
    
    return()




def turnOrientation4(robot,initialOrientation):
    #robot = Robot()
    
    if (initialOrientation == 0):
        robot.set_var("motor.left.target",150)
        robot.set_var("motor.right.target",-150)
        time.sleep(3)
        robot.set_var("motor.left.target",20)
        robot.set_var("motor.right.target",-20)
        time.sleep(1)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",-90)
        robot.set_var("motor.right.target",90)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",-60)
        robot.set_var("motor.right.target",60)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",-30)
        robot.set_var("motor.right.target",30)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",0)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",30)
        robot.set_var("motor.right.target",-30)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",60)
        robot.set_var("motor.right.target",-60)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -45):
        robot.set_var("motor.left.target",90)
        robot.set_var("motor.right.target",-90)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
             
    #robot.disconnet()
    
    return()




def turnOrientation5(robot,initialOrientation):
    #robot = Robot()
    
    if (initialOrientation == 0):
        robot.set_var("motor.left.target",90)
        robot.set_var("motor.right.target",-90)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",150)
        robot.set_var("motor.right.target",-150)
        time.sleep(3)
        robot.set_var("motor.left.target",20)
        robot.set_var("motor.right.target",-20)
        time.sleep(1)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",-90)
        robot.set_var("motor.right.target",90)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",-60)
        robot.set_var("motor.right.target",60)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",-30)
        robot.set_var("motor.right.target",30)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",0)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",30)
        robot.set_var("motor.right.target",-30)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -45):
        robot.set_var("motor.left.target",60)
        robot.set_var("motor.right.target",-60)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)                 
    
    #robot.disconnet()
     
    return()




def turnOrientation6(robot,initialOrientation):
    #robot = Robot()
    
    if (initialOrientation == 0):
        robot.set_var("motor.left.target",60)
        robot.set_var("motor.right.target",-60)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",90)
        robot.set_var("motor.right.target",-90)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",150)
        robot.set_var("motor.right.target",-150)
        time.sleep(3)
        robot.set_var("motor.left.target",20)
        robot.set_var("motor.right.target",-20)
        time.sleep(1)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",-90)
        robot.set_var("motor.right.target",90)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",-60)
        robot.set_var("motor.right.target",60)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",-30)
        robot.set_var("motor.right.target",30)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",0)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
        
    if (initialOrientation == -45):
        robot.set_var("motor.left.target",30)
        robot.set_var("motor.right.target",-30)
        time.sleep(4)
        robot.set_var("motor.left.target", 0)
        robot.set_var("motor.right.target", 0)
                  
    #robot.disconnet()
    
    return()




def turnOrientation7(robot,initialOrientation):
    #robot = Robot()
    
    if (initialOrientation == 0):
        robot.set_var("motor.left.target",30)
        robot.set_var("motor.right.target",-30)
        time.sleep(4)
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",60)
        robot.set_var("motor.right.target",-60)
        time.sleep(4)

       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",90)
        robot.set_var("motor.right.target",-90)
        time.sleep(4)

        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",150)
        robot.set_var("motor.right.target",-150)
        time.sleep(3)
        robot.set_var("motor.left.target",20)
        robot.set_var("motor.right.target",-20)
        time.sleep(1)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",-90)
        robot.set_var("motor.right.target",90)
        time.sleep(4)

        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",-60)
        robot.set_var("motor.right.target",60)
        time.sleep(4)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",-30)
        robot.set_var("motor.right.target",30)
        time.sleep(4)

    if (initialOrientation == -45):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",0)
        time.sleep(4)
                 
    robot.set_var("motor.left.target", 0)
    robot.set_var("motor.right.target", 0)
    
    #robot.disconnet()
    
    return()




def main():
    
    """
    To make this work, we need to:
    - get the trajectory from the algorithm
    - call the follow up function
    """
    
    #pathx, pathy, orientations = algoTrajectory()
    pathx = [77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67, 66, 65, 64, 63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12]
    pathy = [39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 54, 54, 54, 54, 54, 54, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72]
    orientations = [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, -135, -135, -135, -135, -135, -135, -135, -135, -135, -135, -135, -135, -135, -135, -135, 180, 180, 180, 180, 180, 180, 180, -135, -135, -135, -135, -135, -135, -135, -135, -135, -135, -135, -135, -135, -135, -135, -135, -135, -135, -135]
    #set_coordinate_aruco((2, 2, 20))
    follow_trajectory(pathx, pathy, orientations)
    
    ''' test of several actions outside the follow_trajectory main one : working
    robot = Robot()
    goStraightForward(robot,50,50) # opérationnel
    turnOrientation7(robot,135)
    goStraightForward(robot,50,50)
    turnOrientation5(robot,-45)
    robot.disconnet()
    '''
    
    

if __name__ == "__main__":
    main()
    
        
        