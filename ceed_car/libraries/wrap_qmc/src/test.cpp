#include <iostream>
#include <chrono>
#include <thread>
#include <math.h>
#include <stdint.h>
#include "I2Cdev.h"
#include "MechaQMC5883.h"

using namespace std;

int main() {
  MechaQMC5883 qmc;
  qmc.init();
  int16_t x, y, z;
  float a;
  int i = 0;
  while(i == 0) {
    qmc.read(&x, &y, &z, &a);
    cout << a << endl;
    i++;
    //this_thread::sleep_for(chrono::milliseconds(100));
  }
  return 0;
}
