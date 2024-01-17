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

    def __init__(self, speed):
        self.visited_list = [] # could be a dict
        self.pending_list = []
        # right, down, left, up, right-down, left-up, left-down, right-up
        # self.neighbors_pos = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        self.start_node = None
        self.goal_node = None
        self.path = []
        self.path_index = 0
        self.speed = speed
        # neighbors_directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        neighbors_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] # right, down, left, up

        self.neighbors_pos = [(x*self.speed, y*self.speed)  for x, y in neighbors_directions]

    
    def is_overlap(self, current_pos, width, height, tile):
        import pygame

        rect = pygame.Rect(current_pos[0] - width, current_pos[1] - height, width, height)
        result =  rect.colliderect(tile)
        return result

    def is_touching_tile(self, pos, tile): # tile is a rect, pos is a tuple
        # return pos[0] >= tile.topleft[0] and pos[0] <= tile.topright[0] and pos[1] >= tile.topleft[1] and pos[1] <= tile.bottomleft[1]
        # return pos[0] - self.player_size[0] >= tile.topleft[0] and pos[0] + self.player_size[0] <= tile.topright[0] and pos[1] - self.player_size[1] >= tile.topleft[1] and pos[1] + self.player_size[1] <= tile.bottomleft[1]
        # if pos[0] - self.player_size[0] >= tile.bottomleft[0] or pos[0] + self.player_size[0] <= tile.bottomright[0]: # x is inside wall
        #     if pos[1] - self.player_size[1] >= tile.topleft[1] or pos[1] + self.player_size[1] <= tile.bottomleft[1]: # y is inside wall
        #         return True
        # return False
        # center_pos = pos
        # width = self.player_size[0]
        # height = self.player_size[1]
        # w = tile
        # # self.contains_square(self, pos, self.player_size[0], self.player_size[0], walls):
        # return center_pos[0] - width >= w.topleft[0] and center_pos[0] + width <= w.topright[0] and center_pos[1] - height >= w.topleft[1] and center_pos[1] + height <= w.bottomleft[1]
        # return tile.collidepoint(pos)
        return self.is_overlap(pos, self.player_size[0], self.player_size[1], tile)



    def contains_position(self, tile_list, player_pos):
        # import pygame
        # width = self.player_size[0]
        # height = self.player_size[1]
        # rect = pygame.Rect(player_pos[0] - width, player_pos[1] - height, width * 2, height * 2)

        # return rect.collidelist(tile_list) != -1
        # size = self.player_size[0] // 2, self.player_size[1] // 2
        for tile in tile_list:
            if self.is_touching_tile(player_pos, tile):
                return True
        return False
            
            # px1 = pos[0] + size[0]
            # px2 = pos[0] - size[0]

            # py1 = pos[1] + size[1]
            # py2 = pos[1] - size[1]

            # if (px1 >= p.bottomleft[0] and px1 <= p.bottomright[0]) or (px2 >= p.bottomleft[0] and px2 <= p.bottomright[0]):
            #     if (py1 >= p.topleft[1] and py1 <= p.bottomleft[1]) or (py2 >= p.topleft[1] and py2 <= p.bottomleft[1]):
            #         return True


            # if pos[0] + size[0] >= p.bottomleft[0] and pos[0] + size[0] <= p.bottomright[0]: # x is inside wall
            ## ICIIII
            # if pos[0] + self.player_size[0] >= p.bottomleft[0] and pos[0] + self.player_size[0] <= p.bottomright[0]: # x is inside wall
            #     if pos[1] + self.player_size[1] >= p.topleft[1] and pos[1] + self.player_size[1] <= p.bottomleft[1]: # y is inside wall
            #         return True
            # if pos[0] >= p.bottomleft[0] and pos[0] - self.player_size[0] >= p.bottomleft[0] and pos[0] + self.player_size[0] <= p.bottomright[0]: # x is inside wall
            #     if pos[1] - self.player_size[1] >= p.topleft[1] and pos[1] + self.player_size[1] <= p.bottomleft[1]: # y is inside wall
            #         return True
            # if pos[0] >= p.bottomleft[0] and pos[0] <= p.bottomright[0]: # x is inside wall
            #     if pos[1] >= p.topleft[1] and pos[1] <= p.bottomleft[1]: # y is inside wall
            #         return True
            # if p.x == pos[0] and p.y == pos[1]:
            #     return True
        

    def init(self, start, goal, wall_List, player):
        # print(wall_List)
        # self.player_size = player.get_size() // 2
        self.player_size = player.get_size()[0] / 2, player.get_size()[1] / 2
        self.a_star(wall_List, start, goal)


    def get_neighbors(self, walls, current_node):
        neighbors = []

        x = current_node.pos[0]
        y = current_node.pos[1]

        for n in self.neighbors_pos:
            pos = (x + n[0], y + n[1])

            if self.contains_position(walls, pos):
                continue    
            neighbors.append(Node(pos, current_node))
        print('current_pos ', current_node.pos  ,'neighbors ', len(neighbors))

        return neighbors
    

    def a_star(self, walls, start_pos, end_pos):
        self.start_node = Node(start_pos)
        # self.goal_node = Node(end_pos)
        self.goal_node = Node(end_pos)
        
        self.pending_list.append(self.start_node)

        while len(self.pending_list) > 0:
            current_node = self.pending_list[0]
            current_index = 0

            for i, node in enumerate(self.pending_list):
                if node.f < current_node.f:
                    current_node = node
                    current_index = i

            print(current_node.pos)

            self.pending_list.pop(current_index)
            self.visited_list.append(current_node)

            # check if goal acheived
            if self.is_touching_tile(current_node.pos, self.goal_node.pos):
            # if current_node == self.goal_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.pos)
                    current = current.parent
                self.path = path[::-1]
                return path[::-1]

            neighbors = self.get_neighbors(walls, current_node)

            for n in neighbors:
                if n in self.visited_list:
                    continue
                
                n.g = current_node.g + 1
                n.h = (n.pos[0] - self.goal_node.pos[0]) ** 2 + (n.pos[1] - self.goal_node.pos[1]) ** 2
                n.f = n.g + n.h
                
                if n not in self.pending_list:
                    self.pending_list.append(n)


    # def pathfind(self, walls, player):
        # PROCHAINE ETAPE : call a_star et return le premier element du path (et tous les autres par la suite)
        # if self.start_node is None:
        #     self.start_node = Node(player.get_position())
        #     self.pending_list.append(self.start_node)

        # # while len(self.pending_list) > 0:
        # current_index = 0
        # current_node = self.pending_list[0]

        # for i, node in enumerate(self.pending_list):
        #     if node.f < current_node.f:
        #         current_node = node
        #         current_index = i

        # self.pending_list.pop(current_index)
        # self.visited_list.append(current_node)

        # neighbors = self.get_neighbors(walls, current_node)

        # for n in neighbors:
        #     if n not in self.visited_list:
        #         n.g = current_node.g + 1
        #         n.h = (n.pos[0] - self.start_node.pos[0]) ** 2 + (n.pos[1] - self.start_node.pos[1]) ** 2
        #         n.f = n.g + n.h
                
        #         if n not in self.pending_list:
        #             self.pending_list.append(n)
        #             self.visited_list.append(n)
        #             return n.pos
        # # return self.pending_list[0].pos


    # def play(self, perception_data, player): 
    #     self.player_size = player.get_size()
    #     next_pos = self.pathfind(perception_data[0], player)

    #     # print('DATA ', perception_data[0])

    #     # neighbors = self.get_neighbors(perception_data[0], *player.get_position())
    #     # print('neighbors ', neighbors)

    #     # self.visited[player.get_position()] = True

    #     # instruction = 'DOWN'


    #     return next_pos
                    
    def play(self, perception_data, player):
        next_pos = self.path[self.path_index]
        self.path_index += 1
        return next_pos
    