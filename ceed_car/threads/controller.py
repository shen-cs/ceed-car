import sys
from pubsub import pub
import signal
import RPi.GPIO as gpio
import time
import threading
from libraries.motor_pwm import Motor
from libraries.wrap_qmc.qmc5883 import QMC5883
import math

threadLock = threading.Lock()

class controller_thread(threading.Thread):
  def __init__(self, map):
    threading.Thread.__init__(self)
    self.motor = Motor([18, 23, 24, 25])
    self.qmc = QMC5883()
    self.go = False
    self.stop = False
    self.card_present = False
    self.current_node_idx = 0
    self.next_command = 'f'
    self.current_command = ''
    self.next_heading = 0
    self.map = map
    self.zero_cross = 0 # 0: good, 1: right turn cross 0, 2: left turn cross 0
    
    self.updated = False

    self.dist_rec = []
    self.direc_rec = []
    node = self.map.find_node(self.map.path['header']['start'])
    while node.next_node_id:
      self.dist_rec.append(node.get_edge_len(node.next_node_id))
      if node.prev_node_id:
        self.direc_rec.append(node.get_direction())
        print('[CONTROLLER]', 'path thru:', node.id)
      node = self.map.find_node(map.path[node.id]['next'])

  def rfid_listener(self, arg1):
    global threadLock
    #threadLock.acquire()
    print('[CONTROLLER]', 'card detected')
    if self.current_node_idx == len(self.direc_rec):
      print('[CONTROLLER]', 'at destination')
      self.stop = True
      return
    heading = self.qmc.read_azimuth()
    goal_ang = heading + self.direc_rec[self.current_node_idx]
    if goal_ang > 360:
      goal_ang -= 360
      print('[ZERO CROSS] set 1')
      self.zero_cross = 1
    elif goal_ang < 0:
      goal_ang += 360
      print('[ZERO CROSS] set 2')
      self.zero_cross = 2
    self.card_present = True
    self.next_heading = goal_ang
    self.current_node_idx += 1
    self.updated = True
    print('[CONTROLLER]', 'curr=', heading)
    print('[CONTROLLER]', 'goal=', goal_ang)
    #threadLock.release()

  def go_listener(self, arg1):
    print('[CONTROLLER]', 'recv :', arg1)
    self.go = True

  def cmd_listener(self, arg1):
    self.next_command = arg1
    
  def motor_listener(self, arg1, arg2):
    print('[CONTROLLER]', 'recv pwm params :', arg1, arg2)
    if arg1 == 'set_pwm_l':
      self.motor.set_pwm_l(arg2)
    elif arg1 == 'set_pwm_r':
      self.motor.set_pwm_r(arg2)
  
  def read_normalized_auzimuth(self):
      current_heading = self.qmc.read_azimuth()
      if self.zero_cross == 1:
        if current_heading > 180:
          return current_heading - 360
        else:
          return current_heading
      elif self.zero_cross == 2:
        if current_heading < 180:
          return 360 + current_heading
        else:
          return current_heading
      else:
        return current_heading

  def run(self):
    pub.subscribe(self.rfid_listener, 'rfid')
    pub.subscribe(self.go_listener, 'auto')
    pub.subscribe(self.cmd_listener, 'camera')
    pub.subscribe(self.motor_listener, 'motor')
    global threadLock
    while True:
      #threadLock.acquire()
      if not self.go:
        continue
      if self.stop:
        self.motor.stop()
        break
      #time.sleep(0.1)
      current_heading = self.read_normalized_auzimuth()
      if self.zero_cross != 0:
        print('[ZERO CROSS] current:{}, next: {}'.format(current_heading, self.next_heading))
        print('[ZERO CROSS] error: {}'.format(self.next_heading - current_heading))
      
      if self.card_present:
        #print('[CONTROLLER]', 'curr=', current_heading)
        #print('[CONTROLLER]', 'goal=', self.next_heading)
        if current_heading - self.next_heading < -5:
          self.next_command = 'r'
        elif current_heading - self.next_heading > 5:
          self.next_command = 'l'
        else:
          print('[CONTROLLER]', 'turn complete')
          self.zero_cross = 0
          self.card_present = False
      else:
        self.next_command = 'f'
        if self.next_command == 'l' or self.next_command == 'r':
          if current_heading - self.next_heading < -5:
            self.next_command = 'r'
          elif current_heading - self.next_heading > 5:
            self.next_command = 'l'

      if self.current_command != self.next_command:
        if self.next_command == 'l':
          self.motor.left()
        elif self.next_command == 'r':
          self.motor.right()
        elif self.next_command == 'f':
          self.motor.forward()
        elif self.next_command == 'b':
          self.motor.backward()
        else:
          self.motor.stop()
        self.current_command = self.next_command
      #threadLock.release()
