# !/usr/bin/env python
from __future__ import division
import argparse
import sys
import random

from config import maze_config, mouse_config, runner_config
from mouse.maze import Maze
from mouse.mice import DumbMouse, SmartMouse
from mouse.runner import Runner


def main():
    
    parser = argparse.ArgumentParser(description='Maze config.')
    parser.add_argument('train', type=int, default=10, help='number of training runs')
    parser.add_argument('test', type=int, default=1, help='number of test runs')
    parser.add_argument('--mouse',
                        help='mouse type',
                        choices=['dumb', 'smart'],
                        default='dumb')
    args = parser.parse_args()
    random.seed()

    print '*************** MAZE ****************'
    maze = Maze(maze_config)

    print 'Maze layout:\n', maze.layout
    print 'Maze cheese:\n', maze.cheese
    print 'Initial location: ', maze.initial_location

    mouse = {
        'dumb': lambda: DumbMouse(mouse_config, maze),
        'smart': lambda: SmartMouse(mouse_config, maze),
    }[args.mouse]()

    mice = [mouse]
    
    runner = Runner(runner_config, maze, mice)

    
    def train_closure():
        def train():
            for i in range(args.train):
                print '*************** TRAIN ****************'
                runner.reset(train = True)
                runner.run()
        return train
        
    train_closure()()
    
    def test_closure(overall_rewards):
        def test():
            for i in range(args.test):
                print '*************** TEST *****************'
                runner.reset(train = False)
                run_rewards = runner.run()
        
                for mouse, run_reward in run_rewards.items():
                    overall_rewards[mouse] += run_reward
        return test
        
    overall_rewards = dict(((mouse,0) for m in mice))
    test_closure(overall_rewards)()
        
    print 'overall scores:'
    for mouse, overall_reward in overall_rewards.items():   
        print '\tmouse %s averaged %.2f cheese per run, after %d runs.'\
             % (mouse.id, overall_reward/args.test, args.test)
             
if __name__ == "__main__":
    main()