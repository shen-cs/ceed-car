import RPi.GPIO as gpio

class Motor(object):
   def __init__(self, pins):
     """pins: input1 ~ input4"""
     gpio.setmode(gpio.BCM)
     self.pins = pins
     for pin in pins:
       gpio.setup(pin, gpio.OUT)
       gpio.output(pin, 0)

   def drive(self, outputs):
     for i in range(len(outputs)):
       gpio.output(self.pins[i], outputs[i])
     

   def forward(self):
     outputs = [1, 0, 1, 0]
     self.drive(outputs)

   def backward(self):
     outputs = [0, 1, 0, 1]
     self.drive(outputs)
   
   def left(self):
     outputs = [0, 1, 1, 0]
     self.drive(outputs)
   
   def right(self):
     outputs = [1, 0, 0, 1]
     self.drive(outputs)
   
   def stop(self):
     outputs = [0, 0, 0, 0]
     self.drive(outputs)
   def cleanup(self):
     gpio.cleanup()






