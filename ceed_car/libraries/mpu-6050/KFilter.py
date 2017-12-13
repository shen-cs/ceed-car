import numpy as np
from numpy.linalg import inv
"""
  Kalman filter implementation.
"""
class KFilter(object):

  """
  x: state vector
  P: convariance matrix of state vector
  F: state transition matrix
  u: motion vector
  z: measurement vector
  H: measurement function(projection matrix from state to measurement)
  R: covariance matrix of measurement vector
  """
  def __init__(self, x, P, F, u, z, H, R, Q):
    assert(x.shape[1] == 1)
    assert(x.shape[0] == P.shape[0] and P.shape[0] == P.shape[1] and F.shape[0] == P.shape[0])
    assert(H.shape == (z.shape[0], x.shape[0]))
    assert(R.shape == (z.shape[0], z.shape[0]))
    self.x = x
    self.P = P
    self.F = F
    self.u = u
    self.z = z
    self.H = H
    self.R = R
    self.Q = Q

  def measurement_update(self):
    self.y = self.z - np.dot(self.H, self.x)
    self.S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R
    self.K = np.dot(np.dot(self.P, self.H.T), inv(self.S))
    self.x = self.x + np.dot(self.K, self.y)
    self.P = np.dot(np.eye(self.P.shape[0]) - np.dot(self.K, self.H), self.P)

  def state_transition(self):
    self.x = np.dot(self.F, self.x) + self.u
    self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q

  def filterOnce(self, measurement):
    assert(self.z.shape == measurement.shape)
    self.z = measurement
   # self.state_transition()
    self.measurement_update()
    self.state_transition()
