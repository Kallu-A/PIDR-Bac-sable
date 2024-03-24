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
    oppose = abs(d_y - r_y)
    adjacent = abs(r_x - d_x)
    if r_x == d_x and r_y > d_y:
        return 90
    if r_x == d_x and r_y < d_y:
        return - 90
    if r_y == d_y and r_x > d_x:
        return 180
    if r_y == d_y and r_x < d_x:
        return 0
    if r_y == d_y and r_x == d_x:
        return 0
    val = math.degrees(math.atan(oppose / adjacent))

    # bottom right
    if r_x < d_x and d_y > r_y:
        val *= -1
    # top left
    elif r_x > d_x and r_y > d_y:
        val = (val - 180) * -1
    # bottom left
    elif r_x > d_x and r_y < d_y:
        val = val - 180

    return val


# return a point from a given angle and distance
def get_point_from_angle(x, y, angle, distance):
    angle = math.radians(angle)
    x += distance * math.cos(angle)
    y -= distance * math.sin(angle)
    return x, y


# return the distance between the robot and the target
def calculate_distance(r_x, r_y, d_x, d_y):
    return ((r_x - d_x) ** 2 + (r_y - d_y) ** 2) ** 0.5


def increment_robot_rotate(init, target):
    robot = Robot()
    robot.move_robot(-100, 100)


def decrement_robot_rotate(init,target):
    robot = Robot()
    robot.move_robot(100, -100)
