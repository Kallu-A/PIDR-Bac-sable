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
import heapq
from threshold import threshold_from_frame, get_obstacles_position_grid_from_frame, get_obstacles_position_grid_from_frame_test
import cv2
import time

show_animation = False
pause_time = 1
p_create_random_obstacle = 0


class Node:
    def __init__(self, x: int = 0, y: int = 0, cost: float = 0.0):
        self.x = x
        self.y = y
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.cost == other.cost

    def __hash__(self):
        return hash((self.x, self.y, self.cost))


def add_coordinates(node1: Node, node2: Node):
    new_node = Node()
    new_node.x = node1.x + node2.x
    new_node.y = node1.y + node2.y
    new_node.cost = node1.cost + node2.cost
    return new_node


def compare_coordinates(node1: Node, node2: Node):
    return node1.x == node2.x and node1.y == node2.y


class Node:
    def __init__(self, x: int = 0, y: int = 0, cost: float = 0.0):
        self.x = x
        self.y = y
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.cost == other.cost

    def __hash__(self):
        return hash((self.x, self.y, self.cost))

def add_coordinates(node1: Node, node2: Node):
    new_node = Node()
    new_node.x = node1.x + node2.x
    new_node.y = node1.y + node2.y
    new_node.cost = node1.cost + node2.cost
    return new_node

def compare_coordinates(node1: Node, node2: Node):
    return node1.x == node2.x and node1.y == node2.y

