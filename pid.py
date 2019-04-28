#!/usr/bin/env python3
import time
import math

class PID:
    def __init__(self, Kp, Ki, Kd, bias=0, max_val=math.inf, min_val=-math.inf, debug=False):
        self.error_old = 0
        self.integral = 0
        self.time_prev = 0

        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        
        self.bias = bias
        self.max_val = max_val
        self.min_val = min_val
        self.debug = debug

    def __call__(self, error):
        current_time = time.time()
        iteration_time = current_time - self.time_prev

        if self.time_prev != 0:
            self.integral += (error*iteration_time)
            if self.integral > self.max_val:
                self.integral = self.max_val
            elif self.integral < self.min_val:
                self.integral = self.min_val
            derivative = (error - self.error_old)/iteration_time
            control = self.Kp*error + self.Ki*self.integral + self.Kd*derivative + self.bias
        else:
            control = self.Kp*error
        self.error_old = error
        self.time_prev = current_time
        if self.debug:
            old_control = control
        if control > self.max_val:
            control = self.max_val
        elif control < self.min_val:
            control = self.min_val
        if self.debug:
            return control, old_control
        return control
    
    def reset(self):
        self.error_old = 0
        self.integral = 0
        self.time_prev = 0

def _bell_curve(i):
    a = [0,0,0,1,2,3,4,5,6,7,7,7,8,8,8,8,8,7,6,5,4,3,2,1,0,0]
    if i >= len(a):
        return 0
    else:
        return a[i]


if __name__ == "__main__":
    import random
    pid = PID(100,10,10)
    val = 5
    wanted_val = 0
    iter = 20
    i=0
    while 1:
        print("err",_bell_curve(i))
        control = pid(-_bell_curve(i))
        print("control",control)
        r = random.random() if random.random() > 0.5 else 0
        val = val + control + r
        #print("val",val)
        time.sleep(0.5)
        i+=1
        #pid.reset()