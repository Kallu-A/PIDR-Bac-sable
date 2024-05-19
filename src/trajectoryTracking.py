#from utility.movement_control import get_rotate_needed, rotate_robot
from robot import Robot
#from dStarLite import main as algoTrajectory
#from thymioserial import Thymio
import time


""" 
We need a function that will take the trajectory given
by the dStarLite3d code and follow it using Thymio functions.
""" 

def follow_trajectory(pathx, pathy, orientations):
    
    robot = Robot()
    currentOrientation = 0
    
    """
    The trajectory will be a list of x_positions, y_positions and orientations.
    """
    
    for x, y, orientation in zip(pathx, pathy, orientations):
        # We need to know in which position the robot needs to be between the 8 defined
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
            
        currentOrientation = orientation
        
        goStraightForward(robot,50,50) # to be replaced with goStraightForward when operational
    
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
    
    time.sleep(10) # the robot will go straight forward for 3 secondes
    
    robot.set_var("motor.left.target", 0)
    robot.set_var("motor.right.target", 0)
    
    #robot.disconnet()
    
 
 
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
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",30)
        robot.set_var("motor.right.target",-30)
       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",60)
        robot.set_var("motor.right.target",-60)
        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",90)
        robot.set_var("motor.right.target",-90)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",120)
        robot.set_var("motor.right.target",-120)
        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",-90)
        robot.set_var("motor.right.target",90)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",-60)
        robot.set_var("motor.right.target",60)
        
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
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",0)
       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",30)
        robot.set_var("motor.right.target",-30)
        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",60)
        robot.set_var("motor.right.target",-60)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",90)
        robot.set_var("motor.right.target",-90)
        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",-120)
        robot.set_var("motor.right.target",120)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",-90)
        robot.set_var("motor.right.target",90)
        
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
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",-30)
        robot.set_var("motor.right.target",30)
       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",0)
        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",30)
        robot.set_var("motor.right.target",-30)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",60)
        robot.set_var("motor.right.target",-60)
        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",90)
        robot.set_var("motor.right.target",-90)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",-120)
        robot.set_var("motor.right.target",120)
        
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
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",-60)
        robot.set_var("motor.right.target",60)
       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",-30)
        robot.set_var("motor.right.target",30)
        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",0)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",30)
        robot.set_var("motor.right.target",-30)
        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",60)
        robot.set_var("motor.right.target",-60)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",90)
        robot.set_var("motor.right.target",-90)
        
    if (initialOrientation == -45):
        robot.set_var("motor.left.target",120)
        robot.set_var("motor.right.target",-120)
        
    time.sleep(4)
          
    robot.set_var("motor.left.target", 0)
    robot.set_var("motor.right.target", 0)
    
    #robot.disconnet()
    
    return()




def turnOrientation4(robot,initialOrientation):
    #robot = Robot()
    
    if (initialOrientation == 0):
        robot.set_var("motor.left.target",-120)
        robot.set_var("motor.right.target",120)
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",-90)
        robot.set_var("motor.right.target",90)
       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",-60)
        robot.set_var("motor.right.target",60)
        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",-30)
        robot.set_var("motor.right.target",30)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",0)
        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",30)
        robot.set_var("motor.right.target",-30)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",60)
        robot.set_var("motor.right.target",-60)
        
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
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",-120)
        robot.set_var("motor.right.target",120)
       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",-90)
        robot.set_var("motor.right.target",90)
        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",-60)
        robot.set_var("motor.right.target",60)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",-30)
        robot.set_var("motor.right.target",30)
        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",0)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",30)
        robot.set_var("motor.right.target",-30)
        
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
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",90)
        robot.set_var("motor.right.target",-90)
       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",-120)
        robot.set_var("motor.right.target",120)
        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",-90)
        robot.set_var("motor.right.target",90)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",-60)
        robot.set_var("motor.right.target",60)
        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",-30)
        robot.set_var("motor.right.target",30)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",0)
        
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
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",60)
        robot.set_var("motor.right.target",-60)
       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",90)
        robot.set_var("motor.right.target",-90)
        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",-120)
        robot.set_var("motor.right.target",120)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",-90)
        robot.set_var("motor.right.target",90)
        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",-60)
        robot.set_var("motor.right.target",60)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",-30)
        robot.set_var("motor.right.target",30)
        
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
    pathx = [1, 2, 3, 4]
    pathy = [0, 1, 1, 2]
    orientations = [-90, -135, 180, 0]
    follow_trajectory(pathx, pathy, orientations)
    
    ''' test of several actions outside the follow_trajectory main one : working
    robot = Robot()
    goStraightForward(robot,50,50) # opérationnel
    turnOrientation6(robot,180)
    goStraightForward(robot,50,50)
    turnOrientation3(robot,-90)
    robot.disconnet()
    '''
    
    

if __name__ == "__main__":
    main()
    
        
        