from Constants import *
import LogiqueFloue
import numpy as np

class Node:
    def __init__(self, pos, parent=None):
        self.pos = pos
        self.parent = parent
        self.g = 0  # cost from start node
        self.h = 0  # cost from goal node
        self.f = 0  # total cost

    def __eq__(self, other):
        return self.pos == other.pos


class AIController:

    def __init__(self):
        self.visited_list = []
        self.pending_list = []
        self.start_node = None
        self.goal_node = None
        self.neighbors_pos = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, up, down, left
        self.path_positions = []

        self.path_index = 0
        self.last_position = None
        self.temp_goal_position = None  # temporary goal position for the player
        self.last_direction = 270
        self.direction_a_star = 0
        self.visited_postitions = []

    def init(self, maze, tile_size_x, tile_size_y):
        self.tile_size_x = tile_size_x
        self.tile_size_y = tile_size_y
        self.a_star(maze)
        self.path_index = 0
        self.temp_goal_position = self.path_positions[0]
        self.logique_floue = LogiqueFloue.LogiqueFlou()

    def get_neighbors(self, maze, current_node):
        neighbors = []

        x = current_node.pos[0]
        y = current_node.pos[1]

        for n in self.neighbors_pos:
            pos = (x + n[0], y + n[1])

            if maze[pos[0]][pos[1]] == '1':
                continue
            neighbors.append(Node(pos, current_node))

        return neighbors

    def get_direction(self, current_pos, next_pos):
        deltax = current_pos[0] - next_pos[0]
        deltay = current_pos[1] - next_pos[1]

        if deltax > 0:
            return 180
        elif deltax < 0:
            return 0
        elif deltay > 0:
            return 90
        elif deltay < 0:
            return 270

    def setup(self, maze):
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j] == 'S':
                    self.start_node = Node(pos=(i, j))
                if maze[i][j] == 'E':
                    self.goal_node = Node(pos=(i, j))

    def goal_achieved(self, current_node):
        current = current_node
        while current is not None:
            if current.pos != self.start_node.pos:
                self.path_positions.append((current.pos[1], current.pos[0]))
            current = current.parent

        self.path_positions = self.path_positions[::-1]

    def a_star(self, maze):
        self.setup(maze)
        self.pending_list.append(self.start_node)

        while len(self.pending_list) > 0:
            current_node = self.pending_list[0]
            current_index = 0

            for i, node in enumerate(self.pending_list):
                if node.f < current_node.f:
                    current_node = node
                    current_index = i

            self.pending_list.pop(current_index)
            self.visited_list.append(current_node)

            # check if goal achieved
            if current_node.pos == self.goal_node.pos:
                self.goal_achieved(current_node)
                break

            neighbors = self.get_neighbors(maze, current_node)

            for n in neighbors:
                if n in self.visited_list:
                    continue

                n.g = current_node.g + 1
                n.h = (n.pos[0] - self.goal_node.pos[0]) ** 2 + (n.pos[1] - self.goal_node.pos[1]) ** 2
                n.f = n.g + n.h

                if n not in self.pending_list:
                    self.pending_list.append(n)

    def get_distance(self, p1, p2):
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def find_closest_pos(self, current_pos):
        closest_distance = 100000
        closest_idx = 0

        for i, pos in enumerate(self.path_positions):
            if pos in self.visited_postitions:
                continue
            distance = self.get_distance(current_pos, pos)
            if distance < closest_distance:
                closest_distance = distance
                closest_idx = i

        return closest_idx

    def pixel_to_tile_center_pos(self, pixel_pos):
        return int(pixel_pos[0] // (self.tile_size_x / 3)), int(pixel_pos[1] // (self.tile_size_y / 3))
    
    def pixel_to_tile_pos(self, pixel_pos):
        return int(pixel_pos[0] // (self.tile_size_x)), int(pixel_pos[1] // (self.tile_size_y))

    def tile_pos_to_center_pos(self, tile_pos):
        return ((tile_pos[0] * 3) + 1), ((tile_pos[1] * 3) + 1)

    def get_a_star_direction(self, player):
        if (self.path_index >= len(self.path_positions)):
            print("Path completed or not found")
            return

        temp_center_pos = self.tile_pos_to_center_pos(self.temp_goal_position)
        curr_center_pos = self.pixel_to_tile_center_pos(player.get_rect().center)

        if self.temp_goal_position is not None:
            if temp_center_pos == curr_center_pos:
                self.visited_postitions.append(self.temp_goal_position)
                self.path_index = self.find_closest_pos(self.pixel_to_tile_pos(player.get_rect().center))
                self.temp_goal_position = self.path_positions[self.path_index]
                temp_center_pos = self.tile_pos_to_center_pos(self.temp_goal_position)

        self.direction_a_star = self.get_direction(curr_center_pos, temp_center_pos)

    def play(self, player, perception):
        wall_list, obstacle_list, item_list, monster_list, door_list = perception

        if len(door_list) > 0:
            return {DOOR: ''}
        if len(monster_list) > 0:
            return {MONSTER: monster_list[0]}

        has_obstacle = False
        logique_direction = None
        if len(obstacle_list) > 0:
            logique_direction, has_obstacle = self.run_logique_floue(player, perception)

        self.get_a_star_direction(player)

        if has_obstacle:
            difference = abs(logique_direction - self.last_direction)
            if difference < 0.01:
                next_direction = self.direction_a_star
            else:
                next_direction = logique_direction
        else:
            next_direction = self.direction_a_star

        self.last_direction = next_direction

        return {DIRECTION: next_direction}

    def run_logique_floue(self, player, perception):
        instruction, has_obstacle = self.logique_floue.run(self.last_direction, self.direction_a_star, player, perception)
        next_direction = self.last_direction

        next_direction -= instruction
        if next_direction > 360:
            next_direction -= 360
        if next_direction < 0:
            next_direction += 360

        return next_direction, has_obstacle
