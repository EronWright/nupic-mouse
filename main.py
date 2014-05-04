# !/usr/bin/env python
from __future__ import division
import logging
import argparse
import sys
import random

from util.event import Event

from config import maze_config, mouse_config
from mouse.maze import Maze
from mouse.mice import Mouse, DumbMouse, SmartMouse
from mouse.experiment import Experiment
from mouse.runner import Trial


def main():
    random.seed()
    
    parser = argparse.ArgumentParser(description='Maze config.')
    parser.add_argument('train', type=int, default=10, help='number of training runs')
    parser.add_argument('test', type=int, default=1, help='number of test runs')
    parser.add_argument('--ticks', type=int, default=5, help='number of ticks per run')
    parser.add_argument('--mouse',
                        help='mouse type',
                        choices=['dumb', 'smart'],
                        default='dumb')
    args = parser.parse_args()
    
    # configure logging (incl. NuPIC logging)
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout, 
    #                   format="%(message)s")
       
    logging.basicConfig(level=logging.WARNING, stream=sys.stdout)
    
    maze = Maze(maze_config)
    mice = []

    mouse = {
        'dumb': lambda: DumbMouse(mouse_config, maze),
        'smart': lambda: SmartMouse(mouse_config, maze),
    }[args.mouse]()
    mice.append(mouse)
    
    def _on_before_trial(trial, i):
        print '[trial %d]' % i
        for mouse in trial.mice:
            print '\tmouse %d in initial location %s' % (mouse.id, str(mouse.location))
    
    def _on_before_trial_tick(trial, tick):
        print '\t[tick %d]' % tick
        
    def _on_after_mouse_move(mouse, prev_location, new_location):
        print '\t\tmouse %s moved from %s to %s' \
            % (mouse.id, prev_location, new_location)
        
    def _on_after_trial(trial, i):
        for mouse, reward in trial.total_rewards.items():
            print '\tmouse %d has total reward %d' % \
                (mouse.id, reward)
            
    def _on_after_experiment(experiment):
        for mouse, avg_reward in experiment.average_rewards.items():   
            print 'mouse %s averaged %.2f cheese per run.'\
                 % (mouse.id, avg_reward)
                
    experiment = Experiment(maze, mice) 
    experiment.after_experiment.append(_on_after_experiment)
    experiment.before_trial.append(_on_before_trial)
    experiment.after_trial.append(_on_after_trial)
    experiment.trial.before_tick.append(_on_before_trial_tick)
    mouse.after_move.append(_on_after_mouse_move)
    
    print '*************** MAZE *****************'
    maze.print_maze()
    
    if args.train >= 1:
        print '*************** TRAIN ****************'
    
        experiment.reset(train = True, num_trials = args.train, num_ticks = args.ticks)
        experiment.run()
    
    print '*************** TEST *****************'
    experiment.reset(train = False, num_trials = args.test, num_ticks = args.ticks)
    experiment.run()

             
if __name__ == "__main__":
    main()