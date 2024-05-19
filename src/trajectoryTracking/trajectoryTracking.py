from utility.movement_control import get_rotate_needed, rotate_robot
from robot import Robot
from dStarLite3d import main as algoTrajectory
import time


""" 
We need a function that will take the trajectory given
by the dStarLite3d code and follow it using Thymio functions.
""" 

def follow_trajectory(pathx, pathy, orientations):
    
    robot = Robot()
    currentOrientation = robot.get_initial_orientation(robot)
    
    """
    The trajectory will be a list of x_positions, y_positions and orientations.
    """
    
    for x, y, orientation in zip(pathx, pathy, orientations):
        rotate_robot(currentOrientation, orientation)
        currentOrientation = orientation
        
        robot.move_robot(robot,x,y)  # to be replaced with goStraightForward when operational
    
    """
    Once we have the coordinates one by one, we have to follow them.
    We first get the orientation needed,
    and then go the the x,y position.
    """
    
    return()



def goStraightForward(speedLeft, speedRight):
    # Connection to our robot through Thymio Serial Port in the "Robot" folder
    robot = Robot()
    
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
    
    time.sleep(3) # the robot will got straight forward for 3 secondes
 
 
 
 
    """
    Ces fonctions vont servir à retrouver chaque mouvement de rotation du Thymio
    en connaissant sa position initiale et finale dans le cadran.
    Il y a ainsi 7 positions possibles : 
    - 0 (0°)
    - 1 (45°)
    - 2 (90°)
    - 3 (135°)
    - 4 (180°)
    - 5 (-135°)
    - 6 (-90°)
    - 7 (-45°) 
    
    Pour le moment, les vitesses sont encore à vérifier manuellement.
    """
    
def turnOrientation0(initialOrientation):
    robot = Robot()
    
    if (initialOrientation == 0):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",0)
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",3)
        robot.set_var("motor.right.target",0)
       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",6)
        robot.set_var("motor.right.target",0)
        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",9)
        robot.set_var("motor.right.target",0)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",12)
        robot.set_var("motor.right.target",0)
        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",9)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",6)
        
    if (initialOrientation == -45):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",3)
        
    return()
    
    
    
    
def turnOrientation1(initialOrientation):
    robot = Robot()
    
    if (initialOrientation == 0):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",3)
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",0)
       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",3)
        robot.set_var("motor.right.target",0)
        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",6)
        robot.set_var("motor.right.target",0)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",9)
        robot.set_var("motor.right.target",0)
        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",12)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",9)
        
    if (initialOrientation == -45):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",6)
        
    return()




def turnOrientation2(initialOrientation):
    robot = Robot()
    
    if (initialOrientation == 0):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",6)
        
    if (initialOrientation == 45):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",3)
       
    if (initialOrientation == 90):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",0)
        
    if (initialOrientation == 135):
        robot.set_var("motor.left.target",3)
        robot.set_var("motor.right.target",0)
        
    if (initialOrientation == 180):
        robot.set_var("motor.left.target",6)
        robot.set_var("motor.right.target",0)
        
    if (initialOrientation == -135):
        robot.set_var("motor.left.target",9)
        robot.set_var("motor.right.target",0)
        
    if (initialOrientation == -90):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",6)
        
    if (initialOrientation == -45):
        robot.set_var("motor.left.target",0)
        robot.set_var("motor.right.target",12)
        
    return()




def main():
    
    """
    To make this work, we need to:
    - get the trajectory from the algorithm
    - call the follow up function
    """
    
    pathx, pathy, orientations = algoTrajectory()
    
    follow_trajectory(pathx, pathy, orientations)
    
    

if __name__ == "__main__":
    main()
    
        
        