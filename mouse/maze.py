import numpy as np
import numpy
from numpy.random import random_integers as rand
import random

class Maze(object):
    
    def __init__(self, config):
        self._config = config
        self.initial_location = config['initial_location']
        
        self.layout = generate_maze(20,10,complexity=.75,density=.75)
        self.cheese = generate_cheese(self)
        
    def reset(self):
        pass
    
    def all_locations(self):
        """
        Provides a list of all valid locations in the maze.
        """
        shape = self.layout.shape
        return [(x,y) for x in range(shape[0]) for y in range(shape[1]) if not self.layout[(x,y)]]
        
    def possible_moves(self, location):
        # return the adjacent cells
        cx,cy = location
        shape = self.layout.shape
        cells = [(x,y) for x,y in [(cx-1,cy),(cx+1,cy),(cx,cy-1),(cx,cy+1)] if 0 <= x < shape[0] and 0 <= y < shape[1]]
        return [c for c in cells if not self.layout[c]]
      
    def print_maze(self):
        for x in range(self.layout.shape[0]):
            s = ""
            for y in range(self.layout.shape[1]):
                s += ((str(self.cheese[(x,y)]) if self.cheese[(x,y)] > 0 else ' ') if not self.layout[(x,y)] else '#')
            print s
            
          
def generate_cheese(maze, density=.1, mu=5, sigma=3):
    Z = numpy.zeros(maze.layout.shape, dtype=int)
    locations = maze.all_locations()
    density = int(density * len(locations))
    for i in range(density):
        pos = locations[random.randint(0,len(locations)-1)]
        Z[pos] = min(max(0,int(random.gauss(mu,sigma))),9)
    return Z
  
# credit: wikipedia - http://en.wikipedia.org/wiki/Maze_generation_algorithm
def generate_maze(width=81, height=51, complexity=.75, density=.75):
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    density    = int(density * (shape[0] // 2 * shape[1] // 2))
    # Build actual maze
    Z = numpy.zeros(shape, dtype=bool)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    # Make aisles
    for i in range(density):
        x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2
        Z[y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:             neighbours.append((y, x - 2))
            if x < shape[1] - 2:  neighbours.append((y, x + 2))
            if y > 1:             neighbours.append((y - 2, x))
            if y < shape[0] - 2:  neighbours.append((y + 2, x))
            if len(neighbours):
                y_,x_ = neighbours[rand(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    return Z
    