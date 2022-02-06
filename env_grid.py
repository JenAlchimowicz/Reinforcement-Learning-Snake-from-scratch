import numpy as np
import random

class Grid():
    
    BODY_COLOR  = np.array([1,0,0], dtype=np.uint8)
    HEAD_COLOR  = np.array([9, 0, 0], dtype=np.uint8)
    FOOD_COLOR  = np.array([3,0,255], dtype=np.uint8)
    SPACE_COLOR = np.array([0,255,0], dtype=np.uint8)
    WALL_COLOR  = np.array([5,100,0], dtype=np.uint8)
    
    def __init__(self, grid_size=[30,30], unit_size=10, unit_gap=1):
        
        self.grid_size = np.asarray(grid_size, dtype=np.int)
        self.height = self.grid_size[0].copy()
        self.width = self.grid_size[1].copy()
        
        self.grid = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.grid[:,:,:]  = self.SPACE_COLOR
        self.grid[:,0,:]  = self.WALL_COLOR
        self.grid[:,-1,:] = self.WALL_COLOR
        self.grid[0,:,:]  = self.WALL_COLOR
        self.grid[-1,:,:] = self.WALL_COLOR
        
        self.save_grid = self.grid.copy()
        
        self.food = list()
        
    def reset_grid(self):
        self.grid = self.save_grid.copy()
        self.place_food_random()
    
    def get_color(self, coor):
        return self.grid[coor[0], coor[1], :]
    
    def check_death(self, Snake_c):
        
        # where snake wants to go
        square_color = self.get_color(Snake_c.head)
        
        # head in wall or in body
        if np.array_equal(square_color, self.WALL_COLOR) or np.array_equal(square_color, self.BODY_COLOR):
            return True
        
    def check_food_eaten(self, Snake_c):
        
        # where snake wants to go
        square_color = self.get_color(Snake_c.head)
        
        # head in wall or in body
        if np.array_equal(square_color, self.FOOD_COLOR):
            return True

    def place_food_random(self):
        
        while True:
            new_x = np.random.randint(1, self.height-1)
            new_y = np.random.randint(1, self.width-1)
            
            if np.array_equal(self.grid[new_x, new_y, :], self.SPACE_COLOR):
                #place food
                self.grid[new_x, new_y, :] = self.FOOD_COLOR
                self.food = [new_x, new_y]
                break
        
    def erase_cell(self, coor):
        self.grid[coor[0], coor[1], :] = self.SPACE_COLOR
        
    def draw_snake(self, Snake_c):
        head = Snake_c.head
        body = Snake_c.body
        
        # draw head
        self.grid[head[0], head[1], :] = self.HEAD_COLOR
        #draw body
        for coor in body:
            self.grid[coor[0], coor[1], :] = self.BODY_COLOR
            
    def get_food_direction(self, Snake_c):
        # reward direction, 0, 1, 2, 3; UP, DOWN, LEFT, RIGHT
        food_dir = [0]*4
        head = Snake_c.head
        
        # X coor <- get UP or DOWN or SAME LEVEL
        if head[0] < self.food[0]:    # food below head
            food_dir[1] = 1
        elif head[0] > self.food[0]:  # food below head
            food_dir[0] = 1
            
        # y coor <- get LEFT or RIGHT or SAME LEVEL
        if head[1] < self.food[1]:    # food to the right of head
            food_dir[3] = 1
        elif head[1] > self.food[1]:  # food to the left of head
            food_dir[2] = 1
            
        return food_dir
            
    def get_danger_direction(self, Snake_c):
        
        # UP = 0, RIGHT = 1, DOWN = 2, LEFT = 3 <- clockwise
        danger_absolute_pos = [0]*4
        # left = 0, straight = 1, right = 2
        danger_dir = [0]*3
        
        direction = Snake_c.direction
        head = Snake_c.head
        
        # Get absolute positions
        if np.array_equal(self.get_color([head[0]-1, head[1]]), self.WALL_COLOR) or \
           np.array_equal(self.get_color([head[0]-1, head[1]]), self.BODY_COLOR):     #up
            danger_absolute_pos[0] = 1
        if np.array_equal(self.get_color([head[0], head[1]+1]), self.WALL_COLOR) or \
           np.array_equal(self.get_color([head[0], head[1]+1]), self.BODY_COLOR):     #right
            danger_absolute_pos[1] = 1
        if np.array_equal(self.get_color([head[0]+1, head[1]]), self.WALL_COLOR) or \
           np.array_equal(self.get_color([head[0]+1, head[1]]), self.BODY_COLOR):     #down
            danger_absolute_pos[2] = 1
        if np.array_equal(self.get_color([head[0], head[1]-1]), self.WALL_COLOR) or \
           np.array_equal(self.get_color([head[0], head[1]-1]), self.BODY_COLOR):     #left
            danger_absolute_pos[3] = 1
        # result eg [1,1,0,0] <- corresponds to up, right, down, left
        
        # Get relative positions from absolute <- maintain clockiwse order
#         clock_wise_dir = [self.UP, self.RIGHT, self.DOWN, self.LEFT]
        clock_wise_dir = [0, 3, 1, 2]
        dir_idx = clock_wise_dir.index(direction)
        
        danger_dir[1] = danger_absolute_pos[dir_idx]        # check danger ahead
        danger_dir[0] = danger_absolute_pos[dir_idx-1]      # check danger to the left
        danger_dir[2] = danger_absolute_pos[(dir_idx+1)%4]  # check danger to the right
        
        return danger_dir
            