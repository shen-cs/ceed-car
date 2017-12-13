import sys
sys.path.append('../../rc_control')
from libraries.motor import Motor

m = Motor([18, 23, 24, 25])
m.stop()
m.cleanup()

