#!/usr/bin/python

import smbus
import math
import numpy as np
import pyqtgraph as pg
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

def read():
  gyro_xout = read_word_2c(0x43)
  gyro_yout = read_word_2c(0x45)
  gyro_zout = read_word_2c(0x47)
  # normalize 
  gyro_xout /= 131
  gyro_yout /= 131
  gyro_zout /= 131


  accel_xout = read_word_2c(0x3b)
  accel_yout = read_word_2c(0x3d)
  accel_zout = read_word_2c(0x3f)

  accel_xout_scaled = accel_xout / 16384.0
  accel_yout_scaled = accel_yout / 16384.0
  accel_zout_scaled = accel_zout / 16384.0


  x_rotation = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
  y_rotation =  get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
  
  return [gyro_xout, gyro_yout, gyro_zout, accel_xout_scaled, accel_yout_scaled, accel_zout_scaled, x_rotation, y_rotation]


def run():
  global plotItem, t, y
  while True:
    gyro_xout, gyro_yout, gyro_zout, accel_xout_scaled, accel_yout_scaled, accel_zout_scaled, x_rotation, y_rotation = read()
    y[:-1] = y[1:]
    y[-1] = gyro_zout
    plotItem.plot(t, y, clear=True)
    pg.QtGui.QApplication.processEvents()

if __name__ == '__main__':
   win = pg.GraphicsWindow(title='mpu6050 test')
   plotItem = win.addPlot(title='yaw')
   plotItem.setYRange(-90, 90)
   t = np.arange(100)
   y = np.zeros(100)
   try:
      run()
   except KeyboardInterrupt:
      exit(-1)

