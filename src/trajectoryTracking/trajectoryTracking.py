from utility.movement_control import get_rotate_needed, rotate_robot
from robot import Robot
from dStarLite3d import main


""" 
We need a function that will take the trajectory given
by the dStarLite3d code and follow it using Thymio functions.
""" 

def follow_trajectory(pathx, pathy, orientations):
    
    robot = Robot()
    currentOrientation = robot.getOrientation()
    
    """
    The trajectory will be a list of x_positions, y_positions and orientations.
    """
    
    for x, y, orientation in zip(pathx, pathy, orientations):
        rotate_robot(currentOrientation, orientation)
        currentOrientation = orientation
        
        robot.move_robot(robot,x,y)
    
    """
    Once we have the coordinates one by one, we have to follow them.
    We first get the orientation needed,
    and then go the the x,y position.
    """
    
    return()



def main():
    
    """
    To make this work, we need to:
    - get the trajectory from the algorithm
    - call the follow up function
    """
    
    pathx, pathy, orientations = main()
    
    follow_trajectory(pathx, pathy, orientations)
    
    
        
        