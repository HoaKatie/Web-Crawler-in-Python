class Queue: # follows FIFO (first in first out)

  def __init__(self, root=None): # a constructor to allow class to initialize
    self.root = root
    self.q = []

  def put(self, new_Item):
    if self.root is None:
      self.root = 0
    self.q.append(new_Item) # enqueue item to the end of the queue 
    return True  # flags

  def get(self):
    if self.q is []:
      return "" # the queue is empty
    else:
      return_item = self.q.pop(0) # dequeue item from the start of the queue
      return return_item

  def empty(self): #return True if empty
    return len(self.q) == 0