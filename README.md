nupic-mouse
===========

A maze-running mouse using the NuPIC cortial learning algorithm (CLA).

The code was written during the [NuPIC Fall 2013 Hackathon](http://www.meetup.com/numenta/events/136809782/) in San Francisco, CA.

A demonstration of the project may be seen in the [demo video](http://www.youtube.com/watch?feature=player_detailpage&v=X4XjYXFRIAQ#t=1980).

The purpose of the project was to demonstrate how a hypothetical situation may be evaluated with a model.  I characterized this as giving the CLA an imagination.   A slow, prototype form of the idea is coded in learn/imagination.py.   Look at mouse/mice.py (choose-best-move) for example usage.  The gist is to provide a list of functions, each of which are applied to a copy of the original model to produce a prediction.  The set of predictions (one per function) are returned.

# Usage
Examine the main.py file to see the command-line arguments.  Run either the 'dumb' or the 'smart' mouse with a few training and test iterations, as specified on the command-line.

# Notable Changes
Since the demo, the main change is that the initial location within the maze is randomized.

# TODO
- Use a bigger, more interesting maze
- Provide a visualization of the maze and the mouse's movement (perhaps using curses module)
- Tweak the CLA model parameters

