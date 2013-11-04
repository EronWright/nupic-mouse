from __future__ import division
import os
import random
import operator
from nupic.frameworks.opf.modelfactory import ModelFactory

from learn.imagination import Imagination
from mouse.model_params import MODEL_PARAMS


class Mouse(object):
    
    def __init__(self, config, maze):
        self._config = config
        self._maze = maze
        self._training_mode = None
        
        self.id = 1
        self.location = None
        
    def reset(self, initial_location, training_mode):
        """ Resets the mouse to an initial location, in preparation for a new run """
        self._training_mode = training_mode
        self.location = initial_location
        
    """
    Abstract mouse class
    """
    def move(self):
        """
        Move to a new position in the maze.
        
        The mouse chooses to move a maximum of one space in any direction.
        """        
        pass
        
class DumbMouse(Mouse):
    def __init__(self, config, maze):
        Mouse.__init__(self, config, maze)
        self._previous_location = None
        
    def reset(self, initial_location, training_mode):
        Mouse.reset(self, initial_location, training_mode)
        
    def move(self):
        possible_moves = self._maze.possible_moves(self.location)
        
        # avoid turning around whenever possible (i.e. be curious!)
        if self._previous_location in possible_moves and len(possible_moves) >= 2:
            possible_moves.remove(self._previous_location)
        self._previous_location = self.location
        
        print '\tpossible moves: %s' % possible_moves
        if len(possible_moves) >= 1:
            self.location = random.sample(possible_moves, 1)[0]
    
class SmartMouse(Mouse):
    def __init__(self, config, maze):
        Mouse.__init__(self, config, maze)
        
        self._previous_location = None

        # this mouse uses the CLA
        self._model_path = config['serialization']['path']
        self._model_params = MODEL_PARAMS
        self._init_model()
        self._imagination = Imagination(self._model)
       
    def reset(self, initial_location, training_mode):
        Mouse.reset(self, initial_location, training_mode)
        self._model.resetSequenceStates()
        
    def move(self):
        
        possible_moves = self._maze.possible_moves(self.location)
        
        # avoid turning around whenever possible (i.e. be curious!)
        if self._previous_location in possible_moves and len(possible_moves) >= 2:
            possible_moves.remove(self._previous_location)
        self._previous_location = self.location
            
        if self._training_mode:
            # exploration: randomly walk the maze to learn where the cheese is.
            self.location = random.sample(possible_moves, 1)[0]
        else:
            # exploitation: choose the best possible move
            best_location = self._choose_best_move(possible_moves)
            self.location = best_location
            
        # update the model with the action we've taken
        model_input_data = self._convert_to_model_input(self.location)
        self._model.run(model_input_data)
        
    def _init_model(self):
        
        if os.path.exists(os.path.abspath(self._model_path)):
            self._model = ModelFactory.loadFromCheckpoint(
                os.path.relpath(self._model_path))
        else:
            self._model = ModelFactory.create(self._model_params)

        predicted_field = self._model_params['predictedField']
        if predicted_field:
            self._model.enableInference({'predictedField': predicted_field})
    
    def _convert_to_model_input(self, location):
      model_input_data = {
          'location': '%s-%s' % (location[0], location[1]),
          'cheese': self._maze.cheese[location]
      }
      return model_input_data
    
    def _choose_best_move(self, possible_moves):
        
        # use the imagination module to make predictions based on the 
        # a range of possible moves
        print '\t[alg] from location %s, possible moves are %s' % (self.location, possible_moves)
        
        def predict_closure(input):    
            def predict(model_fork):
                model_fork.disableLearning()
                result = model_fork.run(input)
                return result
            return predict
        
        if len(possible_moves) == 1:
            # no imagination is necessary in this case because there is only one choice
            return possible_moves[0]
            
        # apply the function for each action
        funcs = [predict_closure(self._convert_to_model_input(location)) for location in possible_moves]
        results = self._imagination.imagine(funcs)
       
        # get the OPF result for each possible move
        predictions = \
            [(location,r.inferences['multiStepPredictions']) for location,r in zip(possible_moves,results)]
        
        # evaluate the benefit associated with each possible move (i.e. the cost function)
        benefits = \
            [(location,self._maze.cheese[location] + self._benefit_function(prediction)) for location,prediction in predictions]
            
        # finally, select the best prediction
        sorted_predictions = sorted(benefits, key=operator.itemgetter(1))
        sorted_predictions.reverse()
        for l,p in sorted_predictions:
            print '\t[alg] evalation of move %s yields benefit %d' % (l,p)
        
        return sorted_predictions[0][0]
        
    def _benefit_function(self, multi_step_predictions):
        min_p = self._config['min_probability']
        # estimate how much cheese is predicted down the given path
        # this algorithm simply looks for the maximum potential cheese (with a probability threshold)
        # TODO replace with a better algorithm
        return max([max([v for v,p in probs.items() if p>=min_p])/step for step, probs in multi_step_predictions.items()])
        
        