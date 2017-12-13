import RPi.GPIO as gpio
import time
# 18,23,24,25
slow_rate = 1.0
class Motor(object):
   def __init__(self, pins_idx):
     """pins: input1 ~ input4"""
     gpio.setmode(gpio.BCM)
     self.pins = []
     self.pwm_l = 60
     self.pwm_r = 100
     for pin in pins_idx:
       gpio.setup(pin, gpio.OUT)
       p = gpio.PWM(pin, 50)
       self.pins.append(p)
       #gpio.output(pin, 0)

   def drive(self, outputs):
     for i in range(len(outputs)):
       self.pins[i].start(outputs[i])
   
   def set_pwm_l(self, left):
     self.pwm_l = float(left)

   def set_pwm_r(self, right):
     self.pwm_r = float(right)

   def forward(self):
     outputs = [self.pwm_l, 0, self.pwm_r, 0]
     self.drive(outputs)

   def backward(self):
     outputs = [0, self.pwm_l, 0, self.pwm_r]
     self.drive(outputs)
   
   def left(self):
     outputs = [0, self.pwm_l*slow_rate, self.pwm_r*slow_rate, 0]
     self.drive(outputs)
   
   def right(self):
     outputs = [self.pwm_l*slow_rate, 0, 0, self.pwm_r*slow_rate]
     self.drive(outputs)

   def sophleft(self, angle):
     outputs = [0, 0, 100, 90]
     self.drive(outputs)
     time.sleep(angle)
     self.stop()

   def sophright(self, angle):
     outputs = [90, 100, 0, 0]
     self.drive(outputs)
     time.sleep(angle)
     self.stop()
   
   def stop(self):
     outputs = [0, 0, 0, 0]
     self.drive(outputs)

   def cleanup(self):
     gpio.cleanup()






