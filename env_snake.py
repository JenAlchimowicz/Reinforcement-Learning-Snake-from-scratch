class Snake():
    
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    
    def __init__(self, init_coor=[4,2], init_len=3):
        # note: possible to initialize with error, leave defaults for now
        self.start_coor = init_coor.copy()
        self.head = init_coor.copy()
        self.direction = self.DOWN
        self.body = list()
        for i in reversed(range(1,init_len)):
            self.body.append([self.head[0]-i, self.head[1]])
        self.start_body = self.body.copy()
            
    def reset_snake(self):
        self.head = self.start_coor
        self.body = self.start_body
        self.direction = self.DOWN
        
    def move(self, action):
        #ACTIONS
        # left = 0
        # straight = 1
        # right = 2

        # GET NEXT DIRECTION FROM ACTION
        clock_wise_dir = [self.UP, self.RIGHT, self.DOWN, self.LEFT]
        curr_dir_idx = clock_wise_dir.index(self.direction)
        
        # left turn
        if action == 0:
            next_dir = clock_wise_dir[curr_dir_idx - 1]
        #no turn
        elif action == 1:
            next_dir = self.direction #no change
        # right turn
        elif action == 2:
            next_dir = clock_wise_dir[(curr_dir_idx + 1) % 4]  # 4%4=0, so we go to the other end of list
        
        # update the direction
        self.direction = next_dir

        # EXECUTE TURN
        # add head to body
        self.body.append(self.head.copy())

        # move head
        if next_dir == self.UP:
            self.head[0] -= 1  #remember top left is [0,0]
        elif next_dir == self.DOWN:
            self.head[0] += 1
        elif next_dir == self.RIGHT:
            self.head[1] += 1
        elif next_dir == self.LEFT:
            self.head[1] -= 1

    # removes the last element from the body
    def pop_tail(self):
        self.body.pop(0)
                