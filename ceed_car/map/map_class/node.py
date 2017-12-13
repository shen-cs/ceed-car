"""
Node Class to represent intersections of map
"""


class Node(object):
   def __init__(self, id, neighbor_dict=None):
     self.id = id
     self.neighbor_dict = neighbor_dict # neighbor_dict: { node_id: [edge_len, angle]}
     self.prev_node_id = None
     self.next_node_id = None

   def set_next(self, next_node_id):
     self.next_node_id = next_node_id
   
   def set_prev(self, prev_node_id):
     self.prev_node_id = prev_node_id

   def set_prev_and_next(self, prev_node_id, next_node_id):
     self.set_prev(prev_node_id)
     self.set_next(next_node_id)
   
   def set_neighbor_dict(self, neighbor_dict):
     self.neighbor_dict = neighbor_dict

   def get_direction(self):
     prev_angle = self.neighbor_dict[self.prev_node_id][1]
     next_angle = self.neighbor_dict[self.next_node_id][1]
     turning_angle = (next_angle - prev_angle)-180
     if turning_angle > 180:
         turning_angle -= 360
     elif turning_angle < -180:
         turning_angle += 360
     #return [edge_len, turning_angle]
     return turning_angle
   
   def get_edge_len(self, i):
       if self.neighbor_dict[i]:
           return self.neighbor_dict[i][0]
       else:
           return -1
   
   def __repr__(self):
     s = 'Node_id:{}\t'.format(self.id)
     s += 'prev: {}, next: {}'.format(self.prev_node_id, self.next_node_id)
     return s
