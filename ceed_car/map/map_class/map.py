"""
  Map class to represent road map
"""

import json
from node import Node

class Map(object):
  def __init__(self, mapname):

    """
    map json file format:
    {
      'id1': {'neighbor1': [edge_len, angle], 'neighbor2': [edge_len, angle], ...},
      'id2': {'neighbor1': [edge_len, angle], ...},
      ...
      ...
    }
    """

    with open(mapname, 'r') as f:
      self.data  = json.load(f)
    self.nodes = []
    self.generate_nodes()
  
  def generate_nodes(self):
    for node_id in self.data.keys():
      neighbor_dict = self.data[node_id]
      node = Node(node_id, neighbor_dict)
      self.nodes.append(node)
  
  def load_path(self, path):
     self.path = path
     """ update each node information """
     for node_id in self.path.keys(): # first two is start and end
       if not node_id == 'header':
         node = self.find_node(node_id)
         node_dict = self.path[node_id]
         prev_node_id = node_dict["prev"]
         next_node_id = node_dict["next"]
         node.set_prev_and_next(prev_node_id, next_node_id)
  
  def find_node(self, node_id):
     for node in self.nodes:
       if node.id == node_id:
         return node
     return None

  def load_pathfile(self, pathfile):
     with open(pathfile, 'r') as f:
       path = json.load(f)
       self.load_path(path)

  def output_pathfile(self, pathfile):
     with open(pathfile, 'w') as jsonfile:
       json.dump(self.path, jsonfile)

  
