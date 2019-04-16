#!/usr/bin/env python3
from pid import PID
import math
import time
import sys

class MoveStraight:
    def __init__(self,tank_pair, gyro):
        self.tank_pair = tank_pair
        self.pid_left = PID(100,10,10, max_val=10, min_val=-10)
        self.pid_right = PID(100,10,10, max_val=10, min_val=-10)
        self.pid_straight = PID(1000,100,10, max_val=90, min_val=-90)
        
        self.time_period = 0.01 # s
        self.gyro = gyro
        

        # r = 1.84 cm alpa (kolo) hitrost 1560 °/s
        # r = 2.744 cm hitrost 1050 °/s
        # TODO: prevert te cifre
        self.r = 2.744 #polmer
        self.speed_deg_per_s = 1560 # °/s
        
    def debug_print(self, *args, **kwargs):
        '''Print debug messages to stderr.
        This shows up in the output panel in VS Code. 
        '''
        print(*args, **kwargs, file=sys.stderr)

    def _cm_moved(self,speed_percent):
        speed_deg_per_s_current = self.speed_deg_per_s*(speed_percent/100)
        speed_cm_per_s = (speed_deg_per_s_current/360)*2*math.pi*self.r
        return speed_cm_per_s*self.time_period

    def __call__(self,centimeters):
        starting_angle = self.gyro.angle
        curr_path = 0
        while 1:
            if (abs(curr_path - centimeters)<0.2):
                self.pid_left.reset()
                self.pid_right.reset()
                self.pid_straight.reset()
                
                self.tank_pair.off(brake=True)
                break

            # Pid for straight path
            speed_straight = self.pid_straight(centimeters-curr_path)
            self.debug_print("error:", centimeters-curr_path)
            self.debug_print("regval:",speed_straight)
            
            # rotation pid
            # TODO: prevert da so napake pravilne
            # Note: napake so različno računane je gledano na kot aktuatorja
            angle_reduction_left = self.pid_left(starting_angle - self.gyro.angle)
            angle_reduction_right = self.pid_right(self.gyro.angle - starting_angle)
            self.debug_print("angle_left:", angle_reduction_left, "angle_right:", angle_reduction_right)


            self.tank_pair.on(left_speed=speed_straight+angle_reduction_left, right_speed=speed_straight+angle_reduction_right)
            curr_path += self._cm_moved(speed_straight)
            self.debug_print("Curr_path:",curr_path)
            time.sleep(self.time_period)
            
            self.debug_print()


class tp_dummy:
    def on(self, **kwargs):
        pass
    def off(self, **kwargs):
        pass


class gyro_dummy:
    angle=0


if __name__=="__main__":
    tp = tp_dummy()
    move_straight = MoveStraight(tp,gyro_dummy())
    move_straight(20)