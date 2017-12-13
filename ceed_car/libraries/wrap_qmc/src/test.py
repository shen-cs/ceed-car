import subprocess
import sys
"""
proc = subprocess.Popen("./test", shell=True, stdout=subprocess.PIPE)
for line in proc.stdout:
  out = line.decode('utf-8')
  #print(out)
  try:
    data = float(out)
    print(data)
  except ValueError:
    print('Error')
    pass
  except KeyboardInterrupt:
    exit(-1)
#print(s.decode('UTF-8'))

"""
while True: 
  try: 
    proc = subprocess.Popen('./test', shell=True, stdout=subprocess.PIPE)
    s = proc.stdout.read()
    print(float(s.decode('utf-8')))
  except KeyboardInterrupt:
    print()
    exit(-1)
