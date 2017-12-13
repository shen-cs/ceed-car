import subprocess
import sys
"""
while True: 
  try: 
    proc = subprocess.Popen('./test', shell=True, stdout=subprocess.PIPE)
    s = proc.stdout.read()
    print(float(s.decode('utf-8')))
  except KeyboardInterrupt:
    print()
    exit(-1)
"""

class QMC5883(object):
  def __init__(self):
    pass
  
  def read_azimuth(self):
    proc = subprocess.Popen('/home/pi/ceed_car/hardcode/wrap_qmc/src/test', shell=True, stdout=subprocess.PIPE)
    s = proc.stdout.read().decode('utf-8')
    return float(s)
