"""
D* Lite grid planning
author: vss2sn (28676655+vss2sn@users.noreply.github.com)
Link to papers:
D* Lite (Link: http://idm-lab.org/bib/abstracts/papers/aaai02b.pd)
Improved Fast Replanning for Robot Navigation in Unknown Terrain
(Link: http://www.cs.cmu.edu/~maxim/files/dlite_icra02.pdf)
Implemented maintaining similarity with the pseudocode for understanding.
Code can be significantly optimized by using a priority queue for U, etc.
Avoiding additional imports based on repository philosophy.
"""
import math
import matplotlib.pyplot as plt
import random
import numpy as np
from global_var import get_obstacles, set_obstacles, get_coordinate_aruco, get_destination, set_destination, set_coordinate_aruco, set_path_find, get_path_find, set_cells_y, set_pixels_y, set_pixels_x, set_cells_x, get_pixels_xy, get_cells_xy
from real_wold import convert_pixel_to_case
from queue import PriorityQueue
import itertools
from threshold import threshold_from_frame, get_obstacles_position_grid_from_frame, get_obstacles_position_grid_from_frame_test
import cv2

show_animation = False
pause_time = 1
p_create_random_obstacle = 0


class Node:
    def __init__(self, x: int = 0, y: int = 0, theta: int = 0, cost: float = 0.0):
        self.x = x
        self.y = y
        self.theta = theta
        self.cost = cost


def add_coordinates(node1: Node, node2: Node):
    new_node = Node()
    new_node.x = node1.x + node2.x
    new_node.y = node1.y + node2.y
    new_node.theta = add_angle(node1.theta, node2.theta)
    new_node.cost = node1.cost + node2.cost
    return new_node


def compare_coordinates(node1: Node, node2: Node):
    return node1.x == node2.x and node1.y == node2.y and node1.theta == node2.theta

def calculate_cost(node1: Node, node2: Node):


    #similarity cos between node1 and node2
    # 1 : proportional vector
    # 0 : orthogonal vector
    # -1 : opposed vector

    # scalar = node1.x * node2.x + node1.y * node2.y + node1.theta * node2.theta #scalar between node1 and node2
    # magnitude1 = math.sqrt(node1.x * node1.x + node1.y * node1.y + node1.theta * node1.theta) #magnitude of (0,0,1)
    # magnitude2 = math.sqrt(node2.x * node2.x + node2.y * node2.y + node2.theta * node2.theta) #magnitude of (xb, yb, thetab)
    scalar = 1 * 1 + 1 * 1 + node1.theta * node2.theta #scalar between node1 and node2
    magnitude1 = math.sqrt(1 * 1 + 1 * 1 + node1.theta * node1.theta) #magnitude of (0,0,1)
    magnitude2 = math.sqrt(1 * 1 + 1 * 1 + node2.theta * node2.theta) #magnitude of (xb, yb, thetab)
    cos_similarity = scalar/(magnitude1*magnitude2)
    return (cos_similarity - 1) * -1 #between 0 and 2 : 2 (opposed), 1 (orthogonal), 0 (proportional)

    # return round(abs(node1.theta - node2.theta) + math.sqrt((node2.x-node1.x)**2 + (node2.y-node1.y)**2) * 0.1, 5)


def calculate_angle(theta_start, theta_goal):
    #angle deplacements between theta_start and theta_goal
    if theta_start == theta_goal:
        return 0
    if theta_start > theta_goal:
        if theta_goal > 0:
            return theta_goal - theta_start
        if theta_goal == 0:
            return theta_start
        if theta_goal < 0:
            if theta_goal - theta_start > 4:
                return 8 - (theta_goal - theta_start)
            if theta_goal - theta_start < -4:
                return 8 - abs(theta_goal - theta_start)
            if abs(theta_goal - theta_start) == 4:
                return 4
            if abs(theta_goal - theta_start) < 4:
                return theta_goal - theta_start
    if theta_start < theta_goal:
        if theta_start >= 0:
            return theta_goal - theta_start
        if theta_start < 0:
            if abs(theta_goal - theta_start) > 4:
                return (theta_goal - theta_start) - 8
            if abs(theta_goal - theta_start) == 4:
                return 4
            if abs(theta_goal - theta_start) < 4:
                return theta_goal - theta_start

