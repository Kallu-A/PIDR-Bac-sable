import time

from robot import Robot

if __name__ == '__main__':
    robot = Robot()
    robot.move_robot(100, 100)
    time.sleep(1)
    robot.stop_robot()

    prox_prev = 0
    def obs(node_id):
        global prox_prev
        prox = (robot.thymio["prox.horizontal"][5] - robot.thymio["prox.horizontal"][2]) // 10
        if prox != prox_prev:
            robot.move_robot(prox, prox)
            prox_prev = prox
        robot.disconnect_button_center()

    robot.add_obs(obs)
