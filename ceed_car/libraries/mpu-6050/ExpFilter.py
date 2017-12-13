
class ExpFilter(object):
   def __init__(self, beta, init=0):
     self.beta = beta
     self.state = init

   def filterOnce(self, measurement):
     self.state = self.beta * measurement + (1 - self.beta) * self.state
    
