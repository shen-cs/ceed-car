from qmc5883 import QMC5883
import time
if __name__ == '__main__':
  qmc = QMC5883()
  while True:
    try:
      print(qmc.read_azimuth())
      time.sleep(0.1)
    except KeyboardInterrupt:
      print()
      exit(-1)
