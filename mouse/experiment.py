from __future__ import division
import logging

from util.event import Event

from mouse.maze import Maze
from mouse.mice import Mouse, DumbMouse, SmartMouse
from mouse.runner import Trial

class Experiment(object):
    """
    An experiment consisting of a maze and a set of mice.
    
    A number of a trials are run, with the maze reset between each trial.
    Note that the mouse's memory (if any) is retained across trials.
    
    The experiment might be a training exercise or a test, as indicated
    """
    
    def __init__(self, maze, mice):
        self.maze = maze
        self.mice = mice
        self.trial = Trial(self.maze, self.mice)
        
        self.train = None
        self.num_trials = None
        self.num_ticks = None
    
        self.before_experiment = Event()
        self.after_experiment = Event()
        self.before_trial = Event()
        self.after_trial = Event()
        
    def reset(self, train = False, num_trials = 10, num_ticks = 10):
        self.overall_rewards = dict(((m,0) for m in self.mice))
        self.average_rewards = dict(((m,0.0) for m in self.mice))
        self.train = train
        self.num_trials = num_trials
        self.num_ticks = num_ticks
        
    def run(self):
        self.before_experiment(self)
        
        trial = self.trial
        for i in range(self.num_trials):
            # a single trial run
            trial.reset(train = self.train, num_ticks = self.num_ticks)
            self.before_trial(trial, i+1)
            
            # run the trial
            run_rewards = trial.run()
            
            # update performance numbers
            for mouse, run_reward in run_rewards.items():
                self.overall_rewards[mouse] += run_reward
            self.average_rewards = dict(((m,r/(i+1)) for m,r in self.overall_rewards.items()))

            self.after_trial(trial, i+1)
        
        self.after_experiment(self)
        