def add_angle(theta1, theta2):
    theta_add = theta1 + theta2
    if -3 <= theta_add < 5:
        return theta_add
    if theta_add < -3:
        if theta_add == -4:
            return -theta_add
        return theta_add + 8
    if theta_add >= 5:
        return theta_add - 8



class DStarLite:
    # Please adjust the heuristic function (h) if you change the list of
    # possible motions


    def __init__(self, ox: list, oy: list):
        # Ensure that within the algorithm implementation all node coordinates
        # are indices in the grid and extend
        self.x_max, self.y_max = get_cells_xy()
        self.obstacles = []

        # for x, y in zip(ox, oy):
        #     self.obstacles.append(Node(x=x, y=y, theta=i) for i in [-3, -2, -1, 0, 1, 2, 3, 4])
        self.obstacles = [[Node(x, y, i) for i in [-3, -2, -1, 0, 1, 2, 3, 4]]
                          for x, y in zip(ox, oy)]
        self.obstacles = list(itertools.chain(*self.obstacles))

        self.obstacles_xyt = np.array(
            [[obstacle.x, obstacle.y, obstacle.theta] for obstacle in self.obstacles]
        )
        #print(self.obstacles_xyt)
        self.start = Node(0, 0, 0)
        self.goal = Node(0, 0, 0)
        self.U = list()  # type: ignore
        self.km = 0.0
        self.kold = 0.0
        self.rhs = self.create_grid(float("inf"))
        self.g = self.create_grid(float("inf"))
        self.detected_obstacles_xyt = np.empty((0, 3))
        self.xy = np.empty((0, 3))
        if show_animation:
            self.detected_obstacles_for_plotting_x = list()  # type: ignore
            self.detected_obstacles_for_plotting_y = list()  # type: ignore
        self.initialized = False

    def create_grid(self, val: float):
        return np.full((self.x_max, self.y_max, 8), val)

    def is_obstacle(self, node: Node):
        x = np.array([node.x])
        y = np.array([node.y])
        theta = np.array([node.theta])
        obstacle_x_equal = self.obstacles_xyt[:, 0] == x
        obstacle_y_equal = self.obstacles_xyt[:, 1] == y
        is_in_obstacles = (obstacle_x_equal & obstacle_y_equal).any()

        is_in_detected_obstacles = False
        if self.detected_obstacles_xyt.shape[0] > 0:
            is_x_equal = self.detected_obstacles_xyt[:, 0] == x
            is_y_equal = self.detected_obstacles_xyt[:, 1] == y
            is_in_detected_obstacles = (is_x_equal & is_y_equal).any()

        return is_in_obstacles or is_in_detected_obstacles

    def c(self, node1: Node, node2: Node):
        if self.is_obstacle(node2):
            # Attempting to move from or to an obstacle
            return math.inf

        # new_node = Node(node1.x-node2.x, node1.y-node2.y, calculate_angle(node1.theta, node2.theta),
        #                 calculate_cost(node1, node2))
        # detected_motion = list(filter(lambda motion:
        #                               compare_coordinates(motion, new_node),
        #                               self.motions))
        return calculate_cost(node1, node2)

    def h(self, s: Node):
        # Cannot use the 2nd euclidean norm as this might sometimes generate
        # heuristics that overestimate the cost, making them inadmissible,
        # due to rounding errors etc (when combined with calculate_key)
        # To be admissible heuristic should
        # never overestimate the cost of a move
        # hence not using the line below
        # return math.hypot(self.start.x - s.x, self.start.y - s.y)

        # Below is the same as 1; modify if you modify the cost of each move in
        # motion
        return 0

    def calculate_key(self, s: Node):
        return (min(self.g[s.x][s.y][s.theta], self.rhs[s.x][s.y][s.theta]) + self.h(s)
                + self.km, min(self.g[s.x][s.y][s.theta], self.rhs[s.x][s.y][s.theta]))

    def is_valid(self, node: Node):
        if 0 <= node.x < self.x_max and 0 <= node.y < self.y_max and -3 <= node.theta < 5:
            return True
        return False


    def get_neighbours(self, u: Node):
        possible_motions = [
        #we are in a 3 dimensions world with x = [-1, 0, 1] y = [-1, 0, 1] theta = [-3, -2, -1, 0, 1, 2, 3, 4]
        #Node(0, 0, 0, calculate_cost(0, 0, 0)),
        # Node(0, 0, 1, calculate_cost(0, 0, 1)),
        # Node(0, 0, 2, calculate_cost(0, 0, 2)),
        # Node(0, 0, 3, calculate_cost(0, 0, 3)),
        # Node(0, 0, 4, calculate_cost(0, 0, 4)),
        # Node(0, 0, -1, calculate_cost(0, 0, 1)),
        # Node(0, 0, -2, calculate_cost(0, 0, 2)),
        # Node(0, 0, -3, calculate_cost(0, 0, 3)),

            Node(1, 0, 0, 0),
            Node(1, 0, 1, 0),
            Node(1, 0, 2, 0),
            Node(1, 0, 3, 0),
            Node(1, 0, 4, 0),
            Node(1, 0, -1, 0),
            Node(1, 0, -2, 0),
            Node(1, 0, -3, 0),

            Node(0, 1, 0, 0),
            Node(0, 1, 1, 0),
            Node(0, 1, 2, 0),
            Node(0, 1, 3, 0),
            Node(0, 1, 4, 0),
            Node(0, 1, -1, 0),
            Node(0, 1, -2, 0),
            Node(0, 1, -3, 0),

            Node(-1, 0, 0, 0),
            Node(-1, 0, 1, 0),
            Node(-1, 0, 2, 0),
            Node(-1, 0, 3, 0),
            Node(-1, 0, 4, 0),
            Node(-1, 0, -1, 0),
            Node(-1, 0, -2, 0),
            Node(-1, 0, -3, 0),

            Node(0, -1, 0, 0),
            Node(0, -1, 1, 0),
            Node(0, -1, 2, 0),
            Node(0, -1, 3, 0),
            Node(0, -1, 4, 0),
            Node(0, -1, -1, 0),
            Node(0, -1, -2, 0),
            Node(0, -1, -3, 0),

            Node(1, 1, 0, 0),
            Node(1, 1, 1, 0),
            Node(1, 1, 2, 0),
            Node(1, 1, 3, 0),
            Node(1, 1, 4, 0),
            Node(1, 1, -1, 0),
            Node(1, 1, -2, 0),
            Node(1, 1, -3, 0),

            Node(1, -1, 0, 0),
            Node(1, -1, 1, 0),
            Node(1, -1, 2, 0),
            Node(1, -1, 3, 0),
            Node(1, -1, 4, 0),
            Node(1, -1, -1, 0),
            Node(1, -1, -2, 0),
            Node(1, -1, -3, 0),

            Node(-1, 1, 0, 0),
            Node(-1, 1, 1, 0),
            Node(-1, 1, 2, 0),
            Node(-1, 1, 3, 0),
            Node(-1, 1, 4, 0),
            Node(-1, 1, -1, 0),
            Node(-1, 1, -2, 0),
            Node(-1, 1, -3, 0),

            Node(-1, -1, 0, 0),
            Node(-1, -1, 1, 0),
            Node(-1, -1, 2, 0),
            Node(-1, -1, 3, 0),
            Node(-1, -1, 4, 0),
            Node(-1, -1, -1, 0),
            Node(-1, -1, -2, 0),
            Node(-1, -1, -3, 0),

        ]

        neighbours = []
        for node in possible_motions:
            neigh = Node(u.x + node.x, u.y + node.y, add_angle(u.theta, node.theta), calculate_cost(u, add_coordinates(u, node)))
            if self.is_valid(neigh) and (neigh not in neighbours):
                neighbours.append(neigh)

        return neighbours

        # return [add_coordinates(u, motion) for motion in self.motions
        #         if self.is_valid(add_coordinates(u, motion))]

    def pred(self, u: Node):
        # Grid, so each vertex is connected to the ones around it
        return self.get_neighbours(u)

    def succ(self, u: Node):
        # Grid, so each vertex is connected to the ones around it
        return self.get_neighbours(u)

    def initialize(self, start: Node, goal: Node):
        self.start.x = start.x
        self.start.y = start.y
        self.start.theta = start.theta
        self.goal.x = goal.x
        self.goal.y = goal.y
        self.goal.theta = goal.theta
        if not self.initialized:
            self.initialized = True
            print('Initializing')
            self.U = list()  # Would normally be a priority queue : PriorityQueue()
            self.km = 0.0
            self.rhs = self.create_grid(math.inf)
            self.g = self.create_grid(math.inf)
            self.rhs[self.goal.x][self.goal.y][self.goal.theta] = 0
            self.U.append((self.goal, self.calculate_key(self.goal))) # U = [(node, key), ...]
            self.detected_obstacles_xyt = np.empty((0, 3))
            print('Initializing finished')

    def update_vertex(self, u: Node):
        if not compare_coordinates(u, self.goal):
            self.rhs[u.x][u.y][u.theta] = min([self.c(u, sprime) +
                                      self.g[sprime.x][sprime.y][sprime.theta]
                                      for sprime in self.succ(u)])
        if any([compare_coordinates(u, node) for node, key in self.U]):
            self.U = [(node, key) for node, key in self.U
                      if not compare_coordinates(node, u)]
            self.U.sort(key=lambda x: x[1])
        if self.g[u.x][u.y][u.theta] != self.rhs[u.x][u.y][u.theta]:
            self.U.append((u, self.calculate_key(u)))
            self.U.sort(key=lambda x: x[1])

    def compare_keys(self, key_pair1: tuple[float, float],
                     key_pair2: tuple[float, float]):
        return key_pair1[0] < key_pair2[0] or \
               (key_pair1[0] == key_pair2[0] and key_pair1[1] < key_pair2[1])

    def compute_shortest_path(self):
        self.U.sort(key=lambda x: x[1])
        has_elements = len(self.U) > 0
        start_key_not_updated = self.compare_keys(
            self.U[0][1], self.calculate_key(self.start)
        )
        #local inconsistency
        rhs_not_equal_to_g = self.rhs[self.start.x][self.start.y][self.start.theta] != \
            self.g[self.start.x][self.start.y][self.start.theta]

        while has_elements and start_key_not_updated or rhs_not_equal_to_g:
            self.kold = self.U[0][1]
            u = self.U[0][0]
            self.U.pop(0)
            if self.compare_keys(self.kold, self.calculate_key(u)):
                self.U.append((u, self.calculate_key(u)))
                self.U.sort(key=lambda x: x[1])
            elif self.g[u.x][u.y][u.theta] > self.rhs[u.x][u.y][u.theta]:
                self.g[u.x][u.y][u.theta] = self.rhs[u.x][u.y][u.theta]
                for s in self.pred(u):
                    self.update_vertex(s)
            else:
                self.g[u.x][u.y][u.theta] = math.inf
                for s in self.pred(u) + [u]:
                    self.update_vertex(s)

            self.U.sort(key=lambda x: x[1])
            start_key_not_updated = self.compare_keys(
                self.U[0][1], self.calculate_key(self.start)
            )
            rhs_not_equal_to_g = self.rhs[self.start.x][self.start.y][self.start.theta] != \
                self.g[self.start.x][self.start.y][self.start.theta]



        # print("while out")
        # print("has_elements : ", has_elements)
        # print("rhs_not_equal_to_g : ", rhs_not_equal_to_g)
        # print("start_key_not_updated : ", start_key_not_updated)



    def detect_changes(self):
        changed_vertices = list()
        if len(self.spoofed_obstacles) > 0:
            for spoofed_obstacle in self.spoofed_obstacles[0]:
                if compare_coordinates(spoofed_obstacle, self.start) or \
                   compare_coordinates(spoofed_obstacle, self.goal):
                    continue
                changed_vertices.append(spoofed_obstacle)
                self.detected_obstacles_xyt = np.concatenate(
                    (
                        self.detected_obstacles_xyt,
                        [[spoofed_obstacle.x, spoofed_obstacle.y, spoofed_obstacle.theta]]
                    )
                )
                if show_animation:
                    self.detected_obstacles_for_plotting_x.append(
                        spoofed_obstacle.x)
                    self.detected_obstacles_for_plotting_y.append(
                        spoofed_obstacle.y)
                    plt.plot(self.detected_obstacles_for_plotting_x,
                             self.detected_obstacles_for_plotting_y, ".k")
                    plt.pause(pause_time)
            self.spoofed_obstacles.pop(0)

        return changed_vertices

    def compute_current_path(self):
        path = list()
        current_point = Node(self.start.x, self.start.y, self.start.theta)
        while not compare_coordinates(current_point, self.goal):
            path.append(current_point)
            current_point = min(self.succ(current_point),
                                key=lambda sprime:
                                self.c(current_point, sprime) +
                                self.g[sprime.x][sprime.y][sprime.theta])
        path.append(self.goal)
        return path

    def compare_paths(self, path1: list, path2: list):
        if len(path1) != len(path2):
            return False
        for node1, node2 in zip(path1, path2):
            if not compare_coordinates(node1, node2):
                return False
        return True

    def display_path(self, path: list, colour: str, alpha: float = 1.0):
        px = [(node.x) for node in path]
        py = [(node.y) for node in path]
        drawing = plt.plot(px, py, colour, alpha=alpha)
        plt.pause(pause_time)
        return drawing

    def main(self, start: Node, goal: Node,
             spoofed_ox: list, spoofed_oy: list):
        self.spoofed_obstacles = [[Node(x,
                                        y)
                                   for x, y in zip(rowx, rowy)]
                                  for rowx, rowy in zip(spoofed_ox, spoofed_oy)
                                  ]
        pathx = []
        pathy = []
        paththeta = []
        self.initialize(start, goal)
        last = self.start
        self.compute_shortest_path()
        pathx.append(self.start.x)
        pathy.append(self.start.y)
        paththeta.append(self.start.theta)
        path = []
        for i in range(len(pathx)):
            path.append((pathx[i], pathy[i], paththeta[i]))
        set_path_find(path)


        # if show_animation:
        #     current_path = self.compute_current_path()
        #     previous_path = current_path.copy()
        #     previous_path_image = self.display_path(previous_path, ".c",
        #                                             alpha=0.3)
        #     current_path_image = self.display_path(current_path, ".c")

        while not compare_coordinates(self.goal, self.start):
            if self.g[self.start.x][self.start.y][self.start.theta] == math.inf:
                print("No path possible")
                return False, pathx, pathy

            self.start = min(self.succ(self.start),
                             key=lambda sprime:
                             self.c(self.start, sprime) +
                             self.g[sprime.x][sprime.y][sprime.theta])

            pathx.append(self.start.x)
            pathy.append(self.start.y)
            paththeta.append(self.start.theta)
            if show_animation:
                current_path.pop(0)
                plt.plot(pathx, pathy, "-r")
                plt.pause(pause_time)
            changed_vertices = self.detect_changes()
            if len(changed_vertices) != 0:
                print("New obstacle detected")
                self.km += self.h(last)
                last = self.start
                for u in changed_vertices:
                    if compare_coordinates(u, self.start):
                        continue
                    self.rhs[u.x][u.y][u.theta] = math.inf
                    self.g[u.x][u.y][u.theta] = math.inf
                    self.update_vertex(u)
                self.compute_shortest_path()

                if show_animation:
                    new_path = self.compute_current_path()
                    if not self.compare_paths(current_path, new_path):
                        current_path_image[0].remove()
                        previous_path_image[0].remove()
                        previous_path = current_path.copy()
                        current_path = new_path.copy()
                        previous_path_image = self.display_path(previous_path,
                                                                ".c",
                                                                alpha=0.3)
                        current_path_image = self.display_path(current_path,
                                                               ".c")
                        plt.pause(pause_time)
        print("Path found")

        path = []
        for i in range(len(pathx)):
            path.append([pathx[i], pathy[i], paththeta[i]])
        set_path_find(path)
        add_angle_to_path(path)
        print("path : ", get_path_find())
        set_path_find(path)
        return True, pathx, pathy


