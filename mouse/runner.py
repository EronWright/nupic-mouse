import sys

class Runner(object):
    
    def __init__(self, config, maze, mouse_list):
        self._config = config
        self._maze = maze
        self._mouse_list = mouse_list
        self._ticks = 0
        
    def reset(self, train = False):
        self._ticks = 0
        self._total_rewards = dict()
        for mouse in self._mouse_list:
            mouse.reset(self._maze.initial_location, train)
            self._total_rewards[mouse] = 0
            
    def run(self):
        
        print 'Start Run'
        while self._ticks < self._config['max_ticks']:
            try:
                self._tick()
            except Exception as e:
                print e
                sys.exit()

        print 'End Run'
    
        for mouse in self._mouse_list:
            print 'Mouse %d has total reward %d' % \
                (mouse.id, self._total_rewards[mouse])
        
        return self._total_rewards
        
    def _tick(self):
        
        self._ticks += 1
        
        print '[tick %d]' % self._ticks
        
        # tick each mouse
        for mouse in self._mouse_list:
            
            # move
            old_location = mouse.location
            mouse.move()
            new_location = mouse.location
            
            # reward
            reward = self._maze.cheese[new_location]
            self._total_rewards[mouse] += reward
            
            print '\tmouse %s moved from %s to %s, reward is %d' \
                % (mouse.id, old_location, new_location, reward)
            

                