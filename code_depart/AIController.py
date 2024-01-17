class Node:
    def __init__(self, pos, parent=None):
        self.pos = pos
        self.parent = parent  # no parent needed ?
        self.g = 0            # cost from start node
        self.h = 0            # cost from goal node
        self.f = 0            # total cost


    def __eq__(self, other):
        return self.pos == other.pos
    

class AIController:
    
    def contains_square(self, center_pos, width, height, walls):
        for w in walls:
            if center_pos[0] - width >= w.topleft[0] and center_pos[0] + width <= w.topright[0] and center_pos[1] - height >= w.topleft[1] and center_pos[1] + height <= w.bottomleft[1]:
                return True
        return False

    # def contains_square(self, current_pos, walls):
    #     for w in walls:
    #         if current_pos[0] >= w.topleft[0] and current_pos[0] <= w.topright[0] and current_pos[1] >= w.topleft[1] and current_pos[1] <= w.bottomleft[1]:
    #             return True
    #     return False

    def __init__(self):
        self.visited_list = [] # could be a dict
        self.pending_list = []
        self.start_node = None
        self.goal_node = None
        self.path = []
        self.path_index = 0
        self.neighbors_pos  = [(0, 1), (1, 0), (0, -1), (-1, 0)] # right, down, left, up
        self.last_position = None


    def init(self, maze, player):
        self.a_star(maze)
        self.width = len(maze[0])
        self.height = len(maze)


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

    

    def a_star(self, maze):
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j] == 'S':
                    self.start_node = Node(pos=(i, j))
                    # self.pending_list.append(self.start_node)
                if maze[i][j] == 'E':
                    self.goal_node = Node(pos=(i, j))
        
        self.pending_list.append(self.start_node)
        self.positions = []	# for debugging
        while len(self.pending_list) > 0:
            current_node = self.pending_list[0]
            current_index = 0

            for i, node in enumerate(self.pending_list):
                if node.f < current_node.f:
                    current_node = node
                    current_index = i

            # print(current_node.pos)

            self.pending_list.pop(current_index)
            self.visited_list.append(current_node)

            x = current_node.pos[0]
            y = current_node.pos[1]
            # check if goal acheived
            if maze[x][y] == 'E':
                path = []
                current = current_node
                while current is not None:
                    # path.append(current.pos)
                    if current.pos != self.start_node.pos:
                        path.append(self.get_direction(current.parent.pos, current.pos))
                        self.positions.append((current.pos[1], current.pos[0]))
                    current = current.parent
                self.path = path[::-1]
                self.positions = self.positions[::-1]
                return path[::-1]

            neighbors = self.get_neighbors(maze, current_node)

            for n in neighbors:
                if n in self.visited_list:
                    continue
                
                n.g = current_node.g + 1
                n.h = (n.pos[0] - self.goal_node.pos[0]) ** 2 + (n.pos[1] - self.goal_node.pos[1]) ** 2
                n.f = n.g + n.h
                
                if n not in self.pending_list:
                    self.pending_list.append(n)

                    
    def pixel_postition_in_grid(self, pixel_pos, tile_size_x, tile_size_y):
        return pixel_pos[0] // tile_size_x, pixel_pos[1] // tile_size_y

    def pixel_to_tile(self, pixel_pos, tile_size_x, tile_size_y):
        position = (pixel_pos[0] // tile_size_x) // self.width, (pixel_pos[1] // tile_size_y) // self.height
        test = int(pixel_pos[1] // tile_size_y), int(pixel_pos[0] // tile_size_x)
        return int(pixel_pos[0] // tile_size_x), int(pixel_pos[1] // tile_size_y)
                    
    def play(self, perception_data, player, tile_size_x, tile_size_y):
        if(self.path_index >= len(self.positions)):
            return
        
        if self.last_position is None:
            self.last_position = self.pixel_to_tile(player.get_position(), tile_size_x, tile_size_y)
            print('next pos ', self.positions[self.path_index])
            # return self.path[self.path_index]
        print('player pos ', player.get_position(), ' en tile ',self.pixel_to_tile(player.get_position(), tile_size_x, tile_size_y))
        
        if self.last_position != self.pixel_to_tile(player.get_position(), tile_size_x, tile_size_y):
            self.path_index += 1
            print('next pos ', self.positions[self.path_index])

        # next_pos = self.path[self.path_index]
        next_pos = self.get_direction(self.last_position, self.positions[self.path_index])
        print(next_pos)
        self.last_position = self.pixel_to_tile(player.get_position(), tile_size_x, tile_size_y)
        return next_pos
    