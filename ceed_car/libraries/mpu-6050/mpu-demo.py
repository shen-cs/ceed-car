import numpy as np
import pyqtgraph as pg
import time
from mpu import Mpu
from KFilter import KFilter
from ExpFilter import ExpFilter
def init(dt):
   x = np.zeros(2).reshape(2, 1)
   P = np.array([[1000., 0], [0, 1000]])
   F = np.array([[1., dt], [0, 1.]])
   u = np.zeros(2).reshape(2, 1)
   z = np.array([[0.]])
   H = np.array([[0., 1.]])
   R = np.array([[0.01]])
   Q = 0.5 * np.array([[np.power(dt, 5)/20., np.power(dt, 4)/8.], [np.power(dt, 4)/8., np.power(dt, 3)/3.]])

   return KFilter(x, P, F, u, z, H, R, Q), ExpFilter(0.1)

def run():
   global plotItem, y, mpu, kalman, dt, yaw_int, exp
   while True:
    # gyro_xout, gyro_yout, gyro_zout, accel_xout_scaled, accel_yout_scaled, accel_zout_scaled, x_rotation, y_rotation = mpu.read()
     gyro_xout, gyro_yout, gyro_zout = mpu.read()
    # kalman.filterOnce(np.array([[gyro_zout]]))
    # yaw, yaw_speed = kalman.x
     exp.filterOnce(gyro_zout)
     y[:-1] = y[1:]
     y[-1] = yaw_int
     yaw_int += (exp.state-1.5) * dt
     plotItem.plot(t, y, clear=True)
     pg.QtGui.QApplication.processEvents()
     time.sleep(dt)

if __name__ == '__main__':
   dt = 0.01
   yaw_int = 0
   kalman, exp = init(dt)
   win = pg.GraphicsWindow(title='mpu6050 test')
   plotItem = win.addPlot(title='yaw')
   plotItem.setYRange(-90, 90)
   t = np.arange(100)
   y = np.zeros(100)
   mpu = Mpu()
   try:
      run()
   except KeyboardInterrupt:
      exit(-1)