def get_obs():
    obstacles = get_obstacles_position_grid_from_frame_test(imageP)
    # obstacles = get_obstacles()
    ox = []
    oy = []
    otheta = []
    for y in range(len(obstacles)):
        for x in range(len(obstacles[0])):
            if obstacles[y][x] == True:
                ox.append(x)
                oy.append(y)

    return ox, oy


def rot_conversion(rot):
    if 0 <= rot < 45:
        return 0
    if 45 <= rot < 90:
        return 1
    if 90 <= rot < 135:
        return 2
    if 135 <= rot < 180:
        return 3
    if rot == abs(180) or -180 < rot < -135:
        return 4
    if -135 <= rot < -90:
        return -3
    if -90 <= rot < -45:
        return -2
    if -45 <= rot < 0:
        return -1

def add_angle_to_path(path):
    for i in range(len(path) - 1):
        motion_x = path[i+1][0] - path[i][0]
        motion_y = path[i+1][1] - path[i][1]
        if motion_x == -1 and motion_y == -1:
            path[i][2] = 135
        elif motion_x == -1 and motion_y == 0:
            path[i][2] = 180
        elif motion_x == -1 and motion_y == 1:
            path[i][2] = -135
        elif motion_x == 0 and motion_y == -1:
            path[i][2] = 90
        elif motion_x == 0 and motion_y == 1:
            path[i][2] = -90
        elif motion_x == 1 and motion_y == -1:
            path[i][2] = 45
        elif motion_x == 1 and motion_y == 0:
            path[i][2] = 0
        elif motion_x == 1 and motion_y == 1:
            path[i][2] = -45
    path[-1][2] = path[-2][2]


