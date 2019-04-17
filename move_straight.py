#!/usr/bin/env python3
from pid import PID
import math
import time
import sys

class MoveStraight:
    def __init__(self,left_motor, right_motor, gyro):
        #self.tank_pair = tank_pair
        #self.pid_left = PID(5,0.2,0.1, max_val=10, min_val=-10)
        #self.pid_right = PID(5,0.2,0.1, max_val=10, min_val=-10)
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.pid_rotation = PID(5,0.2,0.1, max_val=10, min_val=-10)
        self.pid_straight = PID(3,0.5,0, max_val=90, min_val=-90)
        
        self.time_period = 0.1 # s
        self.gyro = gyro
        

        # r = 1.84 cm alpa (kolo) hitrost 1560 °/s
        # r = 2.744 cm hitrost 1050 °/s
        # TODO: prevert te cifre
        self.r = 2.35 #polmer
        self.speed_deg_per_s = 1050 # °/s
        
    def debug_print(self, *args, **kwargs):
        '''Print debug messages to stderr.
        This shows up in the output panel in VS Code. 
        '''
        print(*args, **kwargs, file=sys.stderr)

    def _cm_moved(self,speed_percent, time_passed):
        speed_deg_per_s_current = self.speed_deg_per_s*(speed_percent/100)
        speed_cm_per_s = (speed_deg_per_s_current/360)*2*math.pi*self.r
        return speed_cm_per_s*self.time_period

    def __call__(self,centimeters):
        starting_angle = self.gyro.angle
        curr_path = 0
        end_time=time.time()+0.5
        old_speed=0
        while 1:
            begin_time=time.time()
            if (abs(curr_path - centimeters)<0.2):
                #self.pid_left.reset()
                #self.pid_right.reset()
                self.pid_rotation.reset()
                self.pid_straight.reset()
                
                self.tank_pair.off(brake=True)
                break

            # Pid for straight path
            speed_straight = self.pid_straight(centimeters-curr_path)
            #self.debug_print("error:", centimeters-curr_path)
            self.debug_print("regval:",speed_straight)
            
            # rotation pid
            # TODO: prevert da so napake pravilne
            # Note: napake so različno računane je gledano na kot aktuatorja
            #angle_reduction_left = self.pid_left(starting_angle - self.gyro.angle)
            #angle_reduction_right = self.pid_right(self.gyro.angle - starting_angle)
            angle_reduction = self.pid_rotation(starting_angle - self.gyro.angle)
            #self.debug_print("angle_left:", angle_reduction, "current angle:",self.gyro.angle,"wanted angle:",starting_angle)

            
            
            old_speed=speed_straight#+(abs(angle_reduction_left)+abs(angle_reduction_right))/2
            
            #self.debug_print("Curr_path:",curr_path)
            #time.sleep(self.time_period)
            #self.debug_print()
            #self.tank_pair.on(left_speed=speed_straight+angle_reduction, right_speed=speed_straight-angle_reduction)
            self.left_motor.speed_sp = speed_straight+angle_reduction
            self.right_motor.speed_sp = speed_straight-angle_reduction
            self.left_motor.command('run-forever')
            self.right_motor.command('run-forever')
            end_time=time.time()
            curr_path += self._cm_moved(old_speed,end_time-begin_time)
            #self.debug_print("time_passed: ",end_time-begin_time)            


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