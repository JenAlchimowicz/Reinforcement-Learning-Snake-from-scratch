'''
class with STEP, GET_STATE, and RESET
Combines env_snake and env_grid
All this could have been implemented in Snake_ENV but I prefer to keep the longer functions here to keep the Snake_ENV file clean
'''
from env_grid import Grid
from env_snake import Snake
import numpy as np

class Env_control():
    
    def __init__(self, grid_size=[30,30]):
        self.grid = Grid(grid_size)
        self.snake = Snake()
        self.done = False
        self.state = None
        # Solution to snake not learning
        self.distance_to_food = np.inf
    
    def step(self, action):
        # move snake
        self.snake.move(action)

        # check death
        if self.grid.check_death(self.snake):
            self.done = True
            reward = -10
            self.state = 'TERMINAL'
        
        # if didn't die
        else:
            # check reward (delete tail if no reward) + (palce food if food eaten)
            if self.grid.check_food_eaten(self.snake):
                reward = 20
                self.grid.place_food_random()

                # update grid
                self.grid.draw_snake(self.snake)

                # reset distance to food
                self.distance_to_food = np.inf

            else:
                # Snake not learning -> solution add reward for getting closer to food
                dist = np.power(np.power(self.grid.food[0] - self.snake.head[0],2) + np.power(self.grid.food[1] - self.snake.head[1] ,2), 0.5)
                if dist < self.distance_to_food:
                   reward = 1
                   self.distance_to_food = dist
                else:
                  reward = 0

                # update grid
                self.grid.erase_cell(self.snake.body[0])
                self.snake.pop_tail()
                self.grid.draw_snake(self.snake)

            # get state
            self.state = self.get_state()
    
        return self.state, reward, self.done, {}
    
    def get_state(self):
        # need to return (moving direction: [0, 0, 0, 0]; UP, DOWN, LEFT, RIGHT
        #                 reward direction: [0, 0, 0, 0]; UP, DOWN, LEFT, RIGHT
        #                 danger: [0, 0, 0]; LEFT, STRAIGHT, RIGHT) 
        state = [0]*4
        
        # Get moving direction
        direction = self.snake.direction
        state[direction] = 1
        
        # Get food direction
        state.extend(self.grid.get_food_direction(self.snake)) # adds eg [0,1,0,1]
        
        # Get danger directions
        state.extend(self.grid.get_danger_direction(self.snake)) # adds eg [0,1,0]
        
        return tuple(state)
    
    def reset(self):
        self.snake.reset_snake()
        self.grid.reset_grid()
        self.grid.draw_snake(self.snake)
        return self.get_state()
        