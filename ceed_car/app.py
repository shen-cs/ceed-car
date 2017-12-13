#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request, abort
import sys
import json
import time
from wrap_qmc.qmc5883 import QMC5883
from pubsub import pub
from threads.rfid import rfid_thread
from camera_pi import Camera
from libraries.motor_pwm import Motor
sys.path.append('./map/map_class')
from map import Map
from datetime import datetime, timedelta

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)

mode = sys.argv[1]
qmc = QMC5883()
heading = 0
card_detected = False
last_card_read = datetime.min

map = Map('map/map.json')
map.load_pathfile(sys.argv[2])

def update_heading():
  global heading, qmc
  heading = qmc.read_azimuth()

def convert_cmd(cmd):
  global heading, qmc, card_detected
  if card_detected:
    return None
  
  if cmd == 'l' or cmd == 'r':
    diff = qmc.read_azimuth() - heading
    #print('diff', diff)
    if diff > 5:
      cmd = 'l'
    elif diff < -5:
      cmd = 'r'
    else:
      cmd = 'f'
  return cmd


@app.route('/')
def index():
  """Video streaming home page."""
  return render_template('index.html')

if mode == 'rc':
  @app.route('/forward')
  def motor_forward():
    global motor
    motor.forward()
    return json.dumps({"success": True})

  @app.route('/backward')
  def motor_backward():
    global motor
    motor.backward()
    return json.dumps({"success": True})

  @app.route('/left')
  def motor_left():
    global motor
    motor.left()
    return json.dumps({"success": True})

  @app.route('/right')
  def motor_right():
    global motor
    motor.right()
    return json.dumps({"success": True})

  @app.route('/stop')
  def motor_stop():
    global motor
    motor.stop()
    return json.dumps({"success": True})

else:
  def cmd_to_motor(cmd):
    global motor
    if cmd == 'r':
      motor.right()
    elif cmd == 'l':
      motor.left()
    elif cmd == 'f':
      motor.forward()
    else:
      motor.stop()

@app.route('/pwm_l', methods=['POST'])
def pwm_left():
  global motor
  if not request.form:
    abort(400)
  val = request.form['val']
  motor.set_pwm_l(val)
  return json.dumps({"success": True})

@app.route('/pwm_r', methods=['POST'])
def pwm_right():
  global motor
  if not request.form:
    abort(400)
  val = request.form['val']
  motor.set_pwm_r(val)
  return json.dumps({"success": True})


@app.after_request
def after_request(res):
  res.headers.add('Access-Control-Allow-Origin', '*')
  res.headers.add('Access-Control-Allow-Headers', 'X-Custom-Header, Origin, X-Requested-With, Content-Type')
  res.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, OPTIONS')
  return res

def gen(camera):
  """Video streaming generator function."""
  global mode
  print('mode', mode)
  while True:
    frame, cmd = camera.get_frame()
    #if mode == 'auto' or 'debug':
    #  cmd = convert_cmd(cmd)
      #print(cmd)
    #  if mode == 'auto':
    #    cmd_to_motor(cmd)
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
  global mode
  """Video streaming route. Put this in the src attribute of an img tag."""
  return Response(gen(Camera('rc')),
                  mimetype='multipart/x-mixed-replace; boundary=frame')

def path_finding():
  global map, last_card_read, motor, heading, card_detected
  dist_rec = []
  direc_rec = []
  camera = Camera('auto')
  node = map.find_node(map.path['header']['start'])
  while node.next_node_id:
    dist_rec.append(node.get_edge_len(node.next_node_id))
    if node.prev_node_id:
      direc_rec.append(node.get_direction())
      print(node.id)
    node = map.find_node(map.path[node.id]['next'])
  
  update_heading()
  current_node_idx = 0
  while True:
    frame, cmd = camera.get_frame()
    if mode == 'auto' and card_detected:
      print('card detected')
      if current_node_idx == len(direc_rec):
        print('complete')
        return
      motor.stop()
      time.sleep(0.1)
      update_heading()
      goal_ang = heading+direc_rec[current_node_idx]
      if goal_ang > 360:
        goal_ang -= 360
      elif goal_ang < 0:
        goal_ang += 360
      print('goal ang:', goal_ang)
      heading = goal_ang
      card_detected = False
      current_node_idx += 1
      cmd = 'l'
      last_card_read = datetime.now()
    elif mode == 'auto' or mode == 'debug':
      cmd = convert_cmd(cmd)
    if mode == 'auto':
      cmd_to_motor(cmd)
    #yield (b'--frame\r\n'
    #       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def rfid_listener(arg1):
  global card_detected, last_card_read
  if arg1:
    if (datetime.now() - last_card_read) < timedelta(0, 5):
      return
    card_detected = True
    #time.sleep(1)
    #update_heading()
    #card_detected = False
    print(arg1)

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print('Usage: python3 {} mode/rc'.format(sys.argv[0]))
    exit(-1)
  motor = Motor([18, 23, 24, 25])
  update_heading()
  rfid_thd = rfid_thread('rfid')
  pub.subscribe(rfid_listener, 'rfid')
  try:
    rfid_thd.start()
    app.run(host='0.0.0.0', threaded=True, debug=False)
    #path_finding()
  except Error as e:
    print('fuck')
    print(e)
    motor.stop()
    motor.cleanup()
    exit(-1)
