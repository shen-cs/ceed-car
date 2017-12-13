
#!/usr/bin/python

import smbus
import math
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

class Mpu(object):
  def __init__(self):
      self.bus = smbus.SMBus(1)
      self.address = 0x68
      self.bus.write_byte_data(self.address, power_mgmt_1, 0)

  def read_byte(self, adr):
      return self.bus.read_byte_data(self.address, adr)

  def read_word(self, adr):
      high = self.bus.read_byte_data(self.address, adr)
      low = self.bus.read_byte_data(self.address, adr+1)
      val = (high << 8) + low
      return val

  def read_word_2c(self, adr):
      val = self.read_word(adr)
      if (val >= 0x8000):
          return -((65535 - val) + 1)
      else:
          return val

  def dist(self, a,b):
      return math.sqrt((a*a)+(b*b))

  def get_y_rotation(self, x,y,z):
      radians = math.atan2(x, self.dist(y,z))
      return -math.degrees(radians)

  def get_x_rotation(self, x,y,z):
      radians = math.atan2(y, self.dist(x,z))
      return math.degrees(radians)

  # Now wake the 6050 up as it starts in sleep mode

  def read(self):
    gyro_xout = self.read_word_2c(0x43)
    gyro_yout = self.read_word_2c(0x45)
    gyro_zout = self.read_word_2c(0x47)
    # normalize 
    gyro_xout /= 131
    gyro_yout /= 131
    gyro_zout /= 131

    return [gyro_xout, gyro_yout, gyro_zout]

"""   
    accel_xout = self.read_word_2c(0x3b)
    accel_yout = self.read_word_2c(0x3d)
    accel_zout = self.read_word_2c(0x3f)

    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0


    x_rotation = self.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    y_rotation =  self.get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    
    return [gyro_xout, gyro_yout, gyro_zout, accel_xout_scaled, accel_yout_scaled, accel_zout_scaled, x_rotation, y_rotation]
"""


