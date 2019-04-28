#!/usr/bin/env python3
from pid import PID
import os
import time


class Rotation:
    def __init__(self, motor_left, motor_right, gyro):
        self.left_motor = motor_left
        self.right_motor = motor_right
        self.gyro = gyro

        self.pid = PID(6,0,0, max_val=self.left_motor.max_speed/5, min_val=-self.left_motor.max_speed/5, debug=True)
        os.system("cat debug_rotation.log >> debug_rotation.log.old; rm debug_rotation.log")
        # Povprečje 3 meritev 10x360° (CW): 35+15+27,5 / 3 = 28,83° napake
        # CCW je pribl natančen
        # torej za CW je:
        # 3600+28,83°= 3627.83° realni kot za kok se je obrnu
        # torej na en krog je to 2.883° napake
        # torej je za 1 izmerjeno stopinjo realno 1+2.883/360=1+0,0080083°=1,008008° stopinje nrjene
        

    def print_to_file(self, string):
            with open("debug_rotation.log",'a') as f:
                f.write(string)

    def __call__(self, abs_degrees):
        self.print_to_file("---start-rotation---\n")
        self.print_to_file("Kp: "+str(self.pid.Kp)+","+"Ki: "+str(self.pid.Ki)+","+"Kd: "+str(self.pid.Kd)+"\n")
        num_of_end = 0
        #self.left_motor.ramp_up_sp = 100
        #self.right_motor.ramp_up_sp = 100
        while 1:
            

            deg_current = self.gyro.angle()
            if abs(deg_current-abs_degrees)<0.2:
                
                self.left_motor.command, self.right_motor.command="stop","stop"
                
                self.left_motor.speed_sp, self.right_motor.speed_sp = 0,0
                
                
                time.sleep(0.5)
                if abs(self.gyro.angle()-abs_degrees)<0.2:
                    self.pid.reset()
                    self.print_to_file("...end-rotation...\n")
                    break
            
            
                

                
            
                
            err = (abs_degrees-deg_current)
            reg, true_reg = self.pid(err)
            self.print_to_file(str(abs_degrees)+","+str(deg_current)+","+str(err)+","+ str(reg)+","+ str(true_reg)+"\n")
            self.left_motor.speed_sp, self.right_motor.speed_sp = reg, -reg
            self.left_motor.command, self.right_motor.command='run-forever','run-forever'
            


