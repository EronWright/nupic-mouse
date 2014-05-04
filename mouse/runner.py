from __future__ import division
import sys
import random

from util.event import Event

class Trial(object):
    """
    Represents a single trial of a given set of mice in a given maze
    """
    def __init__(self, maze, mice):
        self._maze = maze
        self.mice = mice
        
        self.current_tick = None
        self.num_ticks = None
        
        self.before_run = Event()
        self.after_run = Event()
        self.before_tick = Event()
        self.after_tick = Event()
        
    def reset(self, train = False, num_ticks = 0):
        self.num_ticks = num_ticks
        self.current_tick = 0
        self.train = train
        self.total_rewards = dict()
        
        self._maze.reset()
        for mouse in self.mice:
            initial_location = random.sample(self._maze.all_locations(),1)[0]
            mouse.reset(initial_location, train)
            self.total_rewards[mouse] = self._maze.cheese[initial_location]
            
    def run(self):
        self.before_run(self)
        
        while self.current_tick < self.num_ticks:
            self._tick()

        self.after_run(self)
        return self.total_rewards
        
    def _tick(self):
        
        self.current_tick += 1
        
        self.before_tick(self, self.current_tick)
        
        # tick each mouse
        for mouse in self.mice:
            
            # move
            old_location = mouse.location
            mouse.move()
            new_location = mouse.location
            
            # reward
            reward = self._maze.cheese[new_location]
            self.total_rewards[mouse] += reward
            
        self.after_tick(self, self.current_tick)
                