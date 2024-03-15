

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


def increment_robot_rotate(init, target):
    robot = Robot()
    robot.move_robot(-100, 100)


def decrement_robot_rotate(init,target):
    robot = Robot()
    robot.move_robot(100, -100)
