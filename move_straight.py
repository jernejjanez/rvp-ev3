#!/usr/bin/env python3
from pid import PID
import math
import time
import sys
import os

class MoveStraight:
    def __init__(self, left_motor, right_motor, gyro):
        #self.tank_pair = tank_pair
        #self.pid_left = PID(5,0.2,0.1, max_val=10, min_val=-10)
        #self.pid_right = PID(5,0.2,0.1, max_val=10, min_val=-10)
        self.left_motor = left_motor
        self.right_motor = right_motor
        
        # 5,1,15 je najbolš do zdej
        self.pid_rotation_plus = PID(5,1,15, max_val=self.left_motor.max_speed*0.25, min_val=-self.left_motor.max_speed*0.25, debug=True)
        self.pid_rotation_minus = PID(2,0,9, max_val=self.left_motor.max_speed*0.25, min_val=-self.left_motor.max_speed*0.25, debug=True)
        self.pid_straight = PID(40,0,0, max_val=(self.left_motor.max_speed-self.left_motor.max_speed*0.25)*0.5, 
                                        min_val=(-self.left_motor.max_speed+self.left_motor.max_speed*0.25)*0.5, debug=True)
        print(self.left_motor.max_speed)
        self.time_period = 0.1 # s
        self.gyro = gyro

        os.system("cat debug.log >> debug.log.old; rm debug.log")

        # r = 1.84 cm alpa (kolo) hitrost 1560 °/s
        # r = 2.744 cm hitrost 1050 °/s
        # TODO: prevert te cifre
        self.r = 2.744 #polmer
        self.speed_deg_per_s = 1050 # °/s
        
    def debug_print(self, *args, **kwargs):
        '''Print debug messages to stderr.
        This shows up in the output panel in VS Code. 
        '''
        print(*args, **kwargs, file=sys.stderr)
    
    def print_to_file(self, string):
        with open("debug.log",'a') as f:
            f.write(string)

    def _cm_moved(self, time_passed):
        #self.debug_print(self.left_motor.speed,",",self.right_motor.speed)
        cnts_p_s = (self.left_motor.speed + self.right_motor.speed)/2
        cnts_p_rot = self.left_motor.count_per_rot
        rot_p_s = cnts_p_s/cnts_p_rot

        #speed_deg_per_s_current = self.speed_deg_per_s*(speed_percent/100)
        #speed_cm_per_s = (speed_deg_per_s_current/360)*2*math.pi*self.r
        #return speed_cm_per_s*self.time_period
        return rot_p_s*time_passed*2*math.pi*self.r

    def __call__(self,centimeters):
        if centimeters > 0:
            self.pid_rotation = self.pid_rotation_plus
        elif centimeters < 0:
            self.pid_rotation = self.pid_rotation_minus
        else:
            self.debug_print(str(centimeters))
            return

        self.left_motor.ramp_up_sp, self.right_motor.ramp_up_sp = 8000, 8000
        
        #self.__init__(self.left_motor,self.right_motor, self.gyro)
        
        starting_angle = self.gyro.angle()
        curr_path = 0
        old_speed=0
        rotation_integrl = 0
        old_angle = 0
        self.print_to_file("---start-straight----\n")
        self.print_to_file("pid_straight:"+str(self.pid_straight.Kp)+","+str(self.pid_straight.Ki)+","+str(self.pid_straight.Kd))
        self.print_to_file(","+"pid_rotation:"+str(self.pid_rotation.Kp)+","+str(self.pid_rotation.Ki)+","+str(self.pid_rotation.Kd)+"\n")
        
        begin_time=time.time()
        while 1:
            if (abs(curr_path - centimeters)<0.2):
                #self.pid_left.reset()
                #self.pid_right.reset()
                #self.tank_pair.off(brake=True)
                self.left_motor.command="stop"
                self.right_motor.command="stop"
                self.left_motor.speed_sp = 0
                self.right_motor.speed_sp = 0
                self.pid_rotation.reset()
                self.pid_rotation_minus.reset()
                self.pid_rotation_plus.reset()
                self.pid_straight.reset()
                self.print_to_file("...end-straight...\n")
                break

            # Pid for straight path
            err_path = centimeters - curr_path
            speed_straight, real_straight_reg = self.pid_straight(err_path)
            #self.debug_print("error:", centimeters-curr_path)
            #self.debug_print("regval:",speed_straight)
            
            # rotation pid
            # TODO: prevert da so napake pravilne
            # Note: napake so različno računane je gledano na kot aktuatorja
            #angle_reduction_left = self.pid_left(starting_angle - self.gyro.angle)
            #angle_reduction_right = self.pid_right(self.gyro.angle - starting_angle)
            err_angle = starting_angle - self.gyro.angle()
            

            angle_reduction, real_angle_reg = self.pid_rotation(rotation_integrl)
            #self.debug_print("angle_left:", angle_reduction, "current angle:",self.gyro.angle,"wanted angle:",starting_angle)

            
            
            old_speed = speed_straight#+(abs(angle_reduction_left)+abs(angle_reduction_right))/2
            
            #self.debug_print("Curr_path:",curr_path)
            #time.sleep(self.time_period)
            #self.debug_print()
            #self.tank_pair.on(left_speed=speed_straight+angle_reduction, right_speed=speed_straight-angle_reduction)
            l_speed = speed_straight + angle_reduction
            r_speed = speed_straight - angle_reduction
            self.left_motor.speed_sp = l_speed
            self.right_motor.speed_sp = r_speed
            self.left_motor.command = 'run-forever'
            self.right_motor.command = 'run-forever'
            self.print_to_file(str(err_path)+","+str(speed_straight)+","+str(real_straight_reg)+','+str(angle_reduction)+','+str(real_angle_reg)+','+str(l_speed)+","+str(r_speed)+','+str(err_angle))

            # end_time=time.time()
            time_passed = time.time()-begin_time
            begin_time = time.time()
            curr_path += self._cm_moved(time_passed)
            rotation_integrl += time_passed*(err_angle+old_angle)/2
            old_angle = err_angle
            self.print_to_file(','+str(time_passed)+","+str(curr_path)+","+str(rotation_integrl)+"\n")
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