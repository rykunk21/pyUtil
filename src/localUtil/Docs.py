class Docs:
  """
  Docs provides a convenient interface for accessing the methods, docstrings, and data members of a given class.
  """

  def __init__(self, cls):
    """
    Constructor for the Docs class.

    Arguments:
    cls -- the class to get the methods, docstrings, and data members for.
    """
    self.cls = cls

  def getMethods(self):
    """
    Get a dictionary of the methods of the given class, where the keys are the method names and the values are their docstrings.

    Returns:
    A dictionary of the methods of the given class.
    """
    methods = {}
    for name, method in self.cls.__dict__.items():
      if callable(method):
        methods[name] = method.__doc__
    return methods

  def getDataMembers(self):
    """
    Get a dictionary of the data members of the given class, where the keys are the data member names and the values are their values.

    Returns:
    A dictionary of the data members of the given class.
    """
    data_members = {}
    for name, value in self.cls.__dict__.items():
      if not callable(value):
        data_members[name] = value
    return data_members
    
  def getName(self):
    """
    Get the name of the constructor of the given class.

    Returns:
    The name of the constructor of the given class.
    """
    return self.cls.__name__

    