import sys
from libraries.MFRC522 import MFRC522
from pubsub import pub
import signal
import RPi.GPIO as gpio
import time
import threading

class rfid_thread(threading.Thread):
  def __init__(self, name):
    print('[RFID]', 'initialize')
    threading.Thread.__init__(self)
    self.name = name
    self.rfid = MFRC522()
    self.reading = True
    self.last_uid = 0
    #signal.signal(signal.SIGINT, self.end_read)
  
  def run(self):
    print('[RFID]', 'starting')
    while self.reading:
      try:
        self.read()
      except KeyboardInterrupt:
        print()
        exit(-1)
  
 # def end_read(self, signal, frame):
  #  print()
  #  self.reading = False
  #  gpio.cleanup()

  def read(self):
    OK = self.rfid.MI_OK
    (status, tag_type) = self.rfid.MFRC522_Request(self.rfid.PICC_REQIDL)
    
    (status, uid) = self.rfid.MFRC522_Anticoll()
    # if have uid
    if status == OK:
      if uid != self.last_uid:
        print('[RFID]', 'Card detected')
        pub.sendMessage('rfid', arg1='card detected')
        self.last_uid = uid

