from pid import PID
import os
import time
class Rotation:
    def __init__(self, motor_left, motor_right, gyro):
        self.left_motor = motor_left
        self.right_motor = motor_right
        self.gyro = gyro

        self.pid = PID(1,1,0, max_val=self.left_motor.max_speed/2, min_val=-self.left_motor.max_speed/2, debug=True)
        os.system("cat debug_rotation.log >> debug_rotation.log.old; rm debug_rotation.log")
        # Povprečje 3 meritev 10x360° (CW): 35+15+27,5 / 3 = 28,83° napake
        # CCW je pribl natančen
        # torej za CW je:
        # 3600+28,83°= 3627.83° realni kot za kok se je obrnu
        # torej na en krog je to 2.883° napake
        # torej je za 1 izmerjeno stopinjo realno 1+2.883/360=1+0,0080083°=1,008008° stopinje nrjene
        self.drift = 0        
        self.drift_koef_cw = 0.005
        self.drift_koef_ccw = 0

    def print_to_file(self, string):
            with open("debug_rotation.log",'a') as f:
                f.write(string)

    def calc_angle(self, time_delta):
        rate = 0
        for i in range(10):
            rate += self.gyro.rate

        return rate/10*time_delta

    def __call__(self, abs_degrees):
        self.print_to_file("---start-rotation---\n")
        num_of_end = 0
        self.left_motor.ramp_up_sp = 500
        self.right_motor.ramp_up_sp = 500
        deg_current = 0
        start_time = time.time()

        #self.gyro.get

        
        #old_meas = self.gyro.angle
        while 1:
            '''
            deg_measurement = self.gyro.angle
            if deg_measurement > old_meas:
                self.drift += self.drift_koef_cw*(deg_measurement-old_meas)
            elif deg_measurement < old_meas:
                self.drift += self.drift_koef_ccw*(old_meas-deg_measurement)
            old_meas=deg_measurement
            '''

            if abs(deg_current-abs_degrees)<0.2:
                
                self.left_motor.command="stop"
                self.right_motor.command="stop"
                self.left_motor.speed_sp = 0
                self.right_motor.speed_sp = 0
                
                time.sleep(0.5)
                if abs(deg_current-abs_degrees)<0.2:
                    self.pid.reset()
                    self.print_to_file("...end-rotation...\n")
                    break
            
            
                

                
            
                
            err = (abs_degrees-deg_current)
            reg, true_reg = self.pid(err)
            self.print_to_file(str(abs_degrees)+","+str(deg_current)+","+str(err)+","+ str(reg)+","+ str(true_reg)+"\n")
            self.left_motor.speed_sp = reg
            self.right_motor.speed_sp = -reg
            self.left_motor.command='run-forever'
            self.right_motor.command='run-forever'
            end_time = time.time()
            time_delta = end_time-start_time
            start_time=time.time()
            deg_current+=self.calc_angle(time_delta)

