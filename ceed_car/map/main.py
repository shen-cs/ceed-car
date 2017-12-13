import sys
sys.path.insert(0, './map')
sys.path.insert(1, '../rc_control')
sys.path.insert(2, './wrap_qmc')
from map import Map
from motor_pwm import Motor
from qmc5883 import QMC5883
import time

SPEED = 0.8

def build_path():
  global map
  
  #if len(sys.argv) != 3:
  #  print('Usage: python3 {} <map file> <path file>'.format(sys.argv[0]))
  #  exit(-1)
  map = Map('map.json')
  map.load_pathfile(sys.argv[1])

  dist_rec = []
  direc_rec = []
  node = map.find_node(map.path['header']['start'])
  while node.next_node_id:
      dist_rec.append(node.get_edge_len(node.next_node_id))
      if node.prev_node_id:
          direc_rec.append(node.get_direction())
          print(node.id)
      node = map.find_node(map.path[node.id]['next'])

  return dist_rec, direc_rec

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('<path file>')
        exit(-1)
    dist_rec, direc_rec = build_path()
    direc_rec.append(0)
    print(dist_rec, direc_rec)
    motor = Motor([18,23,24,25])
    qmc = QMC5883()
    for i, dis in enumerate(dist_rec):
        print('dis: ', dis)
        motor.forward()
        time.sleep(dis/SPEED)
        print('dir: ', direc_rec[i])
        goal_ang = qmc.read_azimuth()+direc_rec[i]
        if goal_ang > 360:
            goal_ang -= 360
        elif goal_ang < 0:
            goal_ang += 360
        print('goal ang:', goal_ang)
        if direc_rec[i]>0:
            while abs(qmc.read_azimuth()-goal_ang) > 1:
                motor.right()
                print('ang: ', qmc.read_azimuth())
        else:
            while abs(qmc.read_azimuth()-goal_ang) > 1:
                motor.left()
                print('ang: ', qmc.read_azimuth())
    motor.stop()
