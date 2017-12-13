from pubsub import pub
from rfid import rfid_thread

def rfid_listener(arg1):
  print(arg1)

pub.subscribe(rfid_listener, 'rfid')

rfid_thd = rfid_thread('rfid')
rfid_thd.start()
