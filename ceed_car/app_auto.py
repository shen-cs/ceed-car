#!/usr/bin/env python
import sys
paths = ['./map/map_class', './camera', './libraries', './opencv']
sys.path += paths
from importlib import import_module
import os
from flask import Flask, render_template, Response, request, abort
import json
import time
from pubsub import pub
from threads.rfid import rfid_thread
from threads.controller import controller_thread
from camera.camera_pi import Camera
from datetime import datetime, timedelta
from map import Map

app = Flask(__name__)

map_filename = sys.argv[1]
path_filename = sys.argv[2]

print('Map file name:', map_filename)
print('Path file name:', path_filename)

map = Map(map_filename)
map.load_pathfile(path_filename)

@app.route('/')
def index():
  """Video streaming home page."""
  return render_template('index.html')

@app.route('/pwm_l', methods=['POST'])
def pwm_left():
  if not request.form:
    abort(400)
  val = request.form['val']
  pub.sendMessage('controller', arg1='set_pwm_l', arg2=val)
  return json.dumps({"success": True})

@app.route('/pwm_r', methods=['POST'])
def pwm_right():
  if not request.form:
    abort(400)
  val = request.form['val']
  pub.sendMessage('controller', arg1='set_pwm_r', arg2=val)
  return json.dumps({"success": True})

@app.after_request
def after_request(res):
  res.headers.add('Access-Control-Allow-Origin', '*')
  res.headers.add('Access-Control-Allow-Headers', 'X-Custom-Header, Origin, X-Requested-With, Content-Type')
  res.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, OPTIONS')
  return res

def gen(camera):
  """Video streaming generator function."""
  pub.sendMessage('auto', arg1='go')
  while True:
    frame, cmd = camera.get_frame()
    pub.sendMessage('camera', arg1=cmd)
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
  """Video streaming route. Put this in the src attribute of an img tag."""
  return Response(gen(Camera('auto')),
                  mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
  rfid_thd = rfid_thread('rfid')
  controller_thd = controller_thread(map)
  #pub.subscribe(rfid_listener, 'rfid')
  try:
    rfid_thd.start()
    controller_thd.start()
    app.run(host='0.0.0.0', threaded=True, debug=False)
  except Error as e:
    print('fuck')
    print(e)
    exit(-1)
