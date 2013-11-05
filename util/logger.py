import inspect
import logging

def init_logger(obj):
  """Helper function to create a logger object for the current object with
  the project prefix """
  if inspect.isclass(obj):
    myClass = obj
  else:
    myClass = obj.__class__
  logger = logging.getLogger(".".join(
    ['com.example', myClass.__module__, myClass.__name__]))
  return logger