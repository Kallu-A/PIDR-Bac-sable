import math

from robot import Robot

# init is the current degree of the robot
# target is the targeted degree

def rotate_robot(init, target):
    if target >= init:
        if  abs(target - init) <= 180:
            increment_robot_rotate(init, target)
            # robot turn trigo increment init degree value
        else:
            decrement_robot_rotate(init, target)
            # robot turn anti trigo decrement init degree value
    else:
        if abs(init - target) <= 180:
            decrement_robot_rotate(init, target)
            # robot turn anti trigo decrement init degree value
        else:
            increment_robot_rotate(init, target)
            # robot turn trigo increment init degree value


# return the degree needed for  the robot to be aligned with the target
def get_rotate_needed(r_x, r_y, d_x, d_y):
    oppose = -1 * (d_y - r_y)
    adjacent = -1 * (r_x - d_x)
    print("oppose: " + str(oppose))
    print("adjacent: " + str(adjacent))
    return (math.tan(oppose / adjacent))


# return the distance between the robot and the target
def calculate_distance(r_x, r_y, d_x, d_y):
    return ((r_x - d_x) ** 2 + (r_y - d_y) ** 2) ** 0.5


def increment_robot_rotate(init, target):
    robot = Robot()
    robot.move_robot(-100, 100)


def decrement_robot_rotate(init,target):
    robot = Robot()
    robot.move_robot(100, -100)
