import numpy as np

class Maze(object):
    
    def __init__(self, config):
        self._config = config
        self.initial_location = config['initial_location']
        
        self.layout = np.matrix(config['layout'])
        self.cheese = np.matrix(config['cheese'])
        
    def reset(self):
        pass
    
    def all_locations(self):
        """
        Provides a list of all valid locations in the maze.
        """
        shape = self.layout.shape
        return [(x,y) for x in range(shape[0]) for y in range(shape[1]) if self.layout[(x,y)] > 0]
        
    def possible_moves(self, location):
        # return the adjacent cells
        cx,cy = location
        shape = self.layout.shape
        cells = [(x,y) for x,y in [(cx-1,cy),(cx+1,cy),(cx,cy-1),(cx,cy+1)] if 0 <= x < shape[0] and 0 <= y < shape[1]]
        return [c for c in cells if self.layout[c] > 0]
      
    def print_maze(self):
        for x in range(self.layout.shape[0]):
            s = ""
            for y in range(self.layout.shape[1]):
                s += (str(self.cheese[(x,y)]) if self.layout[(x,y)] == 1 else '#')
            print s