def dstar_algo():

    sx, sy, rot = get_coordinate_aruco()
    print(sx, sy)
    gx, gy = get_destination()
    print("g : ", gx, gy)

    sx, sy = convert_pixel_to_case(int(sx), int(sy))
    gx, gy = convert_pixel_to_case(int(gx), int(gy))
    rot = float(rot)

    # TODO : change image path to frame
    image_path = "../res/threshold/barre-rouge.jpg"

    ox, oy = get_obs()

    spoofed_ox = []
    spoofed_oy = []
    dstarlite = DStarLite(ox, oy)
    dstarlite.main(Node(x=sx, y=sy, theta=0), Node(x=gx, y=gy, theta=0),
                    spoofed_ox=spoofed_ox, spoofed_oy=spoofed_oy)


if __name__ == "__main__":
    image_path = "res/threshold/barre-rouge.jpg"
    imageP = cv2.imread(image_path)
    croped_image = threshold_from_frame(imageP)
    # cv2.imshow("Threshold", croped_image)
    # cv2.waitKey()
    rows, cols = croped_image.shape
    set_pixels_x(cols)
    set_pixels_y(rows)
    set_cells_y(100)
    set_cells_x(100)
    set_destination((2, 1))
    set_coordinate_aruco((599, 599, 180))
    obstacles = get_obstacles_position_grid_from_frame_test(imageP)
    # print(obstacles)
    dstar_algo()