class DStarLite:
    motions = [
        Node(1, 0, 1),
        Node(0, 1, 1),
        Node(-1, 0, 1),
        Node(0, -1, 1),
        Node(1, 1, math.sqrt(2)),
        Node(1, -1, math.sqrt(2)),
        Node(-1, 1, math.sqrt(2)),
        Node(-1, -1, math.sqrt(2))
    ]

    def __init__(self, ox: list, oy: list):
        self.x_max, self.y_max = get_cells_xy()
        self.obstacles = [Node(x, y) for x, y in zip(ox, oy)]
        self.obstacles_xy = np.array([[obstacle.x, obstacle.y] for obstacle in self.obstacles])
        self.start = Node(0, 0)
        self.goal = Node(0, 0)
        self.U = []
        self.km = 0.0
        self.rhs = self.create_grid(float("inf"))
        self.g = self.create_grid(float("inf"))
        self.detected_obstacles_xy = np.empty((0, 2))
        self.initialized = False

    def create_grid(self, val: float):
        return np.full((self.x_max, self.y_max), val)

    def is_obstacle(self, node: Node):
        obstacle_x_equal = self.obstacles_xy[:, 0] == node.x
        obstacle_y_equal = self.obstacles_xy[:, 1] == node.y
        return (obstacle_x_equal & obstacle_y_equal).any()

    def c(self, node1: Node, node2: Node):
        if self.is_obstacle(node2):
            return math.inf
        new_node = Node(node1.x - node2.x, node1.y - node2.y)
        detected_motion = list(filter(lambda motion: compare_coordinates(motion, new_node), self.motions))
        return detected_motion[0].cost if detected_motion else math.inf

    def h(self, s: Node):
        return 1

    def calculate_key(self, s: Node):
        return (min(self.g[s.x][s.y], self.rhs[s.x][s.y]) + self.h(s) + self.km, min(self.g[s.x][s.y], self.rhs[s.x][s.y]))

    def is_valid(self, node: Node):
        return 0 <= node.x < self.x_max and 0 <= node.y < self.y_max

    def get_neighbours(self, u: Node):
        return [add_coordinates(u, motion) for motion in self.motions if self.is_valid(add_coordinates(u, motion))]

    def pred(self, u: Node):
        return self.get_neighbours(u)

    def succ(self, u: Node):
        return self.get_neighbours(u)

    def initialize(self, start: Node, goal: Node):
        self.start.x = start.x
        self.start.y = start.y
        self.goal.x = goal.x
        self.goal.y = goal.y
        if not self.initialized:
            self.initialized = True
            self.U = []
            self.km = 0.0
            self.rhs = self.create_grid(math.inf)
            self.g = self.create_grid(math.inf)
            self.rhs[self.goal.x][self.goal.y] = 0
            heapq.heappush(self.U, (self.calculate_key(self.goal), self.goal))
            self.detected_obstacles_xy = np.empty((0, 2))

    def update_vertex(self, u: Node):
        if not compare_coordinates(u, self.goal):
            self.rhs[u.x][u.y] = min([self.c(u, sprime) + self.g[sprime.x][sprime.y] for sprime in self.succ(u)])
        self.U = [(key, node) for key, node in self.U if not compare_coordinates(node, u)]
        if self.g[u.x][u.y] != self.rhs[u.x][u.y]:
            heapq.heappush(self.U, (self.calculate_key(u), u))

    def compare_keys(self, key_pair1: tuple[float, float], key_pair2: tuple[float, float]):
        return key_pair1 < key_pair2

    def compute_shortest_path(self):
        while self.U and (self.compare_keys(self.U[0][0], self.calculate_key(self.start)) or self.rhs[self.start.x][self.start.y] != self.g[self.start.x][self.start.y]):
            kold, u = heapq.heappop(self.U)
            if self.compare_keys(kold, self.calculate_key(u)):
                heapq.heappush(self.U, (self.calculate_key(u), u))
            elif self.g[u.x][u.y] > self.rhs[u.x][u.y]:
                self.g[u.x][u.y] = self.rhs[u.x][u.y]
                for s in self.pred(u):
                    self.update_vertex(s)
            else:
                self.g[u.x][u.y] = math.inf
                for s in self.pred(u) + [u]:
                    self.update_vertex(s)

    def detect_changes(self):
        changed_vertices = list()
        if len(self.spoofed_obstacles) > 0:
            for spoofed_obstacle in self.spoofed_obstacles[0]:
                if compare_coordinates(spoofed_obstacle, self.start) or \
                        compare_coordinates(spoofed_obstacle, self.goal):
                    continue
                changed_vertices.append(spoofed_obstacle)
                self.detected_obstacles_xy = np.concatenate(
                    (
                        self.detected_obstacles_xy,
                        [[spoofed_obstacle.x, spoofed_obstacle.y]]
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
        path = []
        current_point = Node(self.start.x, self.start.y)
        while not compare_coordinates(current_point, self.goal):
            path.append(current_point)
            current_point = min(self.succ(current_point), key=lambda sprime: self.c(current_point, sprime) + self.g[sprime.x][sprime.y])
        path.append(self.goal)
        return path

    def display_path(self, path: list, colour: str, alpha: float = 1.0):
        px = [(node.x) for node in path]
        py = [(node.y) for node in path]
        drawing = plt.plot(px, py, colour, alpha=alpha)
        plt.pause(pause_time)
        return drawing

    def compare_paths(self, path1: list, path2: list):
        if len(path1) != len(path2):
            return False
        for node1, node2 in zip(path1, path2):
            if not compare_coordinates(node1, node2):
                return False
        return True

    def main(self, start: Node, goal: Node,
             spoofed_ox: list, spoofed_oy: list):
        self.spoofed_obstacles = [[Node(x,
                                        y)
                                   for x, y in zip(rowx, rowy)]
                                  for rowx, rowy in zip(spoofed_ox, spoofed_oy)
                                  ]
        pathx = []
        pathy = []
        self.initialize(start, goal)
        last = self.start
        self.compute_shortest_path()
        pathx.append(self.start.x)
        pathy.append(self.start.y)
        path = []
        for i in range(len(pathx)):
            path.append((pathx[i], pathy[i], 0))
        set_path_find(path)

        while not compare_coordinates(self.goal, self.start):
            if self.g[self.start.x][self.start.y]== math.inf:
                print("No path possible")
                return False, pathx, pathy

            self.start = min(self.succ(self.start),
                             key=lambda sprime:
                             self.c(self.start, sprime) +
                             self.g[sprime.x][sprime.y])
            pathx.append(self.start.x)
            pathy.append(self.start.y)
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
                    self.rhs[u.x][u.y] = math.inf
                    self.g[u.x][u.y]= math.inf
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
            path.append([pathx[i], pathy[i], 0])
        set_path_find(path)
        add_angle_to_path(path)
        print("path : ", get_path_find())
        set_path_find(path)
        return True, pathx, pathy


def get_obs():
    #obstacles = get_obstacles_position_grid_from_frame_test(imageP)
    obstacles = get_obstacles()
    ox = []
    oy = []
    otheta = []
    for y in range(len(obstacles)):
        for x in range(len(obstacles[0])):
            if obstacles[y][x] == True:
                ox.append(x)
                oy.append(y)

    return ox, oy

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
    print("dStarLite coordinate aruco : ", get_coordinate_aruco())

    gx, gy = get_destination()
    sx, sy = convert_pixel_to_case(int(sx), int(sy))
    gx, gy = convert_pixel_to_case(int(gx), int(gy))
    # print("Start : ", sx, sy)
    # print("Goal : ", gx, gy)
    rot = float(rot)

    # TODO : change image path to frame
    image_path = "../res/threshold/barre-rouge.jpg"

    ox, oy = get_obs()

    spoofed_ox = []
    spoofed_oy = []
    dstarlite = DStarLite(ox, oy)
    dstarlite.main(Node(x=sx, y=sy), Node(x=gx, y=gy),
                    spoofed_ox=spoofed_ox, spoofed_oy=spoofed_oy)


if __name__ == "__main__":

    start = time.time()


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
    end = time.time()
    print("algo time : ", end - start)  # around 4s for a 100 x 100 grid

