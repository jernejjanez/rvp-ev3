#!/usr/bin/env python3
from ev3dev2.sensor import lego
import time
class GyroSensor:
    def __init__(self):
        self.gyro = lego.GyroSensor()
        
        self.gyro.mode = lego.GyroSensor.MODE_GYRO_CAL
        self.gyro.mode = lego.GyroSensor.MODE_GYRO_RATE
        self.gyro.mode = lego.GyroSensor.MODE_GYRO_ANG
        
        self.drift = 0
        self.angle_old=0
        self.drift_koef_cw = 0.0075
        self.drift_koef_ccw = 0


    def wait_until_angle_changed_by(self, delta, direction_sensitive=False):
        self.gyro.wait_until_angle_changed_by(delta,direction_sensitive)

    def angle(self):
        angle = self.gyro.angle
        return angle
        if angle > self.angle_old:
            self.drift += (angle-self.angle_old)*self.drift_koef_cw
            self.angle_old = angle
            return self.drift+angle
        else:
            self.drift += (self.angle_old-angle)*self.drift_koef_ccw
            self.angle_old = angle
            return self.drift+angle
    
    
