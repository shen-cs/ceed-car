import sys
from map import Map

def init():
  global map
  if len(sys.argv) != 3:
    print('Usage: python3 {} <map file> <path file>'.format(sys.argv[0]))
    exit(-1)
  map = Map(sys.argv[1])
  map.load_pathfile(sys.argv[2])

def run():
  global map
  print(map.path)
  for node in map.nodes:
    # print(node.id, ': ', end='')
    # print(node.neighbor_dict)
    print(node)
    if node.id in map.path and node.prev_node_id and node.next_node_id:
        print(node.get_direction())

if __name__ == '__main__':
  init()
  run()
