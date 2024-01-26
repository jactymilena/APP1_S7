from LogiqueFloue import *

class Node:
    def __init__(self, pos, parent=None):
        self.pos = pos
        self.parent = parent  
        self.g = 0            # cost from start node
        self.h = 0            # cost from goal node
        self.f = 0            # total cost


    def __eq__(self, other):
        return self.pos == other.pos
    

class AIController:
    
    def __init__(self):
        self.visited_list = []
        self.pending_list = []
        self.start_node = None
        self.goal_node = None
        self.path_index = 0
        self.neighbors_pos  = [(0, 1), (1, 0), (0, -1), (-1, 0)] # right, up, down, left
        self.last_position = None
        self.path_positions = []	
        self.last_direction = 270
        


    def init(self, maze, tile_size_x, tile_size_y):
        self.tile_size_x = tile_size_x
        self.tile_size_y = tile_size_y
        self.a_star(maze)
        self.logique_flou = LogiqueFlou()


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
            return "LEFT"
        elif deltax < 0:
            return "RIGHT"
        elif deltay > 0:
            return "UP"
        elif deltay < 0:
            return "DOWN"
        
    
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


    def pixel_to_tile_pos(self, pixel_pos):
        return int(pixel_pos[0] // self.tile_size_x), int(pixel_pos[1] // self.tile_size_y)


    def play(self, player):
        if(self.path_index >= len(self.path_positions)):
            print("Path completed or not found")
            return
        
        current_position = self.pixel_to_tile_pos(player.get_position())
        
        if self.last_position is not None and self.last_position != current_position:
            # continue to the next position in the path
            self.path_index += 1

        self.last_position = current_position

        return self.get_direction(current_position, self.path_positions[self.path_index])
    
    def run_logique_flou(self, player, perception):

        instruction = self.logique_flou.run(self.last_direction, player, perception)
        self.last_direction += instruction
        if self.last_direction > 360 : 
            self.last_direction -= 360
        if self.last_direction < 0:
            self.last_direction += 360
        return self.last_direction
    